from os.path import dirname, join
from xml.etree.ElementTree import Element

from src.app.parser_xml import parse_xml


def get_xml_file_path():
    return join(dirname(__file__), 'parser_data_test.xml')


def test_find_in_xml_given_path():
    xml = get_xml_file_path()
    response = parse_xml(xml, 'saúde')
    assert response
    assert response.url
