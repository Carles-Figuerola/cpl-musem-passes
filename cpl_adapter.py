import requests
import yaml

class CPLAdapter:
    def __init__(self, cpl_config):
        with open(cpl_config, 'r') as fd:
            content = yaml.safe_load(fd)

        self.museums = content["museums"]
        self.url = content["libraryRecord"]["url"]


    def get_pass_availability(self, museum, libraries):
        print(f'Getting url: {self.url}{self.museums[museum]}/availability')
        response = requests.get(f'{self.url}/{self.museums[museum]}/availability')
        if response.ok:
            availability = response.json()["entities"]["bibItems"]
        else:
            return {"error": True, "message": f"Got failed response from the library api: {response.content}"}
        
        items = {}
        items['all'] = {}
        items['available'] = {}
        for key in availability:
            if availability[key]["branch"]["name"] in libraries:
                avail_obj = availability[key]
                lib_name = availability[key]["branch"]["name"]

                # fill the 'all' key
                if not lib_name in items['all']:
                    items['all'][lib_name] = []
                items['all'][lib_name].append(avail_obj)

                # fill the 'available' key
                if avail_obj["availability"]["status"] == "AVAILABLE":
                    if not lib_name in items['available']:
                        items['available'][lib_name] = []
                    items['available'][lib_name].append(avail_obj)

        return items


