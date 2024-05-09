from tkinter import ttk, constants, Listbox, Scrollbar
from services.station_service import station_service


class StationListView:
    """Station list view."""

    def __init__(self, root, handle_show_settings_view):
        """Class constructoimport Tkinter as tkr. Creates new view for stations.

        Args:
            root:
                TKinter element, in which view is installed.
            handle_button_click:
                Save selection to the database and change to station settigns view
        """

        self._root = root
        self._handle_show_settings_view = handle_show_settings_view
        self._frame = None
        self._list_label = None
        self._button_select = None
        self._error_variable = None
        self.stations = station_service.get_stations()
        self._error_label = ttk.Label(master=self._frame)
        self.selected_label = ttk.Label(master=self._frame)
        self._list_label = Listbox(master=self._frame)
        self._vertscroll = Scrollbar(master=self._frame)
        self.continue_button = ttk.Button(master=self._frame)
        self._initialize()

    def pack(self):
        """"Shows the view."""
        self._frame.pack(fill=constants.X)

    def destroy(self):
        """"Destroys the view."""
        self._frame.destroy()

    # Initialize fields and buttons

    def _initialize_error_msg(self):
        """"Field for error message."""
        self._error_label.destroy()
        self._error_label = ttk.Label(
            master=self._frame,
            text=self._error_variable,
            foreground="red"
        )
        self._error_label.grid(column=0, row=1, columnspan=3)

    def _initialize_stations_list(self):
        """"Listbox for stations to select."""
        self._list_label.destroy()
        stations_list = self.stations

        self._list_label = Listbox(
            master=self._frame, selectmode="single", width=28)

        # TODO without this line selected id:s are off +1 - WHY?
        self._list_label.insert(0, "")

        for s in stations_list:
            self._list_label.insert(s.station_id, s.name)

        self._list_label.grid(column=0, row=3, columnspan=2, rowspan=2,
                              padx=10, pady=10, sticky=constants.W)

        # Scrollbar
        self._vertscroll.destroy()
        self._vertscroll = Scrollbar(master=self._frame)
        self._vertscroll.config(command=self._list_label.yview)
        self._list_label.config(yscrollcommand=self._vertscroll.set)
        self._vertscroll.grid(column=1, row=3, columnspan=2, rowspan=2,
                              sticky=constants.NS)

    def _check_selected_count(self):
        if station_service.count_selected() > 5:
            self._error_variable = "At maximum 5 stations can be selected."
            self._initialize_error_msg()
            self.select_button.config(state="disabled")
            self.continue_button.config(state="disabled")
            return False
        elif station_service.count_selected() < 1:
            self._error_variable = "Select at least 1."
            self._initialize_error_msg()
            self.continue_button.config(state="disabled")
            return False
        else:
            self.select_button.config(state="normal")
            return True

    def _initialize_selected(self):
        self.selected_label.destroy()
        list_of_selected = self._get_selected_list()
        self.selected_label = ttk.Label(master=self._frame, text=list_of_selected,
                                        font=('Arial', 12, 'normal'))
        self.selected_label.grid(column=3, row=3, columnspan=2, rowspan=2,
                                 padx=10, pady=10, sticky=constants.NW)

        self._check_selected_count()

    def _initialize_continue_to_settings(self):
        """"Field for continue button."""
        self.continue_button.destroy()
        self.continue_button = ttk.Button(
            master=self._frame,
            text="Continue >",
            command=self._handle_continue_click
        )
        self.continue_button.grid(column=4, row=5,
                                  padx=10, pady=20, sticky=constants.N)
        self._check_selected_count()

    # Handle button clicks

    def _handle_select_click(self):
        """Handles actions after button click: Add to selected >.
        Actions:
            Checks for errors.
            Saves selected station to the database.
            Clears selected list.
            Prints new selected list.
        """

        selected_values = []

        for i in self._list_label.curselection():
            if i == 0:
                return
            selected_values.append(i)
        station_service.save_selected(selected_values[0])

        self._initialize_selected()
        self._initialize_continue_to_settings()

    def _handle_clear_click(self):

        station_service.delete_selected()
        self._initialize_error_msg()
        self.select_button.config(state="normal")
        self._initialize_selected()
        self.continue_button.config(state="disabled")

    def _handle_continue_click(self):
        """Handles actions after button click.
        Actions:
            Saves selected station to the database.
            Switches view to station settings.
        """
        if self._check_selected_count():
            self._handle_show_settings_view()
        else:
            return

    # Get stations from database and return as lists

    def _get_selected_list(self):
        """Gets selected stations from the database and returns them as a list."""
        selected_list = ""
        for s in station_service.get_selected():
            # print(f"Selected {str(s.name)}")
            selected_list += str(s.name) + "\n"
        return selected_list

    def _get_station_list(self):
        """Gets stations from the database and returns them as a list."""
        stations_list = []
        for s in self.stations:
            #            nimi = str(s.station_id) +" "+ s.name
            nimi = s.name
            stations_list.append((s.station_id, nimi))
        return stations_list

    # View

    def _initialize(self):
        """Initializes the frame view"""
        self._frame = ttk.Frame(master=self._root)
        style = ttk.Style(self._frame)
        style.theme_use("clam")

        # Title of the window
        self.station_label = ttk.Label(master=self._frame, text="Select station",
                                       font=('Arial', 24, 'bold'))
        self.station_label.grid(column=0, row=0, columnspan=5,
                                padx=10, pady=10, sticky=constants.NW)
        # Error message
        self._initialize_error_msg()

        # Title of left field
        self.note1_label = ttk.Label(master=self._frame, text="Select 1 station at the time",
                                     font=('Arial', 12, 'bold'))
        self.note1_label.grid(column=0, row=2, columnspan=2,
                              padx=10, pady=10, sticky=constants.W)

        # Title of right field
        self.note2_label = ttk.Label(master=self._frame,
                                     text="Selected stations (max 5)                    ",
                                     font=('Arial', 12, 'bold'))
        self.note2_label.grid(column=3, row=2, columnspan=2,
                              padx=10, pady=10, sticky=constants.W)

        # List of stations
        self._initialize_stations_list()

        # Button select
        self.select_button = ttk.Button(
            master=self._frame,
            text="Add to >",
            state="normal",
            command=self._handle_select_click
        )
        self.select_button.grid(column=2, row=3,
                                padx=10, pady=10, sticky=constants.S)

        # Button clear all
        self.clear_button = ttk.Button(
            master=self._frame,
            text="< Clear all",
            command=self._handle_clear_click
        )
        self.clear_button.grid(column=2, row=4,
                               padx=10, pady=10, sticky=constants.N)

        # Selected list
        self._initialize_selected()

        # Button Continue to settings
        self._initialize_continue_to_settings()

        self._frame.grid_columnconfigure(0, weight=1, minsize=100)
        self._frame.grid_columnconfigure(1, weight=1, minsize=100)
        self._frame.grid_columnconfigure(2, weight=1, minsize=100)
        self._frame.grid_columnconfigure(3, weight=1, minsize=100)
        self._frame.grid_columnconfigure(4, weight=1, minsize=100)
        self._frame.grid_rowconfigure(0, weight=1, minsize=20)


print("STATIONLIST VIEW\n")
