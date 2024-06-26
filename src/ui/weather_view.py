from tkinter import ttk, constants
from PIL import Image, ImageTk
from services.station_service import station_service
from services.observation_service import observation_service
from services.observation_scheduler import Scheduler


class WeatherView:
    """WeatherView class for showing observation data of selected stations."""

    def __init__(self, root, show_stationlist_view, show_settings_view):
        """Class constructor. Creates new view for weather data from station.

        Args:
            root:
                TKinter element, in which view is installed.
            handle_show_stationlist_view:
                next frame where stations are selected
            handle_show_settings_view:
                next frame where settings are made
            self._scheduler: Creates Scheduler instance

            self._stations: Gets list of all stations as objects

            self._station_loop: keeps track which stations have been shown
            self._station_time: keeps track station update interval time
            station_service.get_selected()

            Bases for the Labels, buttons, image on the frame
        """

        self._root = root
        self._frame = None
        self._show_stationlist_view = show_stationlist_view
        self._show_settings_view = show_settings_view
        self._scheduler = Scheduler()

        self._station_loop = {}
        self._station_time = {}
        self._interval_minutes = 10
        for sl in station_service.get_selected():
            self._station_loop[sl.station_id] = False
            self._station_time[sl.station_id] = self._interval_minutes

        self._error_variable = None
        self._station_name_label = ttk.Label(master=self._frame)
        self._error_label = ttk.Label(master=self._frame)
        self._station_temp_label = ttk.Label(master=self._frame)
        self._station_wind_label = ttk.Label(master=self._frame)
        self._station_date_label = ttk.Label(master=self._frame)
        self._bg_image = None
        self._label_img = None

        self._station_date = ""
        self._station_id = None
        self._station_temp = 0
        self._station_wind = 0
        self._station_wind_direction = 0
        self._station_error = 0

        self._initialize()

    def pack(self):
        """"Shows the view."""
        self._frame.pack(fill=constants.X)

    def destroy(self):
        """"Destroys the view."""
        self._frame.destroy()


    # Content labels

    def _initialize_error_msg(self):
        """"Initializes Label for error message."""
        self._error_label.destroy()
        self._error_label = ttk.Label(
            master=self._frame, text=self._error_variable,
            foreground="red"
        )

        self._error_label.grid(column=0, row=6, padx=10,
                pady=10, sticky=constants.W)

    def _initialize_name(self):
        """Initializes Label for the name of the station. If nickname is set, 
        shows it instead."""

        self._station_name_label.destroy()
        nick_var = station_service.get_nickname(self._station_id).get_nickname()[0]
        name_var = station_service.get_station(self._station_id).name

        if len(nick_var) > 0:
            name_var = nick_var

        self._station_name_label = ttk.Label(master=self._frame,
                text=name_var, font=('Arial', 24, 'bold'))
        self._station_name_label.grid(
            column=0, row=1, columnspan=3, padx=10, pady=10, sticky=constants.W)

    def _initialize_observations(self):
        """Initializes Labels for observation data: temperature, wind and time.
        Actions:
            observation_service.get_observation: gets data from database as instance
            Destroys previous labels
            station_temp_label: Temperature
            station_wind_label: wind and its direction
            station_date_label: time of observation
            self.initialize_obs_update: runs check if data needs update
        """

        self._error_variable = None
        self._initialize_error_msg()

        o = observation_service.get_observation(self._station_id)
        self._station_temp = o.temperature
        self._station_wind = o.wind
        self._station_wind_direction = o.wind_direction
        self._station_date = o.datetime
        self._station_error = o.error_msg
        none_error = 0

        self._station_temp_label.destroy()
        temp_text = f"{self._station_temp}°C"
        if self._station_temp is None:
            temp_text = "-"
            none_error = 1

        self._station_temp_label = ttk.Label(master=self._frame, text=temp_text,
                                            font=('Arial', 42, 'bold'))
        self._station_temp_label.grid(column=0, row=2, columnspan=3,
                                     padx=10, pady=10)

        self._station_wind_label.destroy()
        wind_text = f"Wind: {self._station_wind} m/s    \
                Direction: {self._station_wind_direction}°"
        if self._station_wind is None:
            wind_text = "Wind: -"
            none_error = 1

        self._station_wind_label = ttk.Label(master=self._frame,
                                            text=wind_text,
                                            font=('Arial', 16, 'bold'))
        self._station_wind_label.grid(
            column=0, row=3, padx=10, pady=10, 
            columnspan=3, sticky=constants.N)

        self._station_date_label.destroy()
        if self._station_error == 1:
            self._error_variable = "No current observations from the station"
            date_label = f"Unable to retrieve data at: {self._station_date}"
        else:
            date_label = f"Observation time: {self._station_date}"

        self._station_date_label = ttk.Label(master=self._frame, text=date_label,
                                            font=('Arial', 12, 'bold'))
        self._station_date_label.grid(
            column=0, row=4, padx=10, pady=10, sticky=constants.W)

        if none_error>0:
            self._error_variable = "Some requested data was not available"
            self._initialize_error_msg()

        self.initialize_obs_update()


    # Buttons

    def _initialize_buttons(self):
        """"Initializes Button 'Select stations' to switch to
        its view. Button 'Settings' switches to the Settings View.
        Buttons are located at the bottom of the frame."""

        select_button = ttk.Button(
            master=self._frame,
            text="Select stations", style='Dodger.TButton',
            command=self._show_stationlist_view
        )

        select_button.grid(column=1, row=6, padx=10,
                           pady=10, sticky=constants.EW)

        settings_button = ttk.Button(
            master=self._frame,
            text="Settings", style='Dodger.TButton',
            command=self._show_settings_view
        )

        settings_button.grid(column=2, row=6, padx=10,
                             pady=10, sticky=constants.EW)


    # Observations update

    def initialize_obs_update(self):
        """Function checks if datetime of the observation
        is older than stations interval minutes. 
        Triggers update for old data.

        observation_service.check_obs_if_old: checks if old
        self._scheduler.scheduled_observation_update: gets new data
        If no new data is recieved:
            slows down checks by adding 2 and 10 minutes 
            to the interval time.
        If new data is recieved: returns interval time to global settings.
        """
        if observation_service.check_obs_if_old(self._station_date,
                                                self._station_time[self._station_id]):
            if not self._scheduler.scheduled_observation_update(self._station_id,
                                                self._station_time[self._station_id]):
                if self._station_time[self._station_id]<20:
                    self._station_time[self._station_id] += 2
                elif self._station_time[self._station_id]<60:
                    self._station_time[self._station_id] += 10
            else:
                self._station_time[self._station_id] = self._interval_minutes
        return


    # View update

    def _update_view(self):
        """Update view switches view to next station in every 20 sec.

        self._station_loop[self._station_id]: Set previous station as viewed True
        self._station_loop: Find next unviewed (False) station
        counter: If all station_loops are viewed ->
            Set all stations from viewed (True) as unviewed (False)
        self._initialize_name: initializes station name/nickname
        self._initialize_observations: initializes observation data
        self._initialize_error_msg: initializes error message
        self._frame.after: waits 20 sec until runs again
        """

        if self._station_id is not None:
            self._station_loop[self._station_id] = True

        counter = 0
        for key_id, status in self._station_loop.items():
            if status is False:
                self._station_id = key_id
                break
            else:
                counter += 1

        if counter == station_service.count_selected()[0]:
            for key in self._station_loop:
                self._station_loop[key] = False
            self._station_id = next(iter(self._station_loop))

        self._initialize_name()
        self._initialize_observations()
        self._initialize_error_msg()
        self._frame.after(20000, self._update_view)


    # Layout image and colors

    def _load_colors_and_image(self, style):
        """Adds style configurations for layout.
        Actions:
            Configures theme
            Configures background color for frame and labels.
            Configures colors for buttons. 
            Opens image file.
            Sets Label for the image.
        """

        style.theme_use("clam")
        style.configure('TFrame', background='white')
        style.configure('TLabel', background='white')
        style.configure('Dodger.TButton', foreground='black', background='dodger blue')

        image = Image.open("./src/ui/background.png")
        self._bg_image = ImageTk.PhotoImage(image)

        self._label_img = ttk.Label(self._frame, image=self._bg_image)
        self._label_img.grid(column=0, row=0, columnspan=5)


    # Frame

    def _initialize(self):
        """Initializes the frame view.
        Sets title label
        Actions:
            load_colors_and_image: Loads colors and image on layout
            _update_view: Label for error message
            _initialize_buttons: Buttons Select stations and Settings
            grid_columnconfigure: Grid size configurations
        """
        self._frame = ttk.Frame(master=self._root)
        style = ttk.Style(self._frame)
        self._load_colors_and_image(style)

        title_label = ttk.Label(master=self._frame, text="   Weather at the station ",
                                  font=('Arial', 24, 'bold'))
        title_label.grid(column=0, row=0, columnspan=3,
                           padx=10, pady=10, sticky=constants.W)
        self._error_variable = ""
        self._update_view()

        self._initialize_buttons()

        self._frame.grid_columnconfigure(0, weight=1, minsize=100)
