__author__ = 'tmkasun'
import re

ip_pattern = re.compile(
    r"((2[0-4][0-9])|(25[0-5])|([10]?[0-9]?[0-9]))\.((2[0-4][0-9])|(25[0-5])|([10]?[0-9]?[0-9]))\.((2[0-4][0-9])|(25[0-5])|([10]?[0-9]?[0-9]))\.((2[0-4][0-9])|(25[0-5])|([10]?[0-9]?[0-9]))")

with open('./ip_list') as ip_list:
    for entry in ip_list:
        if entry[0] == '#':
            continue
        entry_match = ip_pattern.match(entry)
        if entry_match:
            print("DEBUG: Valid IP address: {}".format(entry_match.group()))
        else:
            print("DEBUG: Invalid IP address: {}".format(entry))

ip_list.close()
