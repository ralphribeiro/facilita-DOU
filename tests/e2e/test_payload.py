from datetime import date
from os.path import join, exists

import pytest

from src.app.payload import get_payload, GetPayloadError
from src.app.config import AUTH, get_uri


today = date.today().isoformat()


def test_payload_with_valid_dirpath(temp_dir):
    num_do = 'DO3'
    path = join(temp_dir, f'{today}-{num_do}.zip')
    url = get_uri(today, num_do)
    res = get_payload(path, url, AUTH)
    assert res[0] in (200, 201)
    assert exists(path)


def test_payload_raise_exception_with_not_valid_dirpath():
    num_do = 'DO3'
    path = 'invalid-path'
    url = get_uri(today, num_do)
    with pytest.raises(GetPayloadError, match='Diretório inválido') as e:
        get_payload(path, url, AUTH)
