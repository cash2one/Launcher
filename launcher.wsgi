import sys,os,site

_PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

_VENV_PATH = os.path.sep.join([os.environ('USERPROFILE'), 'Envs', 'launcher'])

_SITE_PACKAGES_DIR = os.path.sep.join([_VENV_PATH, 'lib', 'site-packages'])
sys.path.insert(0, _SITE_PACKAGES_DIR)
#site.addsitedir(_SITE_PACKAGES_DIR)

sys.path.insert(0, _PROJECT_DIR)
#sys.path.append(_PROJECT_DIR+'\\Launcher')
#sys.path.insert(0, os.path.dirname(_PROJECT_DIR))

os.chdir("D:\\\\works\\\\Launcher2")

from Launcher import app as application