from datetime import date
from os.path import join
from random import randbytes, randint
import tempfile

from pytest import fixture


@fixture
def temp_dir():
    td = tempfile.TemporaryDirectory(suffix=date.today().isoformat())
    yield td.name
    td.cleanup()


@fixture
def files(temp_dir):
    ret = []
    for i in range(2):
        name = join(temp_dir, f'i{i}.xml')
        with open(name, 'wb') as tf:
            b = b'<xml><root><child1>test</child1></root></xml>'
            # rand_b = randbytes(randint(10, 11))
            tf.write(b)
        ret.append((name, b))
    return ret
