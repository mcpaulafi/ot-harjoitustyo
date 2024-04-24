from tkinter import ttk, constants
from services.station_service import station_service
from services.observation_service import observation_service

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
        self.station_loop = {}
        for sl in station_service.get_selected():
            self.station_loop[sl.station_id] = False
        self.station_id = None
        self.station_temp = 0
        self.station_wind = 0
        self.station_wind_direction = 0
        self.station_error = 0
        self.station_name_label = ttk.Label(master=self._frame)
        self.station_temp_label = ttk.Label(master=self._frame)
        self.station_wind_label = ttk.Label(master=self._frame)
        self.station_date_label = ttk.Label(master=self._frame)
        self.station_date = ""

#        self.stations = station_service.get_stations()

        self._initialize()

    def pack(self):
        """"Shows the view."""
        self._frame.pack(fill=constants.X)

    def destroy(self):
        """"Destroys the view."""
        self._frame.destroy()

    def _initialize_name(self):
        self.station_name_label.destroy()
        self.station_name_label = ttk.Label(master=self._frame,
                            text=station_service.get_name(self.station_id)[0].name,
                            font=('Arial', 24, 'bold'))
        self.station_name_label.grid(column=0, row=2, padx=10, pady=20, sticky=constants.W)

    def _initialize_observations(self):

        for o in observation_service.get_observation(self.station_id):
            self.station_temp = o.temperature
            self.station_wind = o.wind
            self.station_wind_direction = o.wind_direction
            self.station_date = o.datetime
            self.station_error = o.error_msg

        self.station_temp_label.destroy()
        self.station_temp_label = ttk.Label(master=self._frame, text=f"{self.station_temp}°C",
                                          font=('Arial', 42, 'bold'))
        self.station_temp_label.grid(column=0, row=3, columnspan=2,
                                     padx=10, pady=10)

        self.station_wind_label.destroy()
        self.station_wind_label = ttk.Label(master=self._frame,
             text=f"Wind: {self.station_wind} m/s    \
                Direction: {self.station_wind_direction}°",
                font=('Arial', 14, 'bold'))
        self.station_wind_label.grid(column=0, row=4, padx=10, pady=10, sticky=constants.W)

        self.station_date_label.destroy()
        if self.station_error == 1:
            date_label = f"Unable to retrieve data at: {self.station_date}"
        else:
            date_label = f"Observations collected: {self.station_date}"

        self.station_date_label = ttk.Label(master=self._frame, text=date_label,
                                          font=('Arial', 12, 'bold'))
        self.station_date_label.grid(column=0, row=5, padx=10, pady=10, sticky=constants.W)

    def _update_view(self):
        # Set previous station as viewed True
        if self.station_id is not None:
            self.station_loop[self.station_id] = True
        
        # Find unviewed (False) station
        counter = 0
        for k, v in self.station_loop.items():
            if v is False:
                self.station_id = k
                break
            else:
                counter +=1
        # Set all stations from viewed (True) as unviewed (False)
        if counter == station_service.count_selected():
            for key in self.station_loop:
                self.station_loop[key] = False
                self.station_id = key

        self._initialize_name()
        self._initialize_observations()
        self._frame.after(10000, self._update_view)



    def _initialize(self):
        """Initializes the frame view"""
        self._frame = ttk.Frame(master=self._root)

        weather_label = ttk.Label(master=self._frame, text="Weather at the station",
                                  font=('Arial', 24, 'bold'))
        weather_label.grid(column=0, row=0, columnspan=2,
                           padx=10, pady=10, sticky=constants.W)
        
        self._error_label = ttk.Label(
            master=self._frame,
            text="Stations are on 10 sec loop",
            foreground="red"
        )

        self._error_label.grid(column=0, row=1, padx=10, pady=10, sticky=constants.W)


        self._update_view()

        select_button = ttk.Button(
            master=self._frame,
            text="Select station",
            command=self._show_stationlist_view
        )

        select_button.grid(column=1, row=6, padx=10, pady=10, sticky=constants.EW)

        self._frame.grid_columnconfigure(0, weight=1, minsize=100)


print("WEATHER_VIEW\n")
