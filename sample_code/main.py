# my_module/main.py

# The 'cgi' module is deprecated and its use should be flagged by pylint.
import cgi
import os
from .utils import useful_function

class WebHandler:
    """
    A sample class that uses a deprecated module for handling web data.
    """
    def __init__(self, query_string):
        self.query_string = query_string

    def get_field(self, field_name):
        """
        Parses a query string to get a specific field.
        This uses the deprecated 'cgi.parse_qs' function.
        """
        parsed_data = cgi.parse_qs(self.query_string)
        return parsed_data.get(field_name, [None])[0]

def run_main_logic():
    """
    Main logic of the script.
    """
    print("Starting main application.")
    useful_function()

    handler = WebHandler("user=test&action=submit")
    user = handler.get_field("user")

    print(f"Username from query string: {user}")

if __name__ == "__main__":
    run_main_logic()