def parse_section(child_section, configs=[]):
    """Custom function for getting the full parsed config data from conf as list"""
    for i in range(len(child_section)):
        if child_section[i].section:
            configs.append('New Section')
            configs.append([child_section[i].name, child_section[i].values])
            parse_section(child_section[i].children, configs)
            configs.append('Section End')
        else:
            configs.append([child_section[i].name, child_section[i].values])
    return configs