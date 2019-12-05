from subprocess import Popen, PIPE
import os


def vuetify(src):
    try:
        ps = Popen(['vue-beautify'], stdin=PIPE, stdout=PIPE)
        stdout, stderr = ps.communicate(src.encode('utf-8'))
        if ps.wait() == 0:
            return stdout.decode('utf-8')
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        return src


def run(cmd):
    return os.system(cmd) == 0


def fail(cmd, msg=None):
    if not run(cmd):
        raise OSError('Failed to run {}'.format(cmd) if msg is None else msg)
    return True
