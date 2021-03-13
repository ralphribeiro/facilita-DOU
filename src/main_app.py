from datetime import date
import logging
from os.path import join
from os import listdir
import tempfile

from app.config import AUTH, get_uri
from app.payload import get_payload, unpack_payload
from app.parser_xml import find_in_xml

import xml.etree.ElementTree as elem

logging.getLogger().setLevel(logging.INFO)

today = date.today().isoformat()


def prepare_files(dir_path):
    num_do = 'DO3'
    path = join(dir_path, f'{today}-{num_do}.zip')
    url = get_uri(today, num_do)
    get_payload(path, url, AUTH)
    unpack_payload(path)


def get_xmlpath():
    return 'article/body/Texto'


def main():
    td = tempfile.TemporaryDirectory(prefix='facdou', suffix=today)
    xmlpath = get_xmlpath()
    prepare_files(td.name)
    xmls = listdir(td.name)
    for xml in xmls:
        if xml.endswith('.xml'):
            resp: elem.Element = find_in_xml(join(td.name, xml), xmlpath)
            a = 1
            # print(resp.text)p 


if __name__ == "__main__":
    main()
