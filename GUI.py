from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
import main


class HammingEncoder(FloatLayout):
    pass


class HammingEncoderApp(App):
    def build(self):
        return HammingEncoder()
    
    def validar_entrada_binaria(self, instancia):
        caracteres_permitidos = set('01')
        if not all(c in caracteres_permitidos for c in instancia.text) or len(instancia.text) > 11:
            instancia.text = instancia.text[:-1]

    def calcular():
        main.programa()   
    

HammingEncoderApp().run()