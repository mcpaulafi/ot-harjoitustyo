from tkinter import ttk, constants
from services.station_service import station_service

class StationView:
    """Station list view."""

    def __init__(self, root, handle_show_weather_view):
        """Class constructoimport Tkinter as tkr. Creates new view for stations.

        Args:
            root:
                TKinter element, in which view is installed.
            handle_button_click
                Change to another view
        """

        self._root = root
        self._handle_show_weather_view = handle_show_weather_view
        self._frame = None
        self._list_label = None
        self._button_select = None
        self._error_variable = None
        self._error_label = None
        self._label_selection = "none"
        self.station_id = station_service.get_selected()[0][0]
        self.station_temp = station_service.get_selected()[0][1]
        self.station_wind = station_service.get_selected()[0][2]
        self.stations = station_service.get_stations()

        self._initialize()

    def pack(self):
        """"Shows the view."""
        self._frame.pack(fill=constants.X)

    def destroy(self):
        """"Destroys the view."""
        self._frame.destroy()

    def _handle_button_click(self):
        """"Changes the view."""
        self._handle_show_weather_view()

    def _initialize(self):
        """Initializes the frame view"""

        self._frame = ttk.Frame(master=self._root)

        station_label = ttk.Label(master=self._frame, text="Station settings",
                                  font=('Arial', 24, 'bold'))
        station_label.grid(column=0, row=1, padx=5, pady=5, sticky=constants.W)

        self._error_label = ttk.Label(
            master=self._frame,
            textvariable=self._error_variable,
            foreground="red"
        )

        self._error_label.grid(column=0, row=2, padx=5, pady=5)

        station_name = "none"

        for s in station_service.get_name(self.station_id):
            station_name = s.name

        selection_label = ttk.Label(master=self._frame, text=f"Selected station is {self.station_id}, name: {station_name}",
                                    font=('Arial', 12, 'normal'))
        selection_label.grid(column=0, row=3, padx=5,
                             pady=5, sticky=constants.W)

        temperature = "SELECTED"
        if self.station_temp == 0:
            temperature = "NOT SELECTED"

        wind = "SELECTED"
        if self.station_wind == 0:
            wind = "NOT SELECTED"

        temp_label = ttk.Label(master=self._frame, text=f"Temperature {temperature}",
                                    font=('Arial', 12, 'normal'))
        temp_label.grid(column=0, row=4, padx=5,
                             pady=5, sticky=constants.W)

        wind_label = ttk.Label(master=self._frame, text=f"Wind {temperature}",
                                    font=('Arial', 12, 'normal'))
        wind_label.grid(column=0, row=5, padx=5,
                             pady=5, sticky=constants.W)


        self._frame.grid_columnconfigure(0, weight=1, minsize=400)
        select_button1 = ttk.Button(
            master=self._frame,
            text="Save and view",
            command=self._handle_button_click
        )

        select_button1.grid(column=0, row=6, padx=5, pady=5,
                           rowspan=1, sticky=constants.EW)


        self._frame.grid_columnconfigure(0, weight=1, minsize=400)


print("STATION VIEW\n")
