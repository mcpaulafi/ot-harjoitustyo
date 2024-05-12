from tkinter import ttk, constants, StringVar
import re
from PIL import Image, ImageTk
from services.station_service import station_service
from services.observation_service import observation_service

class SettingsView:
    """Class for Settings view."""

    def __init__(self, root, handle_show_weather_view, handle_show_stationlist_view):
        """Class constructoimport Tkinter as tkr. Creates new view for stations.

        Args:
            root:
                TKinter element, in which view is installed.
            handle_show_weather_view: Change to Weather view
            handle_show_stationlist_view: Change to Select stations view
            self._stations : list of Station objects
            self._row: keeps count of grid row number
        """

        self._root = root
        self._handle_show_weather_view = handle_show_weather_view
        self._handle_show_stationlist_view = handle_show_stationlist_view
#        self._stations = station_service.get_stations()
        self._frame = None
        self._row = 0

        self._list_label = None
        self._button_select = None
        self._error_variable = None
        self._error_label = None
        self._error_key = None
        self._error_label = ttk.Label(master=self._frame)
        self._name_label = ttk.Label(master=self._frame)
        self._error_row_label = ttk.Label(master=self._frame)
        self._bg_image = None
        self._label_img = None
        self._nick_label = None
        self._nick_entry = None
        self._nick_entry_list = {}
        self._station_row_list = {}

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
        self._error_label.grid(column=0, row=1, padx=5, pady=0,
                               columnspan=2, sticky=constants.W)
        self._frame.update_idletasks()


    # Buttons

    def _initialize_buttons(self):
        """Initializes Button  'Save and view>' and Button <Select stations.
        Both are located at the bottom of the frame.
        """

        select_button1 = ttk.Button(
            master=self._frame, text="Save and view>", style='Dodger.TButton',
            command=self._handle_save_click
        )
        select_button1.grid(column=2, row=self._row+1, padx=10, pady=10,
                            rowspan=1, sticky=constants.EW)

        select_button1 = ttk.Button(
            master=self._frame, text="<Select stations", style='Dodger.TButton',
            command=self._handle_back_click
        )
        select_button1.grid(column=1, row=self._row+1, padx=10, pady=10,
                            rowspan=1, sticky=constants.EW)

    def _initialize_stations(self):
        """Initializes station labels and input entry for nickname.
        Actions:
            _station_row_list[s.station_id]: Saves station_id and row for error messages
            _name_label: Official station name
            _nick_label: Nickname title
            station_service.get_nickname: Gets nickname from database 
                if it is already saved
            nick_entry: Entry for nickname input
            self.nick_entry_list[s.station_id]: Saves station_id and nickname to make sure 
                they match on save
        """

        for s in station_service.get_selected():
            self._station_row_list[s.station_id] = self._row

            self._name_label = ttk.Label(master=self._frame, 
                    text=s.name, font=('Arial', 12, 'bold'))
            self._name_label.grid(column=0, row=self._row, columnspan=2,
                    padx=10, pady=2, sticky=constants.NW)
            self._row += 1

            self._nick_label = ttk.Label(master=self._frame, 
                    text="Nickname", font=('Arial', 12, 'normal'))
            self._nick_label.grid(column=0, row=self._row, columnspan=1,
                    padx=10, pady=0, sticky=constants.NW)

            nick = StringVar()
            nick = station_service.get_nickname(s.station_id).nickname[0]

            self._nick_entry = ttk.Entry(master=self._frame,
                                        font=('Arial', 12, 'normal'))
            if nick is not None:
                self._nick_entry.insert(0, nick)
            self._nick_entry.grid(column=1, row=self._row, columnspan=1,
                                 padx=10, pady=0, sticky=constants.NW)

            self._nick_entry_list[s.station_id] = self._nick_entry
            self._row += 1

    def _set_error_row(self, erow):
        """"Marks the row of a station with * if there is an error.
        Args: 
            row number
        Note: 
            only one row is processed at the time!"""

        self._error_row_label = ttk.Label(master=self._frame,
                            text="*", foreground="red"
        )
        self._error_row_label.grid(column=2, row=erow+1, padx=5, pady=5,
                                   columnspan=1, sticky=constants.NW)


    # Handle button clicks

    def _handle_save_click(self):
        """"Handles actions after button click 'Save and continue>'.
        Checks input data. If errors prints error messages,
        if none saves nicknames to database and 
        changes the view to Weather View.
        Actions:
            Gets nick entry
            Checks maximum length of the name<20
            Checks if name is empty or contains only letters, numbers or spaces
            station_service.save_selected_nickname: Saves nickname to the database
            _initialize_error_msg: Re-initializes error Label
            observation_service.update_observation: Retrieves observations for the selected stations
            self._handle_show_weather_view: Switches to weather view
        In case errors on input:
            _initialize_error_msg: Re-initializes error Label
            _set_error_row: Initializes action that shows the row of error
        """

        for key, nick in self._nick_entry_list.items():
            nick_input = nick.get()

            if len(nick_input) > 20:
                self._error_row_label.config(text="")
                self._error_variable = "Too long nickname."
                self._error_key = key
                self._initialize_error_msg()
                self._set_error_row(self._station_row_list[key])
                return

            if len(nick_input) == 0 or re.match(r"^[åäöa-zÅÄÖA-Z0-9\s-]+$", nick_input):
                pass
            else:
                self._error_row_label.config(text="")
                self._error_key = key
                self._error_variable = "Nickname has unallowed characters."
                self._initialize_error_msg()
                self._set_error_row(self._station_row_list[key])
                return

            station_service.save_selected_nickname(key, nick_input)

            self._error_variable = "Wait! Loading weather information..."
            self._initialize_error_msg()

        for s1 in station_service.get_selected():
            observation_service.update_observation(s1.station_id)

        self._handle_show_weather_view()

    def _handle_back_click(self):
        """"Changes the view back to station selection."""
        self._handle_show_stationlist_view()


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


    #Frame

    def _initialize(self):
        """Initializes the frame view.
        Sets titles:
            title_label: Settings
            note_label: instructions to fill Entry
        Actions:
            load_colors_and_image: Loads colors and image on layout
            _initialize_error_msg: Label for error message
            _initialize_stations_list: Loads station labels
            _initialize_buttons: Buttons <Select stations and <Save and view
            grid_columnconfigure: Grid size configurations
        """

        self._frame = ttk.Frame(master=self._root)
        style = ttk.Style(self._frame)
        self._load_colors_and_image(style)

        title_label = ttk.Label(master=self._frame, 
                        text="   Settings ",
                        font=('Arial', 24, 'bold'))
        title_label.grid(column=0, row=0, columnspan=3,
                        padx=10, pady=0, sticky=constants.W)

        self._initialize_error_msg()

        note_label = ttk.Label(master=self._frame,
                text="You can rename stations. Nickname can contain max 20 characters.",
                font=('Arial', 12, 'normal'))
        note_label.grid(column=0, row=2, columnspan=3,
                        padx=5, pady=10, sticky=constants.W)
        self._row = 3

        self._initialize_stations()
        self._initialize_buttons()

        self._frame.grid_columnconfigure(0, weight=3, minsize=50)
        self._frame.grid_columnconfigure(1, weight=1, minsize=50)
        self._frame.grid_columnconfigure(2, weight=1, minsize=50)
