from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import BooleanProperty, ObjectProperty, NumericProperty
import re
from kivy.garden.graph import MeshLinePlot, LinePlot
from kivy.graphics import Color, Rectangle

class GraphTabs(TabbedPanel):
    """
    @brief Main tabbed panel to show tabbed items.
    """

    """
    @brief Wav dac plot tabbed panel.
    """
    wave_dac_tab = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(GraphTabs, self).__init__(**kwargs)

    def update_plot(self, value):
        """
        @brief Function called to update the plots in the tabbed panel.
        """
        self.wave_dac_tab.update_plot(value)

class GraphPanelItem(TabbedPanelItem):
    """
    @brief Item for a tabbed panel in which a graph is shown.
    """

    """
    @brief Graph widget.
    """
    graph = ObjectProperty(None)

    """
    @brief Plot settings widget.
    """
    plot_settings = ObjectProperty(None)

    """
    @brief Refresh rate: ~ 50 fps (100 Hz/2)
    """
    n_points_per_update = NumericProperty(2)

    def __init__(self, **kwargs):
        super(GraphPanelItem, self).__init__(**kwargs)
        self.n_seconds = 20          # Initial number of samples to be shown
        self.n_points_collected = [] # Number of new collected points
        self.sample_rate = 100       # Sample rate for data streaming

    def on_graph(self, instance, value):
        """
        @brief Callback called when graph widget is ready.
        """
        self.graph.xmin = -self.n_seconds
        self.graph.xmax = 0
        self.graph.xlabel = 'Time (s)'
        self.graph.x_ticks_minor = 1
        self.graph.x_ticks_major = 5
        self.graph.y_ticks_minor = 1
        self.graph.y_ticks_major = 1
        self.graph.x_grid_label = True
        self.graph.ymin = 0
        self.graph.ymax = 5
        self.graph.y_grid_label = True
        # Compute number of points to show
        self.n_points = self.n_seconds * self.sample_rate  # Number of points to plot
        # Compute time between points on x-axis
        self.time_between_points = (self.n_seconds)/float(self.n_points)
        # Initialize x and y points list
        self.x_points = [x for x in range(-self.n_points, 0)]
        for j in range(self.n_points):
            self.x_points[j] = -self.n_seconds + j * self.time_between_points
        self.y_points = [0 for y in range(-self.n_points, 0)]

    def on_plot_settings(self, instance, value):
        """
        @brief Callback called when plot_settings widget is ready.

        Bint several properties together.
        """
        self.plot_settings.bind(n_seconds=self.graph.setter('xmin'))
        self.plot_settings.bind(ymin=self.graph.setter('ymin'))
        self.plot_settings.bind(ymax=self.graph.setter('ymax'))

    def update_plot(self, value):
        """
        @brief Update plot based on value and refresh rate.
        """
        self.n_points_collected.append(value)
        if (len(self.n_points_collected) == self.n_points_per_update):
            for val in self.n_points_collected:
                self.y_points.append(self.y_points.pop(0))
                self.y_points[-1] = val
            self.plot.points = zip(self.x_points, self.y_points)
            self.n_points_collected = []

class WaveDACPlot(GraphPanelItem):
    """
    @brief Tabbed panel item to show wave dac data.
    """
    def on_graph(self, instance, value):
        super(WaveDACPlot, self).on_graph(instance, value)
        self.graph.ylabel = 'Amplitude (V)'
        self.plot = LinePlot(color=(0.75, 0.4, 0.4, 1.0))
        self.plot.line_width = 2
        self.plot.points = zip(self.x_points, self.y_points)
        self.graph.add_plot(self.plot)

class PlotSettings(BoxLayout):
    """
    @brief Class to show some settings related to the plot.
    """

    """
    @brief Number of seconds to show on the plot.
    """
    seconds_spinner = ObjectProperty(None)
    
    """
    @brief Minimum value for y axis text input widget.
    """
    ymin_input = ObjectProperty(None)

    """
    @brief Maximum value for y axis text input widget.
    """
    ymax_input = ObjectProperty(None)

    """
    @brief Current number of seconds shown.
    """
    n_seconds = NumericProperty(0)

    """
    @brief Numeric value of ymin axis minimum value.
    """
    ymin = NumericProperty(0)

    """
    @brief Numeric value of ymin axis maximum value.
    """
    ymax = NumericProperty(5)

    def __init__(self, **kwargs):
        super(PlotSettings, self).__init__(**kwargs)
        self.n_seconds = 20

    def on_seconds_spinner(self, instance, value):
        """
        @brief Bind change on seconds spinner to callback.
        """
        self.seconds_spinner.bind(text=self.spinner_updated)

    def on_ymin_input(self, instance, value):
        """
        @brief Bind enter pressed on ymin text input to callback.
        """
        self.ymin_input.bind(enter_pressed=self.axis_changed)

    def on_ymax_input(self, instance, value):
        """
        @brief Bind enter pressed on on ymax text input to callback.
        """
        self.ymax_input.bind(enter_pressed=self.axis_changed)

    def spinner_updated(self, instance, value):
        """
        @brief Get new value of seconds to show on the plot.
        """
        self.n_seconds = -int(self.seconds_spinner.text)

    def axis_changed(self, instance, focused):
        """
        @brief Called when a new value of ymin or ymax is entered on the GUI.
        """
        if (not focused):
            if (not ((self.ymin_input.text == '') or (self.ymax_input.text == ''))):
                y_min = float(self.ymin_input.text)
                y_max = float(self.ymax_input.text)
                if (y_min >= y_max):
                    self.ymin_input.text = f"{self.ymin:.2f}"
                    self.ymax_input.text = f"{self.ymax:.2f}"
                else:
                    self.ymin = y_min
                    self.ymax = y_max
            elif (self.ymin_input.text == ''):
                self.ymin_input.text = f"{self.ymin:.2f}"
            elif (self.ymax_input.text == ''):
                self.ymax_input.text = f"{self.ymax:.2f}"


class FloatInput(TextInput):
    """
    @brief Class to allow for positive floating point values in TextInput.
    """
    pat = re.compile('[^0-9]')
    enter_pressed = BooleanProperty(None)

    def __init__(self, **kwargs):
        super(FloatInput, self).__init__(**kwargs)
        self.bind(focus=self.on_focus)
        self.multiline = False

    def insert_text(self, substring, from_undo=False):
        """
        @brief Check the entered text and validate it.
        """
        pat = self.pat

        if '.' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '.'.join([re.sub(pat, '', s) for s in substring.split('.', 1)])

        return super(FloatInput, self).insert_text(s, from_undo=from_undo)

    def on_focus(self, instance, value):
        """
        @brief Callback called when focus changes.
        """
        self.enter_pressed = value

class IntInput(TextInput):
    """
    @brief Class to allow for positive and greater than 0 int values in TextInput.
    """
    pat = re.compile('[^1-9]')
    enter_pressed = BooleanProperty(None)

    def __init__(self, **kwargs):
        super(IntInput, self).__init__(**kwargs)
        self.bind(focus=self.on_focus)
        self.multiline = False

    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        s = re.sub(pat, '', substring)
        return super(IntInput, self).insert_text(s, from_undo=from_undo)

    def on_focus(self, instance, value):
        self.enter_pressed = value
