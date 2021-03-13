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


def get_bytes_payload(path: str):
    with open(path, 'rb') as bytes_:
        return bytes_.read()


TAG_RE = re.compile(r'<[^>]+>')


def remove_tags(text):
    return TAG_RE.sub('', text)


def parse_and_remove(xml_file_path: str):
    doc = parse(xml_file_path)
    root = doc.getroot()
    child = root.find('article')

    url = child.attrib['pdfPage']

    child2 = child.find('body')
    child3 = child2.find('Identifica')
    identifica = child3.text.strip()

    child3 = child2.find('Data')
    data = child3.text.strip()

    child3 = child2.find('Texto')
    texto = child3.text.strip()

    print(remove_tags(texto).strip('\n\n'))
    # item = ItemXml(url, identifica, data, texto)

    
    # print(item)

# def parse_and_remove(xml: bytes, path: str) -> ElementTree.Element:
#     path_parts = path.split('/')
#     parser = XMLPullParser(('start', 'end'))
#     parser.feed(xml)
#     doc = parser.read_events()
#     next(doc)  # Skip the root element

#     tag_stack = []
#     elem_stack = []
#     for event, elem in doc:
#         if event == 'start':
#             tag_stack.append(elem.tag)
#             elem_stack.append(elem)
#         elif event == 'end':
#             if tag_stack == path_parts:
#                 yield elem
#                 elem_stack[-2].remove(elem)
#             try:
#                 tag_stack.pop()
#                 elem_stack.pop()
#             except IndexError:
#                 pass


def find_in_xml(filepath: str, xmlpath: str):
    logging.info('Procurando em %s', filepath.split('/')[-1])
    bin_data = get_bytes_payload(filepath)
    data = parse_and_remove(bin_data, xmlpath)

    return data
