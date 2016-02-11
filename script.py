import sys
import urllib2
import json

# Default filename or from command line
fname = 'log.txt'
if len(sys.argv) > 1:
    fname = sys.argv[1]

with open(fname) as f:
    content = f.readlines()


def get_ip(hash):
    data = urllib2.urlopen("https://onionoo.torproject.org/summary?limit=1&search=" + hash).read()
    result = json.loads(data)
    relays = result['relays'][0]
    ip = relays['a']
    return ip[0]


def save_result(str):
    with open('result.txt', 'a') as result_file:
        result_file.write(str+'\n')

output = ''
middle_relay_ip = ''
for line in content:
    if line[0] != '$':
        arr = line.split(' ')
        year = arr[0]
        month = arr[1]
        day = arr[2]
        entry_relay_ip = get_ip(arr[3])
        output = ','.join([year, month, day, entry_relay_ip])
    else:
        if middle_relay_ip == '':
            middle_relay_ip = get_ip(line[1:])
            output += ',' + middle_relay_ip
        else:
            # It'a a exit_relay_ip
            output += ',' + get_ip(line[1:])
            # Now save the result
            save_result(output)
            output = ''
            middle_relay_ip = ''
