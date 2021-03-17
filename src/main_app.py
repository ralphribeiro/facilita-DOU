from datetime import date
import logging
from os.path import join
import tempfile

from app.config import AUTH, get_uri
from app.payload import get_payload, unpack_payload
from app.parser_xml import get_items


logging.getLogger().setLevel(logging.INFO)
today = date.today().isoformat()


def main():
    td = tempfile.TemporaryDirectory(prefix='facdou', suffix=today)

    num_do = 'DO3'
    path = join(td.name, f'{today}-{num_do}.zip')
    url = get_uri(today, num_do)

    get_payload(path, url, AUTH)
    unpack_payload(path)

    pattern = ('licitação', 'saúde')

    items = get_items(td.name, pattern)
    print(len(items))


if __name__ == "__main__":
    main()
