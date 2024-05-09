from tkinter import ttk, constants
from services.station_service import station_service
from services.observation_service import observation_service
from services.observation_scheduler import Scheduler


class WeatherView:
    """Weather from the station view."""

    def __init__(self, root, show_stationlist_view, show_settings_view):
        """Class constructor. Creates new view for weather data from station.

        Args:
            root:
                TKinter element, in which view is installed.
        """

        self._root = root
        self._frame = None
        self._show_stationlist_view = show_stationlist_view
        self._show_settings_view = show_settings_view
        self._scheduler = Scheduler()

        self._error_variable = None
        self.station_loop = {}
        for sl in station_service.get_selected():
            self.station_loop[sl.station_id] = False
        self.station_id = None
        self.station_temp = 0
        self.station_wind = 0
        self.station_wind_direction = 0
        self.station_error = 0
        self.station_name_label = ttk.Label(master=self._frame)
        self._error_label = ttk.Label(master=self._frame)
        self.station_temp_label = ttk.Label(master=self._frame)
        self.station_wind_label = ttk.Label(master=self._frame)
        self.station_date_label = ttk.Label(master=self._frame)
        self.station_date = ""
        self.station_update = []

        self._initialize()

    def pack(self):
        """"Shows the view."""
        self._frame.pack(fill=constants.X)

    def destroy(self):
        """"Destroys the view."""
        self._frame.destroy()

    def _initialize_error(self):

        self._error_label.destroy()
        self._error_label = ttk.Label(
            master=self._frame,
            text=self._error_variable,
            foreground="red"
        )

        self._error_label.grid(column=0, row=1, padx=10,
                               pady=10, sticky=constants.W)

    def _initialize_name(self):
        self.station_name_label.destroy()
        nick_var = station_service.get_nickname(self.station_id).get_nickname()
        name_var = station_service.get_station(self.station_id)[0].name
        if len(nick_var) > 0:
            name_var = nick_var

        self.station_name_label = ttk.Label(master=self._frame,
                                            text=name_var,
                                            font=('Arial', 24, 'bold'))
        self.station_name_label.grid(
            column=0, row=2, columnspan=2, padx=10, pady=20, sticky=constants.W)

    def _initialize_observations(self):

        o = observation_service.get_observation(self.station_id)
        self.station_temp = o.temperature
        self.station_wind = o.wind
        self.station_wind_direction = o.wind_direction
        self.station_date = o.datetime
        self.station_error = o.error_msg

        self.station_temp_label.destroy()
        temp_text = f"{self.station_temp}°C"
        if self.station_temp is None:
            temp_text = "No data available"

        self.station_temp_label = ttk.Label(master=self._frame, text=temp_text,
                                            font=('Arial', 42, 'bold'))
        self.station_temp_label.grid(column=0, row=3, columnspan=2,
                                     padx=10, pady=10)

        self.station_wind_label.destroy()
        wind_text = f"Wind: {self.station_wind} m/s    \
                Direction: {self.station_wind_direction}°"
        if self.station_wind is None:
            wind_text = "Wind: No data available"

        self.station_wind_label = ttk.Label(master=self._frame,
                                            text=wind_text,
                                            font=('Arial', 14, 'bold'))
        self.station_wind_label.grid(
            column=0, row=4, padx=10, pady=10, sticky=constants.W)

        self.station_date_label.destroy()
        if self.station_error == 1:
            self._error_variable = "No current observations from the station"
            date_label = f"Unable to retrieve data at: {self.station_date}"
        else:
            date_label = f"Observation time: {self.station_date}"

        self.station_date_label = ttk.Label(master=self._frame, text=date_label,
                                            font=('Arial', 12, 'bold'))
        self.station_date_label.grid(
            column=0, row=5, padx=10, pady=10, sticky=constants.W)

        # Trigger if new data needs to be retrieved
        self._scheduler.scheduled_observation_update()

    def _update_view(self):
        # Set previous station as viewed True
        if self.station_id is not None:
            self.station_loop[self.station_id] = True

        # Find unviewed (False) station
        counter = 0
        for key_id, status in self.station_loop.items():
            if status is False:
                self.station_id = key_id
                break
            else:
                counter += 1
        # Set all stations from viewed (True) as unviewed (False)
        if counter == station_service.count_selected():
            for key in self.station_loop:
                self.station_loop[key] = False
                self.station_id = key

        self._initialize_name()
        self._initialize_observations()
        self._initialize_error()
        self._frame.after(10000, self._update_view)

    def _initialize(self):
        """Initializes the frame view"""
        self._frame = ttk.Frame(master=self._root)

        weather_label = ttk.Label(master=self._frame, text="Weather at the station",
                                  font=('Arial', 24, 'bold'))
        weather_label.grid(column=0, row=0, columnspan=2,
                           padx=10, pady=10, sticky=constants.W)
        self._error_variable = "TEST: Stations are on 10 sec loop"
        self._update_view()

        select_button = ttk.Button(
            master=self._frame,
            text="Select stations",
            command=self._show_stationlist_view
        )

        select_button.grid(column=1, row=6, padx=10,
                           pady=10, sticky=constants.EW)

        settings_button = ttk.Button(
            master=self._frame,
            text="Settings",
            command=self._show_settings_view
        )

        settings_button.grid(column=1, row=7, padx=10,
                             pady=10, sticky=constants.EW)
        self._frame.grid_columnconfigure(0, weight=1, minsize=100)


print("WEATHER_VIEW\n")
