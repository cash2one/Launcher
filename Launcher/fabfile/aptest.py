import ApacheParser as AP

c = AP.ApacheConfig('httpd')

confs = c.parse_file('httpd.conf')



def parse_section(child_section):
    for i in range(len(child_section)):
        if child_section[i].section:
            print '\n------New Section------\n'
            print child_section[i].name + ':' + str(child_section[i].values)
            parse_section(child_section[i].children)
            print '\n------Section ends------\n'
        else:
            print child_section[i].name + ' : ' + str(child_section[i].values)
            
#for each in confs.children:
    #parse_section(each)
parse_section(confs.children)