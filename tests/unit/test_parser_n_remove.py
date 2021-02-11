from xml.etree.ElementTree import Element

from src.app.parser_xml import parse_and_remove


def test_find_in_xml_given_bytes():
    xml = b'<xml><root><child1>test</child1></root></xml>'
    response = parse_and_remove(xml, 'root/child1')
    response = next(response)
    assert isinstance(response, Element)
    assert response.tag == 'child1'
    assert response.text == 'test'