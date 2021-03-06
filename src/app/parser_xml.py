import re
from dataclasses import dataclass
import logging
from os import listdir
from os.path import join as osjoin
from xml.etree.ElementTree import parse


@dataclass(frozen=True)
class ItemXml:
    url: str
    identifica: str
    data: str
    texto: str


TAG_RE = re.compile(r'<[^>]+>')


def remove_tags(text):
    return TAG_RE.sub('', text)


def parse_xml(xml_file_path: str, pattern: tuple):
    logging.info('Procurando em %s', xml_file_path.split('/')[-1])
    doc = parse(xml_file_path)
    root = doc.getroot()
    child = root.find('article')

    url = child.attrib['pdfPage']

    child2 = child.find('body')
    child3 = child2.find('Identifica')
    identifica = child3.text

    if not identifica or not re.findall(
        pattern[0], identifica, flags=re.IGNORECASE
    ):
        return None

    child3 = child2.find('Data')
    data = child3.text

    child3 = child2.find('Texto')
    texto = child3.text

    texto = remove_tags(texto)

    item = ItemXml(url, identifica, data, texto)
    r = re.findall(pattern[1], item.texto, flags=re.IGNORECASE)
    return item if len(r) > 0 else None


def get_items(path: str, pattern: tuple):
    items = set()
    xmls = listdir(path)
    for xml in xmls:
        if xml.endswith('.xml'):
            item = parse_xml(osjoin(path, xml), pattern)
            if item:
                items.add(item)
    return items
