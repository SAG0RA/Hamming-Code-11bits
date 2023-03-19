from kivy.app import App
from kivy.uix.widget import Widget


class HammingCode(Widget):
    pass


class HammingApp(App):
    def build(self):
        return HammingCode()

HammingApp().run()