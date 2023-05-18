import json
from deepdiff import DeepDiff, Delta, extract
import re


def find_diff(old, new):
    output = {}

    for museum in new:
        museum_output = {}
        diff_dict = DeepDiff(old[museum], new[museum])
        if 'dictionary_item_added' in diff_dict:
            for item in diff_dict['dictionary_item_added']:
                extracted_item = extract(new[museum], item)
                extracted_key = re.findall("\['([^']*)'\]", item)
                museum_output[extracted_key[0]] = extracted_item

        if 'dictionary_item_removed' in diff_dict:
            for item in diff_dict['dictionary_item_removed']:
                extracted_item = extract(old[museum], item)
                extracted_key = re.findall("\['([^']*)'\]", item)
                museum_output[extracted_key[0]] = 0 - extracted_item

        if 'values_changed' in diff_dict:
            for item in diff_dict['values_changed']:
                extracted_item_new = extract(new[museum], item)
                extracted_item_old = extract(old[museum], item)
                extracted_key = re.findall("\['([^']*)'\]", item)
                museum_output[extracted_key[0]] = extracted_item_new - extracted_item_old

        if len(museum_output) > 0:
            output[museum] = museum_output


    if len(output) > 0:
        return True, output
    return False, {}

def simplify(object):
    simplified = {}
    for museum in object:
        simplified[museum] = {}
        for library in object[museum]['available']:
            simplified[museum][library] = len(object[museum]['available'][library])
    return simplified

class State:
    def __init__(self, file):
        self.file = file

    def load(self):
        try:
            with open(self.file, 'r') as fd:
                simplified = json.load(fd)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            return {}
        return simplified

    def save(self, object):
        simplified = simplify(object)
        with open(self.file, 'w') as fd:
            json.dump(simplified, fd)
    
    def has_changes(self, object):
        simplified = simplify(object)
        stored = self.load()

        existing_museums = set(stored.keys())
        new_museums = set(simplified.keys())
        added = new_museums - existing_museums
        removed = existing_museums - new_museums

        for key in added:
            stored[key] = {}
        for key in removed:
            simplified[key] = {}

        return find_diff(stored, simplified)
