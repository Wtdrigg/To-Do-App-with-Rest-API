# To-Do-App-with-Rest-API
A simple app for saving a personal to do list.

This is an app for keeping track of a personal to do list. It consists of a GUI frontend made using Tkinter, and a REST API backend made using Flask and SqlAlchemy.

Any text that is added to the to do list on the GUI is then sent via an HTTP request to a REST API being hosted at http://wtdrigg.pythonanywhere.com/todo. This API receives the HTTP request along with its data payload and has the data added to a small SQLAlchemy database. The database information is then read from and sent back to the GUI to be displayed in the main listbox.

--GUI--
The GUI code and documentation can be found in todo_gui.py and consists of a listbox, an entrybox, and two buttons. The GUI automatically sends a GET request to the API when being opened, which is used to populate the listbox with any data that was sent to the API prior. It will send both a PUT request and another GET request whenever the SUBMIT button is clicked, which sends any data the user typed into the entrybox to the API, and then refreshes the listbox accordingly. The DELETE button will send a PATCH request when clicked, which removes the selected listbox item from the database.

--REQUESTS--
The GUI makes use of several HTTP requests, the code and documentation for which can be found in todo_requests.py. All data is sent and received in JSON format.

--API--
The HTTP requests go to a REST API that is hosted by PythonAnywhere at the URI: http://wtdrigg.pythonanywhere.com/todo. This API stores data sent buy the GUI into a SQLAlchemy database. It then reads from this database to return the data to be displayed on the GUI. The database can currently store up to a 99 rows of data. The code and documentation for the API can be found in todo_api.py.

--Instructions--
This is currently setup to work by simply running either main.py or main.pyw, which will instatiate the GUI, then send a GET request to http://wtdrigg.pythonanywhere.com/todo, and finally display the data that it recieves. If you wish to run this without connecting to PythonAnywhere then simply update the URL in line 14 of todo_requests.py to be localhost ('http://127.0.0.1:5000'). You will also need to uncomment the app.run() and db.create_all() methods from bottom of todo_api.py, and then run the file. Doing this will both create a new database and run the API locally, effectivly having your machine send a receive HTTP requests from iteself.
