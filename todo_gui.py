import tkinter as tk

"""
This file contains all of the classes and methods used to build the todo app GUI.
"""

class ToDoGUI:

    # Constructor builds all required objects and sets the root object parameters.
    def __init__(self, todo_obj):
        self.todo_obj = todo_obj
        self.root = tk.Tk()
        self.root.geometry('400x500')
        self.root.title('My To-Do List')
        self.root.resizable(height='False', width='False')
        self.frames = ToDoFrames(self)
        self.list = ToDoList(self)
        self.entry = ToDoEntryBox(self)
        self.labels = ToDoLabels(self)
        self.buttons = ToDoButtons(self)
        self.buttons.refresh()
        self.root.mainloop()
    
class ToDoFrames:

    # Constructor builds the upper and lower frame widgets and places them within the root.
    def __init__(self, gui_obj):
        self.gui_obj = gui_obj
        self.upper_frame = tk.Frame(self.gui_obj.root, bd=5)
        self.upper_frame.place(anchor='nw', width=400, height=300, x=0, y=0)
        self.lower_frame = tk.Frame(self.gui_obj.root, bd=5)
        self.lower_frame.place(anchor='nw', width=400, height=200, x=0, y=300)

class ToDoList:

    # Constructor builds the listbox widget and places it within the upper frame.
    def __init__(self, gui_obj):
        self.gui_obj = gui_obj
        self.todo_list = tk.Listbox(self.gui_obj.frames.upper_frame, height=200, width=200)
        self.todo_list.place(anchor='nw', width=390, height=275, x=0, y=25)

class ToDoEntryBox:

    # Constructor builds the entrybox widget and places it within the lower frame.
    def __init__(self, gui_obj):
        self.gui_obj = gui_obj
        self.entry_box = tk.Entry(self.gui_obj.frames.lower_frame, width=25)
        self.entry_box.place(anchor='sw', x=25, y=100)

class ToDoLabels:

    # Constructor builds the label widgets and places them within the upper and lower frames.
    def __init__(self, gui_obj):
        self.gui_obj = gui_obj
        self.entry_label = tk.Label(self.gui_obj.frames.lower_frame, text='I need to:')
        self.entry_label.place(anchor='sw', x=75, y=80)
        self.list_label = tk.Label(self.gui_obj.frames.upper_frame, text='My To-Do List')
        self.list_label.place(anchor='n', x=195, y=0)

class ToDoButtons:

    # Constructor builds the button widgets and places them within the upper and lower frames.
    def __init__(self, gui_obj):
        self.gui_obj =gui_obj
        self.submit_button = tk.Button(self.gui_obj.frames.lower_frame, text='SUBMIT', height=1, width=10, command=self.press_submit)
        self.submit_button.place(anchor='sw', x=225, y=102)
        self.delete_button = tk.Button(self.gui_obj.frames.lower_frame, text= 'DELETE', height=1, width=10, command=self.press_delete)
        self.delete_button.place(anchor='sw', x=225, y=142)

    # function is called with the submit button is clicked. This determines and saves the lowest unused ID number, and also
    # saves the data in the entry box. This info is then sent to the API via put request, which will save it to the database.
    def press_submit(self):
        todo_text = self.gui_obj.entry.entry_box.get()
        if len(todo_text) != 0:
            list_size = self.gui_obj.list.todo_list.size()
            ordered_bool = True
            if list_size != 0:
                for i in range(list_size):
                    line = self.gui_obj.list.todo_list.get(i)
                    if int(line[0]) == i + 1:
                        continue
                    else:
                        list_id = i + 1
                        ordered_bool = False
                        break
                if ordered_bool:
                    list_id = list_size + 1
                else:
                    ordered_bool = True
            else:
                list_id = 1
            self.gui_obj.entry.entry_box.delete(0, 'end')
            self.gui_obj.todo_obj.api_put_request(list_id, todo_text)
            self.refresh()
        else:
            pass

    # Takes the data from a selected item in the listbox and sends that data to the API via patch request, which will
    # have that data removed from the database.
    def press_delete(self):
        lines_selected = self.gui_obj.list.todo_list.curselection()
        for item in lines_selected:
            line_text = self.gui_obj.list.todo_list.get(item)
            delete_id = line_text[0]
            self.gui_obj.todo_obj.api_patch_request(delete_id)
        self.refresh()
    
    # Sends a get request to the API, and updates the lisbox to display the data that is recieved.
    def refresh(self):
        list_size = self.gui_obj.list.todo_list.size()
        self.gui_obj.list.todo_list.delete(0, list_size)
        todo_json = self.gui_obj.todo_obj.api_get_request()
        for item in todo_json:
            self.gui_obj.list.todo_list.insert(item['id'], str(item['id']) + ' - ' + item['todo'])
