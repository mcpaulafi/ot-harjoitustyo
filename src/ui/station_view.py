from tkinter import ttk, StringVar, constants, Listbox, Scrollbar
from services.station_service import station_service
from database_connection import get_database_connection


class StationView:
    """Station list view."""

    def __init__(self, root):
        """Class constructor. Creates new view for stations.

        Args:
            root:
                TKinter element, in which view is installed.
        """

        self._root = root
        self._frame = None

        self._initialize()

    def pack(self):
        """"Shows the view."""
        self._frame.pack(fill=constants.X)

    def destroy(self):
        """"Destroys the view."""
        self._frame.destroy()

    def station_list(self):
        """Gets stations from the database and returns them as a list."""
        stations = station_service.get_stations()
        stations_list = []
        for s in stations:
            if s.name != "Name":
                stations_list.append((s.station_id, s.name))
        return stations_list

    def _initialize_station_list_field(self):
        """Creates a view with stations in a listbox"""
        stations_list = self.station_list()
        print("list", stations_list[3])

        station_label = ttk.Label(master=self._frame, text="Select your stations", 
                                  font=('Arial',24,'bold'))
        station_label.grid(padx=5, pady=5, sticky=constants.W)

        list_label = Listbox(master=self._frame, selectmode="multiple", 
        height=10, width=30
        )

        for s in stations_list:
            list_label.insert(s[0], s[1])

        list_label.grid(padx=50, pady=5, sticky=constants.W)

    def _initialize(self):
        """Initializes the frame view"""
        self._frame = ttk.Frame(master=self._root)

        self._initialize_station_list_field()

        self._frame.grid_columnconfigure(0, weight=1, minsize=400)


print("STATIONVIEW\n")