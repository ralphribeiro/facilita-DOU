import pytest

from src.app.parser_xml import get_bytes_payload, find_in_xml


@pytest.mark.asyncio
async def test_must_return_bytes_from_file(files):
    for f in files:
        assert await get_bytes_payload(f[0]) == f[1]


@pytest.mark.asyncio
async def test_find_in_xml_return_text(files):
    for f in files:
        r = await find_in_xml(f[0], 'root/child1')
        r = next(r)
        assert r.text == 'test'
        assert r.tag == 'child1'
