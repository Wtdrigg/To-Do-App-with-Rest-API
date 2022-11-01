from todo_requests import RequestsToDo
from todo_gui import ToDoGUI

""" 
Main file for the todo App. Instantiates a RequestsToDo object from todo_requests.py and then uses it
as a parameter when calling the ToDoGUI class. This is what allows the GUI to send and receive data from the
RequestsToDo Object.
"""

if __name__ == '__main__':
    requests_obj = RequestsToDo()
    ToDoGUI(requests_obj)
