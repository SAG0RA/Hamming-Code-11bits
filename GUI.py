from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.video import Video
from Table import Table
import main


class HammingEncoder(FloatLayout):
    pass


class HammingEncoderApp(App):
    
    def build(self):
        return HammingEncoder()
    
    def on_start(self):
        self.root_window.size = (395, 600)
    
    def validar_entrada_binaria(self, instancia):
        caracteres_permitidos = set('01')
        if not all(c in caracteres_permitidos for c in instancia.text) or len(instancia.text) > 11:
            instancia.text = instancia.text[:-1]

    def calcular(self,paridad_text,num_bin):
        
        if(paridad_text == 'Paridad' or num_bin == ''):
            popup = Popup(title='Alerta', content=Label(text="Agrega una paridad o el numero binario\n faltante, asegurate de que coincidan"), size_hint=(None, None), size=(400, 200))
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

    def senalNRZL(self,paridad_text, num_bin):
        if(paridad_text == 'Paridad' or num_bin == ''):
            popup = Popup(title='Alerta', content=Label(text="Agrega una paridad o el numero binario\n faltante, asegurate de que coincidan"), size_hint=(None, None), size=(400, 200))
            popup.open()
        else:
            if(paridad_text == 'par'):
                paridad = 0
            else: 
                paridad = 1
            
            if(main.verificar_paridad(num_bin) == paridad):
                main.graficar_codigo_nrzl(num_bin)
            else:
                popup = Popup(title='Alerta', content=Label(text="La paridad no coincide con el numero binario ingresado"), size_hint=(None, None), size=(400, 200))
                popup.open()
    
    def show_popup(self):
        self.ids.popup.open()
    
    def show_table(self, paridad_text, num_bin):
        # Crear contenido del Popup
        # Numero de prueba para la tabla, reemplazar por num_bin
        content = Table("11001101011")

        # Crear el Popup y mostrarlo
        popup = Popup(title="Tabla", content=content, size_hint=(0.9, 0.9))
        popup.open()


if __name__ == '__main__':
    HammingEncoderApp().run()