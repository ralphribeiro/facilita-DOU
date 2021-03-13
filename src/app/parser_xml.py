import re
from typing import Any
from dataclasses import dataclass
from html.parser import HTMLParser
import logging
from xml.etree.ElementTree import XMLPullParser, parse, fromstring


@dataclass()
class ItemXml:
    url: str
    identifica: str
    data: str
    texto: str


TAG_RE = re.compile(r'<[^>]+>')


def remove_tags(text):
    return TAG_RE.sub('', text)


def parse_xml(xml_file_path: str, pattern: str):
    logging.info('Procurando em %s', xml_file_path.split('/')[-1])
    doc = parse(xml_file_path)
    root = doc.getroot()
    child = root.find('article')

    url = child.attrib['pdfPage']

    child2 = child.find('body')
    child3 = child2.find('Identifica')
    identifica = child3.text

    child3 = child2.find('Data')
    data = child3.text

    child3 = child2.find('Texto')
    texto = child3.text

    texto = remove_tags(texto)

    item = ItemXml(url, identifica, data, texto)
    r = re.findall(pattern, item.texto, flags=re.IGNORECASE)
    return item if len(r) > 0 else None
        
