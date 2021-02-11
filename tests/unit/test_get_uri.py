from datetime import date

import pytest

from src.app.config import get_uri

def test_get_uri_given_date_and_name():
    today = date.today().isoformat()
    name = 'DO3'
    expected = f'https://inlabs.in.gov.br/index.php?p={today}&dl={today}-{name}.zip'
    assert get_uri(today, name) == expected
    