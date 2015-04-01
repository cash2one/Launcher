import sys,os,site

_PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

_SITE_PACKAGES_DIR = os.path.sep.join([_PROJECT_DIR, 'venv\lib\site-packages'])
sys.path.insert(0, _SITE_PACKAGES_DIR)
#site.addsitedir(_SITE_PACKAGES_DIR)

sys.path.insert(0, _PROJECT_DIR)
#sys.path.append(_PROJECT_DIR+'\\Launcher')
#sys.path.insert(0, os.path.dirname(_PROJECT_DIR))

os.chdir("D:\\\\works\\\\Launcher2")

from Launcher import app as application