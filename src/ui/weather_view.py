from tkinter import ttk, StringVar, constants
from services.station_service import station_service


class WeatherView:
    """Weather from the station view."""

    def __init__(self, root, show_stationlist_view):
        """Class constructor. Creates new view for weather data from station.

        Args:
            root:
                TKinter element, in which view is installed.
        """

        self._root = root
        self._frame = None
        self._show_stationlist_view = show_stationlist_view
        self._error_variable = None
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

    def _initialize(self):
        """Initializes the frame view"""
        self._frame = ttk.Frame(master=self._root)

        self._error_label = ttk.Label(
            master=self._frame,
            textvariable=self._error_variable,
            foreground="red"
        )

        self._error_label.grid(padx=5, pady=5)

        weather_label = ttk.Label(master=self._frame, text="Weather at the station",
                                  font=('Arial', 24, 'bold'))
        weather_label.grid(padx=5, pady=5, sticky=constants.W)

        station_name= "Station not selected"
        for s in station_service.get_name(self.station_id):
            station_name = s.name

        station_name_label = ttk.Label(master=self._frame, text=station_name,
                                       font=('Arial', 12, 'bold'))
        station_name_label.grid(padx=5, pady=5, sticky=constants.W)

        station_weather_label = ttk.Label(master=self._frame, text="Temperature here",
                                          font=('Arial', 42, 'bold'))
        station_weather_label.grid(padx=5, pady=5, sticky=constants.W)

        select_button = ttk.Button(
            master=self._frame,
            text="Select station",
            command=self._show_stationlist_view
        )

        select_button.grid(padx=5, pady=5, sticky=constants.EW)

        self._frame.grid_columnconfigure(0, weight=1, minsize=400)


print("WEATHER_VIEW\n")
