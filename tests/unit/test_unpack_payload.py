from os.path import exists, join
from os import remove
from zipfile import ZipFile

from src.app.payload import unpack_payload


def test_unpack_payload_given_path(temp_dir):
    file_name = 'file.txt'
    path = join(temp_dir, file_name)
    with open(path, 'wb') as f:
        f.write(b'data test')

    path_zip = join(temp_dir, 'file.zip')
    with ZipFile(path_zip, 'x') as z:
        z.write(path, file_name)

    remove(path)
    assert exists(path_zip)
    unpack_payload(path_zip)
    assert exists(path)
