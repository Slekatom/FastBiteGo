import os
import sys

# путь к проекту
path = '/home/FastBiteGo/FastBiteGo'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'FastBiteGo.settings'

# активировать виртуальное окружение
activate_env = '/home/FastBiteGo/FastBiteGo/venv/bin/activate_this.py'
with open(activate_env) as file_:
    exec(file_.read(), dict(__file__=activate_env))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
