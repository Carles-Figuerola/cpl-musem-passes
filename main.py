from cpl_adapter import CPLAdapter
from notify import Notify
from state import State
import yaml

def prepare_html(availability):
    output = ""
    output += "<h4>Current Availability</h4>\n"
    output += "<table>\n"
    output += "<tr><th>Museum</th><th>Library</th><th>Availability</th></tr>\n"
    for museum in availability:
        for library in availability[museum]['available']:
            available = len(availability[museum]['available'][library])
            total = len(availability[museum]['all'][library])
            output += f"<tr><td>{museum}</td><td>{library}</td><td>{available}/{total}</td></tr>\n"
    output += "</table><br>\n"

    output += "<h4>Passes being tracked</h4>\n"
    output += "<table>\n"
    output += "<tr><th>Museum</th><th>Library</th><th>Status</th></tr>\n"
    for museum in availability:
        for library in availability[museum]['all']:
            for each_pass in availability[museum]['all'][library]:
                if each_pass['availability']['status'] == "AVAILABLE":
                    output += f"<tr><td>{museum}</td><td>{library}</td><td>Available</td></tr>\n"
                elif "dueDate" in each_pass:
                    output += f"<tr><td>{museum}</td><td>{library}</td><td>Due: {each_pass['dueDate']}</td></tr>\n"
                else:
                    output += f"<tr><td>{museum}</td><td>{library}</td><td>Unknown</td></tr>\n"
            

    return output     

def main():
    config_file = "config/cpl.yaml"
    adapter = CPLAdapter(config_file)
    state = State('data/state.json')

    with open('data/config.yaml', 'r') as fd:
        user_config = yaml.safe_load(fd)

    library_list = user_config["libraries"]
    museum_list = user_config["museums"]

    availability = {}
    for museum in museum_list:
        availability[museum] = adapter.get_pass_availability(museum, libraries=library_list)

    if not state.compare(availability):
        print("Changes detected, sending email")    
        html_content = prepare_html(availability)
        notify = Notify(user_config["email"])
        notify.send_email("There has been a change in availability", html_content)
    else:
        print("No changes detected, not sending email")
    state.save(availability)

if __name__ == "__main__":
    main()