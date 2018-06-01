import csv
import sys

from itertools import zip_longest

items = []

data = list(csv.reader(open(sys.argv[1], 'r')))
for row in data:
    name, page, image = row
    items.append({
      'name': name.strip(),
      'link': '/esphomeyaml/{}.html'.format(page.strip()),
      'image': '/esphomeyaml/images/{}'.format(image.strip()),
    })

TABLE_ITEM_LENGTH = 50
TABLE_COLUMNS = 3


def create_row_str(type):
    return ' '.join([(type * TABLE_ITEM_LENGTH) for _ in range(TABLE_COLUMNS)])


# https://stackoverflow.com/a/3415150/8924614
def grouper(n, iterable, fillvalue=None):
    """grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"""
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)

print(create_row_str('='))
prev_row = False

for value in grouper(TABLE_COLUMNS, items):
    row1 = []
    row2 = []
    for x in value:
        if x is None:
            continue
        row1.append('|{}|_'.format(x['name']).ljust(TABLE_ITEM_LENGTH))
        row2.append('`{}`_'.format(x['name']).ljust(TABLE_ITEM_LENGTH))
    if prev_row:
        print(create_row_str('-'))
    prev_row = True
    print(' '.join(row1).rstrip())
    print(create_row_str('-'))
    print(' '.join(row2).rstrip())

print(create_row_str('='))
print()

for item in items:
    print('.. |{}| image:: {}'.format(item['name'], item['image']))
    print('    :class: component-image')
    print('.. _{}: {}'.format(item['name'], item['link']))

print()
