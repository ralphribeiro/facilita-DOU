import asyncio
from logging import INFO, Logger
from os.path import dirname, abspath, join
from xml.etree.ElementTree import XMLPullParser
from xml.etree import ElementTree

from aiofiles import open as aopen


logger = Logger(__file__)


async def get_bytes_payload(path: str):
    async with aopen(path, 'rb') as bytes_:
        return await bytes_.read()


def parse_and_remove(xml: bytes, path: str) -> ElementTree.Element:
    path_parts = path.split('/')
    parser = XMLPullParser(('start', 'end'))
    parser.feed(xml)
    doc = parser.read_events()
    next(doc)  # Skip the root element

    tag_stack = []
    elem_stack = []
    for event, elem in doc:
        if event == 'start':
            tag_stack.append(elem.tag)
            elem_stack.append(elem)
        elif event == 'end':
            if tag_stack == path_parts:
                yield elem
                elem_stack[-2].remove(elem)
            try:
                tag_stack.pop()
                elem_stack.pop()
            except IndexError:
                pass


async def find_in_xml(filepath: str, xmlpath: str):
    logger.log(INFO, 'Procurando em %s', filepath.split('/')[-1])
    bin_data = await get_bytes_payload(filepath)
    data = parse_and_remove(bin_data, xmlpath)
    return data

# path_ = join(dirname(abspath(__name__)),
#              '2021-02-05-DO3',
#              '530_20210205_13229037.xml')
# xmlpath_ = 'article/body/Texto'


# async def make_tasks():
#     tasks = asyncio.create_task(find_in_xml(path_, xmlpath_))
#     return await tasks


# if __name__ == "__main__":
#     a = asyncio.run(make_tasks())
#     for _ in a:
#         print(_.text)

#     # for pothole in data:
#         # potholes_by_zip[pothole.findtext('[CDATA[')] += 1
#         # print(pothole.findtext('[CDATA['))

#     # for zipcode, num in potholes_by_zip.most_common():
#         # print(zipcode, num)
