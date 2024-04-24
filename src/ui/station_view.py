from tkinter import ttk, constants, StringVar
from services.station_service import station_service
from services.observation_service import observation_service

# rename this to settings
class StationView:
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
        self._label_selection = "none"
#        self.station_id = station_service.get_selected()[0][0]
        self.station_id = None
        self.station_temp = None
        self.station_wind = None
        self.row = 0
        self._error_label = ttk.Label(master=self._frame)
        self.selected_label = ttk.Label(master=self._frame)
        self.nick_label = ttk.Label(master=self._frame)
        self.nick_entry = ttk.Entry(master=self._frame)
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
            textvariable=self._error_variable,
            foreground="red"
        )
        self._error_label.grid(column=0, row=1, padx=10, pady=10, columnspan=2)

    def _initialize_stations(self):

        for s in station_service.get_selected():

            self.selected_label = ttk.Label(master=self._frame, text=s.name,
                                            font=('Arial', 12, 'bold'))
            self.selected_label.grid(column=0, row=self.row, columnspan=2,
                                      padx=10, pady=2, sticky=constants.NW)
            self.row +=1

            self.nick_label = ttk.Label(master=self._frame, text="Nickname",
                                            font=('Arial', 12, 'normal'))
            self.nick_label.grid(column=0, row=self.row, columnspan=1,
                                      padx=10, pady=0, sticky=constants.NW)

            name_var= StringVar()
            name_var.set("")

            self.nick_entry = ttk.Entry(master=self._frame, textvariable=name_var,
                                            font=('Arial', 12, 'normal'))
            self.nick_entry.grid(column=1, row=self.row, columnspan=1,
                                      padx=10, pady=0, sticky=constants.NW)

            self.row+=1


    def _handle_save_click(self):
        """"Changes the view."""
        #Fix later
        self._error_variable = "Loading weather information..."
        self._initialize_error_msg()

        for s1 in station_service.get_selected():
            observation_service.update_observation(s1.station_id)
            print("Observations updated", s1.name)

        self._handle_show_weather_view()

    def _handle_back_click(self):
        """"Changes the view back to station selection."""
        self._handle_show_stationlist_view()

    def _initialize(self):
        """Initializes the frame view"""

        self._frame = ttk.Frame(master=self._root)

        station_label = ttk.Label(master=self._frame, text="Settings",
                                  font=('Arial', 24, 'bold'))
        station_label.grid(column=0, row=0, columnspan=2,
                           padx=10, pady=5, sticky=constants.W)

        self._error_variable = "Functions for station options are not ready yet. Click buttons."
        self._initialize_error_msg()

        self.row = 2

        self._initialize_stations()

        select_button1 = ttk.Button(
            master=self._frame,
            text="Save and view>",
            command=self._handle_save_click
        )

        select_button1.grid(column=1, row=self.row+1, padx=10, pady=20,
                           rowspan=1, sticky=constants.EW)

# Note to testers
        note_label = ttk.Label(
            master=self._frame,
            text="Wait! Loading observation data takes a while.",
            foreground="red"
        )
        note_label.grid(column=1, row=self.row+2, columnspan=2)


        select_button1 = ttk.Button(
            master=self._frame,
            text="<Select stations",
            command=self._handle_back_click
        )

        select_button1.grid(column=0, row=self.row+1, padx=10, pady=20,
                           rowspan=1, sticky=constants.EW)


        self._frame.grid_columnconfigure(0, weight=1, minsize=100)
        self._frame.grid_columnconfigure(1, weight=1, minsize=100)


print("STATION VIEW\n")
