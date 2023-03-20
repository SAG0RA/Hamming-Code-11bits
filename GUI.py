from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
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

    def calcular(self,paridad_text,num_bin):
        if(paridad_text == 'Paridad'):
            popup = Popup(title='Alerta', content=Label(text="Agrega una paridad, asegurate de que\n    coincida con el numero binario"), size_hint=(None, None), size=(400, 200))
            popup.open()
        else:
            if(paridad_text == 'par'):
                paridad = 0
            else: 
                paridad = 1
            
            if(main.verificar_paridad(num_bin) == paridad):
                main.programa(paridad,num_bin)
                self.root.ids.resultado.text = main.convertir_binario_a_hexadecimal(num_bin)
            else:
                popup = Popup(title='Alerta', content=Label(text="La paridad no coincide con el numero binario ingresado"), size_hint=(None, None), size=(400, 200))
                popup.open()
HammingEncoderApp().run()