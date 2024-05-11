from tkinter import ttk, constants, Listbox, Scrollbar
from PIL import Image, ImageTk
from services.station_service import station_service


class StationListView:
    """Station list view class for selecting weather stations."""

    def __init__(self, root, handle_show_settings_view):
        """Class constructor import Tkinter. Creates new view for selecting stations.

        Args:
            root:
                TKinter element, in which view is installed.
            handle_show_settings_view:
                next frame where settings are made

            handle_button_click:
                Save selection to the database and change to station settigns view
            self.stations: Gets list of all stations as objects
            Bases for the Labels, buttons, image on the frame
        """

        self._root = root
        self._handle_show_settings_view = handle_show_settings_view
        self.stations = station_service.get_stations()
        self._frame = None

        self._list_label = None
        self._button_select = None
        self._error_variable = None
        self._error_label = ttk.Label(master=self._frame)
        self.selected_label = ttk.Label(master=self._frame)
        self._list_label = Listbox(master=self._frame)
        self._vertscroll = Scrollbar(master=self._frame)
        self.continue_button = ttk.Button(master=self._frame)
        self.bg_image = None
        self.label_img = None
        self.select_button = None
        self.clear_button = None

        self._initialize()

    def pack(self):
        """"Shows the view."""
        self._frame.pack(fill=constants.X)

    def destroy(self):
        """"Destroys the view."""
        self._frame.destroy()


    # Content fields

    def _initialize_error_msg(self):
        """"Initializes Label for error message."""
        self._error_label.destroy()
        self._error_label = ttk.Label(
            master=self._frame, text=self._error_variable,
            foreground="red"
        )
        self._error_label.grid(column=0, row=2, columnspan=3)

    def _initialize_stations_list(self):
        """"Initializes Listbox of all stations and its scrollbar."""

        self._list_label.destroy()
        self._list_label = Listbox(
            master=self._frame, selectmode="single", width=28)

        # Without this empty line station ids are +1 off
        self._list_label.insert(0, "")

        for s in self.stations:
            self._list_label.insert(s.station_id, s.name)

        self._list_label.grid(column=0, row=3, columnspan=2, rowspan=2,
                              padx=10, pady=10, sticky=constants.W)

        # Scrollbar for listbox
        self._vertscroll.destroy()
        self._vertscroll = Scrollbar(master=self._frame)
        self._vertscroll.config(command=self._list_label.yview)
        self._list_label.config(yscrollcommand=self._vertscroll.set)
        self._vertscroll.grid(column=1, row=3, columnspan=2, rowspan=2,
                              sticky=constants.NS)

    def _initialize_selected(self):
        """"Initializes Label for the string of selected stations.
        Checks also how many stations have been selected."""

        self.selected_label.destroy()
        list_of_selected = station_service.get_selected_names()
        self.selected_label = ttk.Label(master=self._frame, text=list_of_selected,
                                        font=('Arial', 12, 'normal'))
        self.selected_label.grid(column=3, row=3, columnspan=2, rowspan=2,
                                 padx=10, pady=10, sticky=constants.NW)
        self._check_selected_count()


    # Buttons

    def _initialize_select_clear_buttons(self):
        """"Initializes Button 'Add to>' for selecting stations and another 
        Button '<Clear all' for clearing selected stations. 
        Located between station list and selected stations."""

        self.select_button = ttk.Button(
            master=self._frame,
            text="Add to >", state="normal", style='Dodger.TButton',
            command=self._handle_select_click
        )
        self.select_button.grid(column=2, row=3,
                                padx=10, pady=10, sticky=constants.S)

        self.clear_button = ttk.Button(
            master=self._frame, text="< Clear all", style='Dodger.TButton',
            command=self._handle_clear_click
        )
        self.clear_button.grid(column=2, row=4,
                               padx=10, pady=10, sticky=constants.N)

    def _initialize_continue_to_settings(self):
        """"Initializes Button 'Continue>' for continuing forward to the weather view.
        Checks also how many stations have been selected."""
        self.continue_button.destroy()
        self.continue_button = ttk.Button(
            master=self._frame, text="Continue >", style='Dodger.TButton',
            command=self._handle_continue_click
        )
        self.continue_button.grid(column=4, row=7,
                                  padx=10, pady=20, sticky=constants.N)
        self._check_selected_count()


    # Handle button clicks

    def _check_selected_count(self):
        """"Check how many stations have been selected and changes button states.
        Actions:
            Select and Continue buttons are disabled if number >= 5.
            Continue button is disabled if number < 1
            Initializes error message on these events."""

        if station_service.count_selected()[0] > 4:
            self._error_variable = "At maximum 5 stations can be selected."
            self._initialize_error_msg()
            self.select_button.config(state="disabled")
            self.continue_button.config(state="disabled")
            return False
        elif station_service.count_selected()[0] < 1:
            self._error_variable = "Select at least 1."
            self._initialize_error_msg()
            self.continue_button.config(state="disabled")
            return False
        else:
            self.select_button.config(state="normal")
            return True

    def _handle_select_click(self):
        """Handles actions after button click: 'Add to>'.
        Actions:
            Adds selected value on a list.
            Saves selected station to the database with station service.
            Clears and prints new selected list.
            Re-initializes Continue-button.
        """

        selected_values = []
        for i in self._list_label.curselection():
            if i == 0:
                return
            selected_values.append(i)

        if len(selected_values)>0:
            station_service.save_selected(selected_values[0])

        self._initialize_selected()
        self._initialize_continue_to_settings()

    def _handle_clear_click(self):
        """Handles actions after button click: '<Clear all'.
        Actions:
            Deletes selected stations from databasewith station service.
            Re-initializes error message Label.
            Re-initializes Select button and its state.
            Changes Continue button state.
        """
        station_service.delete_selected()
        self._initialize_error_msg()
        self.select_button.config(state="normal")
        self._initialize_selected()
        self.continue_button.config(state="disabled")

    def _handle_continue_click(self):
        """Handles actions after button click 'Continue>'.
        Actions:
            Checks selected count.
            Switches view to Settings.
        """
        if self._check_selected_count():
            self._handle_show_settings_view()
        else:
            return


    # Layout image and colors

    def load_colors_and_image(self, style):
        """Loads theme, background and button colors. 
        Sets Label for top image'.
        """
        style.theme_use("clam")
        style.configure('TFrame', background='white') 
        style.configure('TLabel', background='white')
        style.configure('Dodger.TButton', foreground='black', background='dodger blue')

        image = Image.open("./src/ui/background.png")
        self.bg_image = ImageTk.PhotoImage(image)

        self.label_img = ttk.Label(self._frame, image=self.bg_image)
        self.label_img.grid(column=0, row=0, columnspan=5)

    # Frame

    def _initialize(self):
        """Initializes the frame view.
        Sets titles and text fields
        Actions:
            load_colors_and_image: Loads colors and image on layout
            _initialize_error_msg: Label for error message
            _initialize_stations_list: List of all stations
            _initialize_select_clear_buttons: Buttons Add to> and <Clear all
            _initialize_selected: List of selected stations
            _initialize_continue_to_settings: Button Continue>
            grid_columnconfigure: Grid size configurations
            grid_rowconfigure: Grid size configurations
            """

        self._frame = ttk.Frame(master=self._root)
        style = ttk.Style(self._frame)
        self.load_colors_and_image(style)

        # Title of the window
        self.station_label = ttk.Label(master=self._frame, text="Select station",
                                       font=('Arial', 24, 'bold'))
        self.station_label.grid(column=0, row=1, columnspan=5,
                                padx=10, pady=10, sticky=constants.NW)

        self._initialize_error_msg()

        # Title of left field
        self.note1_label = ttk.Label(master=self._frame, text="Select 1 station at the time",
                                     font=('Arial', 12, 'bold'))
        self.note1_label.grid(column=0, row=3, columnspan=2,
                              padx=10, pady=10, sticky=constants.W)

        # Title of right field
        self.note2_label = ttk.Label(master=self._frame,
                                     text="Selected stations (max 5)                    ",
                                     font=('Arial', 12, 'bold'))
        self.note2_label.grid(column=3, row=2, columnspan=2,
                              padx=10, pady=10, sticky=constants.W)

        self._initialize_stations_list()
        self._initialize_select_clear_buttons()
        self._initialize_selected()
        self._initialize_continue_to_settings()

        self._frame.grid_columnconfigure(0, weight=1, minsize=100)
        self._frame.grid_columnconfigure(1, weight=1, minsize=100)
        self._frame.grid_columnconfigure(2, weight=1, minsize=100)
        self._frame.grid_columnconfigure(3, weight=1, minsize=100)
        self._frame.grid_columnconfigure(4, weight=1, minsize=100)
        self._frame.grid_rowconfigure(0, weight=1, minsize=20)
