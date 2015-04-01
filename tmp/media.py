from collections import Counter

js_files = {
'divineba.core' : [
    'jquery-1.7.1',
    'jquery.bgiframe',
    'jquery.positionBy',
    'jquery.hoverIntent',
    #'jquery.depends',
    'jquery.ba-bbq',
    'jquery.ajaxmanager',
    'jquery.event.drag-2.0.min',
    'date'
    ],
'divineba.ui' : [
    'ui.widget',
    'ui.mouse',
    'ui.core',
    'ui.draggable',
    'ui.resizable',
    'effects.core',
    'effects.slide',
    'effects.drop',
    'ui.sortable',
    'jquery.layout',
    'layout.config',
    'jquery.jdMenu',
    'tools.tabs-1.2.5',
    'tools.overlay-1.2.5',
    'tools.expose-1.2.5',
    'tools.overlay.apple-1.2.5',
#    'tools.scrollable-1.2.5',
    'jquery.checkbox',
    'jquery.quickpaginate',
    'fullcalendar',
    'jqgrid.plugins'

        ],
'divineba.form' : [
    'ui.dialog',
    'divineba.smartpopup',
    'jquery.mousewheel',
    'ui.datepicker',
    'jquery.timeentry',
    'jquery.dateentry',
    'jquery.sexycombo',
    'divineba.toolbar',
    'jquery.checkbox',
    'jquery.calculation',
    'jquery.spinbutton',
    'config',
    'controls',
    ],
'jquery.jqGrid': [
    'jqgrid/i18n/grid.locale-en',
    'jqgrid/grid.base',
    'jqgrid/grid.common',
    'jqgrid/grid.celledit',
    'jqgrid/grid.treegrid',
    'jqgrid/grid.setcolumns',
    'jqgrid/jquery.fmatter',
    'jqgrid/grid.tbltogrid',
    'jqgrid/grid.grouping',
#    'jqgrid/grid.formedit',
#    'jqgrid/grid.inlinedit',
    'jqgrid/grid.subgrid',
    'jqgrid/grid.custom',
#    'jqgrid/grid.postext',
#    'jqgrid/grid.import',
#    'jqgrid/JsonXml',
#    'jqgrid/jquery.searchFilter',
    ],
'slick.grid': [
    'slick.grid',
#    'slick.pager',
    ],
'divineba.chart': [
    'excanvas',
#    'js-class',
#    'bluff-src',
    'highcharts.src',
    'jquery.orgchart.min'
    ]
}

css_files = {
    'global': [
        'global',
        'jquery.orgchart',
        'ui.divineba',
        'ui.jqgrid',
        'ui.datepicker',
        'ui.override',
        'slick.grid',
        'sexycombo',
        'overlay-apple',
        'fullcalendar',
        'production'
    ],
    'sphere': ['sphere'],
    'sphere_lite': ['sphere_lite'],
    'sphere_plus': ['sphere_plus'],
    'prism': ['prism'],
    'lines': ['lines'],
    'centroid': ['centroid'],
    'circle': ['circle'],
}

def reverseDependencies(files):
    rev = {}
    for out, inputs in files.items():
        duplicates = {f: count for f, count in Counter(inputs).iteritems() if count > 1}
        if duplicates:
            repeated = ', '.join('{} repeated {} times'.format(k, v) for k, v in duplicates.iteritems())
            exit('Error: {repeated} in {out}'.format(**locals()))
        rev.update(dict.fromkeys(inputs, out))
    return rev

rev_files = {
    'css': reverseDependencies(css_files),
    'js' : reverseDependencies(js_files)
}

def getProductionFiles(filetype, filename):
    files = js_files if filetype == 'js' else css_files
    try:
        return [filename] if filename in files else [rev_files[filetype][filename]]
    except KeyError:
        return []

def getDevelopmentFiles(filetype, filename):
    files = js_files if filetype == 'js' else css_files
    return files[filename] if filename in files else [filename]
