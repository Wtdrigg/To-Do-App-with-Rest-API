import requests

"""
This file is used to send http requests to the todo API, which will process the requests accordingly.
"""

class RequestsToDo:

    # Constructor stores the API's URI as a class attribute
    def __init__(self):
        self.url = 'http://127.0.0.1:5000/todo'

    # Takes a provided integer and string and converts them into JSON format. The JSON data is then 
    # sent in a put request to the API, and will be added to the database.
    def api_put_request(self, list_id, todo_text):
        result = requests.put(self.url, {'id': list_id, 'todo': todo_text})

    # Sends a get request to the API. Data that the API sends back is then returned in JSON format.
    def api_get_request(self):
        result = requests.get(self.url)
        result_json = result.json()
        return result_json

    # Takes a provided integer and converts it to JSON format. The JSON data is then sent in a
    # patch request to the API, and is used to determine which database item is modified.
    def api_patch_request(self, list_id):
        result = requests.patch(self.url, {'id': list_id})