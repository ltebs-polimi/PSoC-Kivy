from kivy.properties import NumericProperty, ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from communication import KivySerial

class Toolbar(BoxLayout):
    """
    @brief Lateral toolbar widget.

    The toolbar widget is used to show some
    settings related to the app.
    """

    """
    @brief String used to send messages to bottom bar.
    """
    message_string = StringProperty("")

    def __init__(self, **kwargs):
        super(Toolbar, self).__init__(**kwargs)

    def wave_select_dialog(self):
        """
        @brief Open popup for wave selection.
        """
        self.message_string = "Wave Select Dialog"
        popup = WaveSelectDialog()
        popup.open()

    def range_select_dialog(self):
        """
        @brief Open popup for range selection.
        """
        self.message_string = "Range Select Dialog"
        popup = RangeSelectDialog()
        popup.open()


class WaveSelectDialog(Popup):
    """
    @brief Popup to allow wave selection 
    """
    wave_select_spinner = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(WaveSelectDialog, self).__init__(**kwargs)
        self.board = KivySerial()

    def update_pressed(self):
        """
        @brief Callback called when update button is pressed.

        If the board is connected, update the wave selection.
        """
        if (self.board.is_connected()):
            self.board.select_wave(self.wave_select_spinner.text)
        self.dismiss()

class RangeSelectDialog(Popup):
    """
    @brief Popup to allow range selection 
    """
    range_spinner = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(RangeSelectDialog, self).__init__(**kwargs)
        self.board = KivySerial()

    def update_pressed(self):
        """
        @brief Callback called when update button is pressed.

        If the board is connected, update the range selection.
        """
        if (self.board.is_connected()):
            self.board.select_range(self.range_spinner.text)
        self.dismiss()