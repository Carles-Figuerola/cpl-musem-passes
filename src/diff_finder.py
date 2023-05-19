from notify import Notify
from state import State
from threading import Thread


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
        if museum in diff:
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

class DiffFinder():
    def __init__(self,logger, adapter, config, data_folder):
        self.logger = logger
        self.config = config
        self.data_folder = data_folder
        self.adapter = adapter

        self.states = {}
        for each_user_config in config['configs']:
            self.states[each_user_config['name']] = State(f"{self.data_folder}/{each_user_config['name']}-state.json")
        a = True

    def run(self):
        thread = Thread(target=self.diff_and_notify)
        thread.start()

    def diff(self, user_config):
        config_name = user_config['name']
        library_list = user_config["libraries"]
        museum_list = user_config["museums"]

        availability = {}
        for museum in museum_list:
            availability[museum] = self.adapter.get_pass_availability(museum, libraries=library_list)
        has_changes, diff = self.states[config_name].has_changes(availability)

        return availability, has_changes, diff

    def diff_and_return_for_user(self, user):
        for each_user_config in self.config['configs']:
            if each_user_config['name'] == user:
                user_config = each_user_config

        availability, _, _ = self.diff(user_config)
        return availability

    def diff_and_notify(self):
        for each_user_config in self.config['configs']:
            availability, has_changes, diff = self.diff(each_user_config)
        
            if has_changes:
                self.logger.info("Changes detected, sending email")    
                html_content = prepare_html(availability, diff)
                notify = Notify(self.config["email"])
                notify.send_email(each_user_config["email"], "There has been a change in availability", html_content)
            else:
                self.logger.info("No changes detected, not sending email")
            self.states[each_user_config['name']].save(availability)

if __name__ == "__main__":
    DiffFinder(None).run()