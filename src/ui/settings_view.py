from tkinter import ttk, constants, StringVar
import re
from services.station_service import station_service
from services.observation_service import observation_service

class SettingsView:
    """Settings view."""

    def __init__(self, root, handle_show_weather_view, handle_show_stationlist_view):
        """Class constructoimport Tkinter as tkr. Creates new view for stations.

        Args:
            root:
                TKinter element, in which view is installed.
            handle_button_click
                Change to another view
        """

        self._root = root
        self._handle_show_weather_view = handle_show_weather_view
        self._handle_show_stationlist_view = handle_show_stationlist_view
        self._frame = None
        self._list_label = None
        self._button_select = None
        self._error_variable = None
        self._error_label = None

        self.station_id = None
        self.station_temp = None
        self.station_wind = None
        self.row = 0
        self._error_key = None
        self._error_label = ttk.Label(master=self._frame)
        self.selected_label = ttk.Label(master=self._frame)
        self._error_row_label = ttk.Label(master=self._frame)
        self.nick_label = None
        self.nick_entry = None
        self.nick_entry_list = {}
        self.station_row_list = {}
        self.stations = station_service.get_stations()

        self._initialize()

    def pack(self):
        """"Shows the view."""
        self._frame.pack(fill=constants.X)

    def destroy(self):
        """"Destroys the view."""
        self._frame.destroy()

    def _initialize_error_msg(self):
        """"Field for error message."""
        self._error_label.destroy()
        self._error_label = ttk.Label(
            master=self._frame,
            text=self._error_variable,
            foreground="red"
        )
        self._error_label.grid(column=0, row=1, padx=10, pady=5, columnspan=2)

    def _initialize_stations(self):
        """Initializes station rows with input entry for nickname"""

        for s in station_service.get_selected():

            # Save station_id and row for error messages
            self.station_row_list[s.station_id] = self.row

            self.selected_label = ttk.Label(master=self._frame, text=s.name,
                                            font=('Arial', 12, 'bold'))
            self.selected_label.grid(column=0, row=self.row, columnspan=2,
                                     padx=10, pady=2, sticky=constants.NW)
            self.row += 1

            self.nick_label = ttk.Label(master=self._frame, text="Nickname",
                                        font=('Arial', 12, 'normal'))
            self.nick_label.grid(column=0, row=self.row, columnspan=1,
                                 padx=10, pady=0, sticky=constants.NW)

            nick = StringVar()
            # If Nickname is already saved
            nick = station_service.get_nickname(s.station_id).nickname[0]

            self.nick_entry = ttk.Entry(master=self._frame,
                                        font=('Arial', 12, 'normal'))
            # Insert saved nickname on the field
            if nick is not None:
                self.nick_entry.insert(0, nick)
            self.nick_entry.grid(column=1, row=self.row, columnspan=1,
                                 padx=10, pady=0, sticky=constants.NW)

            # Save station_id and its nickname to make sure they match on save
            self.nick_entry_list[s.station_id] = self.nick_entry

            self.row += 1

    def _set_error_row(self, erow):
        """"Marks the row of a station with * if there is an error.
        Args: 
            row number
        Note: only one row is processed at the time """

        self._error_row_label = ttk.Label(master=self._frame,
                                          text="*",
                                          foreground="red"
                                          )
        self._error_row_label.grid(column=2, row=erow+1, padx=10, pady=5,
                                   columnspan=1, sticky=constants.NW)

    def _handle_save_click(self):
        """"Checks input data. If errors prints error messages, else
            saves nicknames and changes the view to Weather View."""
        for key, nick in self.nick_entry_list.items():
            nick_input = nick.get()

            # Checks maximum length of the name
            if len(nick_input) > 20:
                self._error_variable = "Too long nickname."
                self._error_key = key
                self._initialize_error_msg()
                self._set_error_row(self.station_row_list[key])
                return
            # Checks if name is empty or contains only letters, numbers or spaces
            if len(nick_input) == 0 or re.match(r"^[åäöa-zÅÄÖA-Z0-9\s-]+$", nick_input):
                pass
            else:
                self._error_key = key
                self._error_variable = "Nickname has unallowed characters."
                self._initialize_error_msg()
                self._set_error_row(self.station_row_list[key])
                return

            station_service.save_selected_nickname(key, nick_input)

            # TODO This note does not work - WHY?
            self._error_variable = "Wait! Loading weather information..."
            self._initialize_error_msg()

        # Retrieves observations for the selected stations
        for s1 in station_service.get_selected():
            observation_service.update_observation(s1.station_id)

        self._handle_show_weather_view()

    def _handle_back_click(self):
        """"Changes the view back to station selection."""
        self._handle_show_stationlist_view()

    def _initialize(self):
        """Initializes the frame view"""

        self._frame = ttk.Frame(master=self._root)

        station_label = ttk.Label(master=self._frame, text="Settings",
                                  font=('Arial', 24, 'bold'))
        station_label.grid(column=0, row=0, columnspan=3,
                           padx=10, pady=5, sticky=constants.W)

        self._error_variable = ""
        self._initialize_error_msg()

        note_label = ttk.Label(master=self._frame, text="You can rename stations. Nickname can contain max 20 characters.",
                               font=('Arial', 12, 'normal'))
        note_label.grid(column=0, row=2, columnspan=3,
                        padx=5, pady=10, sticky=constants.W)

        self.row = 3

        self._initialize_stations()

        select_button1 = ttk.Button(
            master=self._frame,
            text="Save and view>",
            command=self._handle_save_click
        )

        select_button1.grid(column=2, row=self.row+1, padx=10, pady=20,
                            rowspan=1, sticky=constants.EW)

        select_button1 = ttk.Button(
            master=self._frame,
            text="<Select stations",
            command=self._handle_back_click
        )

        select_button1.grid(column=1, row=self.row+1, padx=10, pady=20,
                            rowspan=1, sticky=constants.EW)

        self._frame.grid_columnconfigure(0, weight=3, minsize=100)
        self._frame.grid_columnconfigure(1, weight=1, minsize=50)
        self._frame.grid_columnconfigure(2, weight=1, minsize=50)


print("STATION VIEW\n")
