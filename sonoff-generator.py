import csv
import sys

from itertools import zip_longest

items = []

data = list(csv.reader(open(sys.argv[1], 'r')))
for row in data[1:]:
    pin, s, inverted = row
    if not s:
        continue
    if s == 'TX':
        s = '``TX`` pin (for external sensors)'
    if s == 'RX':
        s = '``RX`` pin (for external sensors)'
    if inverted and inverted.lower() in ('yes', 'true', '1'):
        s += ' (inverted)'
    items.append({
      'pin': pin,
      'function': s
    })

TABLE_ITEM_LENGTH = 50
TABLE_COLUMNS = 2


def create_row_str(type):
    return '    ' + ' '.join([(type * TABLE_ITEM_LENGTH) for _ in range(TABLE_COLUMNS)])


print('.. table::')
print('    :class: no-center')
print()
print(create_row_str('='))
prev_row = False

for value in items:
    col1 = '``{}``'.format(value['pin']).ljust(TABLE_ITEM_LENGTH)
    if prev_row:
        print(create_row_str('-'))
    prev_row = True
    print("    {} {}".format(col1, value['function']))

print(create_row_str('='))
