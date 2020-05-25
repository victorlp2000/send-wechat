import sys

import json_file

def getContacts():
    # default contacts
    contacts = ['File Transfer']
    if len(sys.argv) > 1:
        tmp = json_file.readFile(sys.argv[1])
        if type(tmp) is list:
            contacts = tmp
    return contacts
