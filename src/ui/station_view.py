from tkinter import ttk, StringVar, constants, Listbox, Scrollbar, Text
from services.station_service import station_service
from database_connection import get_database_connection


class StationView:
    """Station list view."""

    def __init__(self, root, handle_show_weather_view):
        """Class constructoimport Tkinter as tkr. Creates new view for stations.

        Args:
            root:
                TKinter element, in which view is installed.
            handle_ TODO
                Change to another view
        """

        self._root = root
        self._handle_show_weather_view = handle_show_weather_view
        self._frame = None
        self._list_label = None
        self._button_select = None
        self._error_variable = None
        self._error_label = None
        self.textbox = None
        self._label_selection = []

        self._initialize()

    def pack(self):
        """"Shows the view."""
        self._frame.pack(fill=constants.X)

    def destroy(self):
        """"Destroys the view."""
        self._frame.destroy()

    def _show_error(self, message):
        self._error_variable.set(message)

    def _handle_button_click(self):
        selected_values = []

        # TODO: How to handle this error correctly?
        if len(self._list_label.curselection())>2:
            self._error_variable = "Select at maximum 2 stations"
        # TODO For testing now set to 8. Later add this to error handling "Select at least 1"
        if len(self._list_label.curselection()) == 0:
            selected_values.append(8)

        for i in self._list_label.curselection():
            for i in self._list_label.curselection():
                selected_values.append(i)
        print(f"Value of entry is: {selected_values[0]}")

        self._handle_show_weather_view()
        
    def station_list(self):
        """Gets stations from the database and returns them as a list."""
        stations = station_service.get_stations()
        stations_list = []
        for s in stations:
            if s.name != "Name":
                stations_list.append((s.station_id, s.name))
        return stations_list

    def _initialize_station_list_field(self):
        """Creates a view with stations in a listbox"""
        stations_list = self.station_list()

        note_label = ttk.Label(master=self._frame, text="Select 1 station", 
                                  font=('Arial',12,'normal'))
        note_label.grid(column=0, row=3, padx=5, pady=5, sticky=constants.W)

        # TODO: Make multiple selection available
        # TODO: Show selected stations
        self._list_label = Listbox(master=self._frame, selectmode="single", 
        height=10, width=38
        )

        for s in stations_list:
            self._list_label.insert(s[0], s[1])

        self._list_label.grid(column=0, row=4, padx=5, pady=5, sticky=constants.W)

        #Scrollbar
        vertscroll = Scrollbar(master=self._frame)
        vertscroll.config(command=self._list_label.yview)
        self._list_label.config(yscrollcommand=vertscroll.set)
        vertscroll.grid(column=0, row=4, sticky=constants.NS)


    def _initialize(self):
        """Initializes the frame view"""
        self._frame = ttk.Frame(master=self._root)

        station_label = ttk.Label(master=self._frame, text="Station settings", 
                                  font=('Arial',24,'bold'))
        station_label.grid(column=0, row=1, padx=5, pady=5, sticky=constants.W)

        self._error_label = ttk.Label(
            master=self._frame,
            textvariable=self._error_variable,
            foreground="red"
        )

        self._error_label.grid(column=0, row=2, padx=5, pady=5)

        self._initialize_station_list_field()

        select_button = ttk.Button(
            master=self._frame,
            text="Select",
#            command=self._handle_button_click
            command=self._handle_button_click
        )

        select_button.grid(column=0, row=5, padx=5, pady=5, sticky=constants.EW)

        selection_label = ttk.Label(master=self._frame, text=self._label_selection, 
                                  font=('Arial',12,'normal'))
        selection_label.grid(column=0, row=6, padx=5, pady=5, sticky=constants.W)

        self._frame.grid_columnconfigure(0, weight=1, minsize=400)


print("STATIONVIEW\n")