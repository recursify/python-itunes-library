import xml.sax.handler
import xml.sax
import sys
import os

class ArrayItem(list):
    """
    Provides a common interface to add items to list
    """
    def add_item(self, item):
        self.append(item)

class DictItem(dict):
    """
    Provides a commong interface to add items to dict
    """
    def add_key(self, key):
        self.key = key

    def add_item(self, item):
        self[self.key] = item

def null(input):
    return input

class SimpleDataHandler(object, xml.sax.handler.ContentHandler):
    """
    SAX Handler capable of parsing iTunes Libarary XML files.

    After parsing, the final item is accessible through the final_item
    attribute.
    """
    # Mapping of type -> conversion function
    types = {
        'string'  : null, # Not happy with unicode
        'date'    : str,  # Could use strftime...
        'integer' : int   # Convert to int
        }

    def __init__(self):
        self.content = []
        self.stack = []

    @property
    def state_info(self):
        return "Stack: %s Current_item: %s" % (self.stack, self.current_item)

    def startElement(self, name, attrs):
        to_add = None
        if name == 'dict':
            to_add = DictItem()
        elif name == 'array':
            to_add = ArrayItem()

        if to_add is not None:
            self.stack.append(to_add)

    def endElement(self, name):
        if 'key' == name:
            current_key = ''.join(self.content).strip()
            self.content = []
            self.current_item.add_key(current_key)
        elif name in self.types:
            f = self.types[name]
            item = f(''.join(self.content).strip())
            self.content = []
            self.current_item.add_item(item)
        elif name == 'dict' or name == 'array':
            finished = self.stack.pop(-1)
            if self.current_item is not None:
                self.current_item.add_item(finished)
            else:
                self.final_item = finished
        
    def characters(self, content):
        self.content.append(content)

    @property
    def current_item(self):
        return self.stack[-1] if len(self.stack) > 0 else None
