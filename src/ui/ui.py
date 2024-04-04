from ui.station_view import StationView


class UI:
    """Sovelluksen käyttöliittymästä vastaava luokka."""

    def __init__(self, root):
        """Luokan konstruktori. Luo uuden käyttöliittymästä vastaavan luokan.

        Args:
            root:
                TKinter-elementti, jonka sisään käyttöliittymä alustetaan.
        """
        self._root = root
        self._current_view = None

    def start(self):
        """Käynnistää käyttöliittymän."""
        self._show_station_view()

    def _hide_current_view(self):
        if self._current_view:
            self._current_view.destroy()

        self._current_view = None

    def _show_station_view(self):
#        self._hide_current_view()

        self._current_view = StationView(
            self._root
        )

        self._current_view.pack()

print("UI\n")