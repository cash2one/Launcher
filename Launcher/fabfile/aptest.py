import ApacheParser as AP

c = AP.ApacheConfig('httpd')

confs = c.parse_file('httpd.conf')


#configs = []
def parse_section(child_section, configs=[]):
    
    for i in range(len(child_section)):
        if child_section[i].section:
            #print '\n------New Section------\n'
            configs.append('New Section')
            #print child_section[i].name + ':' + str(child_section[i].values)
            configs.append([child_section[i].name, child_section[i].values])
            parse_section(child_section[i].children, configs)
            #print '\n------Section ends------\n'
            configs.append('Section End')
        else:
            #print child_section[i].name + ' : ' + str(child_section[i].values)
            configs.append([child_section[i].name, child_section[i].values])
    return configs
            
# for each in confs.children:
    # parse_section(each)
r = parse_section(confs.children)

for each in r:
    #if each[0] == 'Listen':
    print each
    
ports = [each[1][0] for each in r if each[0]=='Listen']
unneeded = [each[0] for each in r if each[0] in ('WSGIPythonPath', 'WSGIRestrictStdin', 'WSGIRestrictStdout')]

print ports, unneeded