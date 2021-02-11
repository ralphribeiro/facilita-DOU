from datetime import date
from os.path import join
from os import listdir
import tempfile

from src.app.config import AUTH, get_uri
from src.app.payload import get_payload, unpack_payload
from src.app.parser_xml import find_in_xml


today = date.today().isoformat()


def prepare_files(dir_path):
    num_do = 'DO3'
    path = join(dir_path, f'{today}-{num_do}.zip')
    url = get_uri(today, num_do)
    get_payload(path, url, AUTH)
    unpack_payload(path)


def main():
    td = tempfile.TemporaryDirectory(suffix=today)
    xmlpath = 'article/body/Identifica'
    try:
        prepare_files(td.name)
        xmls = listdir(td.name)
        for xml in xmls:
            if xml.endswith('.xml'):
                resp = find_in_xml(join(td.name, xml), xmlpath)
                print(resp.text)
    finally:
        td.cleanup()
