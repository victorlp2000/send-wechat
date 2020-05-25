import sys

import json_file

def getContacts():
    # default contacts
    contacts = ['test']
    if len(sys.argv) > 1:
        tmp = json_file.readFile(sys.argv[1])
        if type(tmp) is list:
            contacts = tmp
    return contacts
