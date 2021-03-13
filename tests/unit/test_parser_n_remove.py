from os.path import dirname, join
from xml.etree.ElementTree import Element

from src.app.parser_xml import parse_and_remove


def get_xml_file_path():
    return join(dirname(__file__), 'parser_data_test.xml')


def test_find_in_xml_given_bytes():
    xml = get_xml_file_path()
    response = parse_and_remove(xml)
    # # response = next(response)
    # assert isinstance(response, Element)
    # assert response.tag == 'xml'
    # assert response.text == 'test'
