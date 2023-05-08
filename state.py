import json

class State:
    def __init__(self, file):
        self.file = file
    
    def simplify(self, object):
        simplified = {}
        for museum in object:
            simplified[museum] = {}
            for library in object[museum]['available']:
                simplified[museum][library] = len(object[museum]['available'][library])
        return simplified
    
    def save(self, object):
        simplified = self.simplify(object)
        with open(self.file, 'w') as fd:
            json.dump(simplified, fd)

    def load(self):
        try:
            with open(self.file, 'r') as fd:
                simplified = json.load(fd)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            return {}
        return simplified
    
    def compare(self, object):
        simplified = self.simplify(object)
        stored = self.load()
        if simplified == stored:
            return True
        return False