from ui.stationlist_view import StationListView
from ui.settings_view import SettingsView
from ui.weather_view import WeatherView


class UI:
    """User interphase class of the application."""

    def __init__(self, root):
        """Class constructor. Creates a new UI class.

        Args:
            root:
                TKinter element, in which UI is installed.
        """
        self._root = root
        self._current_view = None

    def start(self):
        """Starts the UI."""
        self._show_stationlist_view()

    def _hide_current_view(self):
        if self._current_view:
            self._current_view.destroy()

        self._current_view = None

    def _show_stationlist_view(self):
        """Shows station selection view"""
        self._hide_current_view()

        self._current_view = StationListView(
            self._root, self._show_settings_view
        )
        self._current_view.pack()

    def _show_settings_view(self):
        """Shows selected station"""
        self._hide_current_view()

        self._current_view = SettingsView(
            self._root, self._show_weather_view,
            self._show_stationlist_view
        )

        self._current_view.pack()

    def _show_weather_view(self):
        """Shows weather on selected station(s)"""
        self._hide_current_view()

        self._current_view = WeatherView(
            self._root, self._show_stationlist_view,
            self._show_settings_view
        )

        self._current_view.pack()


print("UI\n")
