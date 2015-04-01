import os
import sys
import subprocess
import multiprocessing
from Queue import Queue
from threading import Thread


def compress(file_queue, output_queue):
    """compress the files defined in media.py"""
    while True:
        filetype, infile, outfile, input_list = file_queue.get()
        
        base_dir = os.path.dirname(__file__)
        compressor_jar = os.path.join(base_dir,'yuicompressor-2.4.2.jar')
        file_to_compress = os.path.join(base_dir, 'dev', filetype, infile+'.'+filetype)
        
        if infile.endswith(".min"):
            output = open("{file_to_compress}".format(**locals()), "rb").read()
        else:
            output = subprocess.check_output('java -jar {compressor_jar} {file_to_compress}'.format(**locals()), shell=True)
        
        output_queue.put((filetype, infile, input_list, outfile, output))
        file_queue.task_done()

def combine(output_queue, files):
    while True:
        filetype, infile, input_list, outfile, data = output_queue.get()
        print >>sys.stderr, "{infile}.{filetype}".format(**locals())
        out = files[filetype][outfile]
        out['data'][infile] = data
        
        if len(out['data']) == len(input_list):
            print >>sys.stderr, "Building... {outfile}.{filetype}".format(**locals())
            for input in input_list:
                out['file'].write(out['data'][input])
        output_queue.task_done()

if __name__ == '__main__':
    import media
    
    base_dir = os.path.dirname(__file__)
    
    to_compress, to_combine = Queue(), Queue()
    files = {'css': {}, 'js': {}}

    for filetype, outdata in files.items():
        pro_path = os.path.join(base_dir,'pro',filetype)
        if not os.path.exists(pro_path):
            os.makedirs(pro_path)
        for out, inputs in getattr(media, '{0}_files'.format(filetype)).items():
            file_name = os.path.join(base_dir, 'pro', filetype, out+'.'+filetype)
            outdata[out] = {'file': open(file_name, "w+b"), 'data': {}}
            for i in inputs:
                to_compress.put((filetype, i, out, inputs))

    t = Thread(target=combine, args=(to_combine, files))
    t.daemon = True
    t.start()

    num_worker_threads = multiprocessing.cpu_count() * 2
    for i in xrange(num_worker_threads):
        t = Thread(target=compress, args=(to_compress, to_combine))
        t.daemon = True
        t.start()
    to_compress.join()
    to_combine.join()
