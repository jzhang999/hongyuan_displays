import sys
import site

python_home = '/var/www/hongyuan_displays/venv/'

site.addsitedir('/var/www/hongyuan_displays/venv/lib/python3.8/site-packages')

sys.path.insert(0, '/var/www/hongyuan_displays')

from flaskr import app as application
