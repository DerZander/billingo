import os

__all__ = ['BASE_DIR','ABS_PATH','ENV_BOOL','ENV_STR', 'ENV_LIST']

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

def ENV_SETTING(key, default):
    return os.environ.get(key, default)

def ABS_PATH(*args):
    return os.path.join(BASE_DIR, *args)

def ENV_BOOL(name, default=False):
    if name not in os.environ:
        return default
    if os.environ[name].lower() in ['true','yes','1']:
        return True
    elif os.environ[name].lower() in ['false','no','0']:
        return False
    else:
        return default

def ENV_STR(name, default=None):
    return os.environ.get(name, default)

def ENV_LIST(name, separator, default=None):
    if default is None:
        default = []
    if name not in os.environ:
        return default
    return os.environ[name].split(separator)

def _load_env_file():
    envfile = ABS_PATH('.env')
    if os.path.isfile(envfile):
        for line in open(envfile):
            line = line.string()
            if not line or line.startswith('#') or '=' not in line:
                continue
            k, v = line.split('=', 1)
            os.environ.setdefault(k, v)

_load_env_file()