from cpl_adapter import CPLAdapter
from notify import Notify
from state import State
import yaml


def style_removed_row():
    return "background-color:#FAA0A0;text-decoration:line-through;"

def style_added_row():
    return "background-color:#C1E1C1;font-weight:bold;"

def prepare_html(availability, diff):
    output = ""

    output += f"<h2>There have been changes in the passes availability</h2>"

    output += "<h4>Current Availability</h4>\n"
    output += "<table>\n"
    output += "<tr><th>Museum</th><th>Library</th><th>Availability</th></tr>\n"
    for museum in availability:
        for library in availability[museum]['available']:
            ## Check if it's new
            style = ""
            if museum in diff:
                if library in diff[museum]:
                    if diff[museum][library] > 0:
                        style = style_added_row()
                        del(diff[museum][library])
            available = len(availability[museum]['available'][library])
            total = len(availability[museum]['all'][library])
            output += f'<tr style="{style}"><td>{museum}</td><td>{library}</td><td>{available}/{total}</td></tr>\n'
        for library in diff[museum]:
            style = style_removed_row()
            available = 0
            total = len(availability[museum]['all'][library])
            output += f'<tr style="{style}"><td>{museum}</td><td>{library}</td><td>{available}/{total}</td></tr>\n'
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

    has_changes, diff = state.has_changes(availability)
    if has_changes:
        print("Changes detected, sending email")    
        html_content = prepare_html(availability, diff)
        notify = Notify(user_config["email"])
        notify.send_email("There has been a change in availability", html_content)
    else:
        print("No changes detected, not sending email")
    state.save(availability)

if __name__ == "__main__":
    main()