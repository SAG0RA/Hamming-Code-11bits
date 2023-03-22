from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
import main

class TablaParidadPopup(Popup):
    pass

class HammingEncoder(FloatLayout):
    pass


class HammingEncoderApp(App):
    
    def build(self):
        return HammingEncoder()
    
    def on_start(self):
        header_paridad = self.root.ids.header_paridad
        headers = ['P1','P2','D1','P3','D2','D3','D4','P4','D5','D6','D7','D8','D9','D10','D11']
        for i in range(15):
            header_paridad.add_widget(HeaderLabel(text=str(headers[i])))
        self.root_window.size = (1000, 600)
    
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


    def generarTablaParidad(self, num_bin):
        if(num_bin == ''):
            popup = Popup(title='Alerta', content=Label(text="Agrega una paridad o el numero binario\n faltante, asegurate de que coincidan"), size_hint=(None, None), size=(400, 200))
            popup.open()
        else:
            tabla_paridad = self.root.ids.tabla_paridad
            tabla_paridad.clear_widgets()

            resultado,data = main.hamming_encode(num_bin)
            lista_bits = list(num_bin)

        # Agregar los ceros en las posiciones indicadas
            for i in (0,1,4,8):
                    lista_bits.insert(i, '-')
        
            bitsParidad = ''.join(lista_bits)
            print(data)
        
            for i in range(15):
                tabla_paridad.add_widget(TablaLabel(text=bitsParidad[i]))      
        
        #Agrega los P1,P2,P3,P4
            listaP = []
            for fila in data:
                listaP.append(fila[:-1])

            listaPString = []
            for lista in listaP:
                string = ''.join(str(elemento) for elemento in lista)
                listaPString.append(string) # eliminamos también la coma y el espacio antes del último elemento
        
            print(listaPString)
        
            for i in range(4):
                for j, char in enumerate(listaPString[i]):
                    tabla_paridad.add_widget(TablaLabel(text=char))
                

    # Agregar los elementos de la lista resultado a la última fila
            for i in range(15):
                tabla_paridad.add_widget(TablaLabel(text=str(resultado[i])))

    


class TablaLabel(Label):
    pass
class HeaderLabel(Label):
    pass

if __name__ == '__main__':
    HammingEncoderApp().run()