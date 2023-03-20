from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout


class HammingEncoder(GridLayout):
    pass


class guiApp(App):
    def build(self):
        return HammingEncoder()

guiApp().run()