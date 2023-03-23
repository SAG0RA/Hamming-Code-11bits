from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
import main

class CheckBitLabel(Label):
    pass
class ConversionNumbers(Label):
    pass
class HeaderConversion(Label):
    pass
class HeaderError(Label):
    pass
class HammingEncoder(FloatLayout):
    pass
class TablaLabel(Label):
    pass
class HeaderLabel(Label):
    pass
class GenerarErrorPopup(Popup):
    pass
class TablaConversionPopup(Popup):
    pass
class HammingEncoderApp(App):
    def build(self):
        return HammingEncoder()
    
    def on_start(self):
        #INICIALIZA LA APLICACION CON VALORES PREDETERMINADOS NECESARIOS COMO
        #LOS HEADERS DE LAS TABLAS,EL TAMANO DE LA APLICACION
        header_paridad = self.root.ids.header_paridad
        header_paridad2 = self.root.ids.header_paridad2
        headers = ['P1','P2','D1','P3','D2','D3','D4','P4','D5','D6','D7','D8','D9','D10','D11']
        headers2 = ['Prueba','Check Bit']
        for i in range(15):
            header_paridad.add_widget(HeaderLabel(text=str(headers[i])))
        for i in range(15):
            header_paridad2.add_widget(HeaderLabel(text=str(headers[i])))
        for i in range(2):
            header_paridad2.add_widget(HeaderError(text=str(headers2[i])))

        self.root_window.size = (1000, 600)
    
    #FUNCION
    #Esta funcion se encarga de validar el numero binario a procesar
    def validar_entrada_binaria(self, instancia):
        caracteres_permitidos = set('01')
        if not all(c in caracteres_permitidos for c in instancia.text) or len(instancia.text) > 11:
            instancia.text = instancia.text[:-1]

    #FUNCION
    #Esta funcion procesa el numero y calcula sus conversiones
    def calcular(self,paridad_text,num_bin):
        #Crea las validaciones necesarias
        if(paridad_text == 'Paridad' or num_bin == ''):
            popup = Popup(title='Alerta', content=Label(text="Agrega una paridad o el numero binario\n faltante, asegurate de que coincidan"), size_hint=(None, None), size=(400, 200))
            popup.open()
        else:
            if(paridad_text == 'par'):
                paridad = 0
            else: 
                paridad = 1
            
            if(main.verificar_paridad(num_bin) == paridad):
                #Manda los valores para que sean procesados en la logica
                main.programa(paridad,num_bin)
                #Llama diversas funciones para retornar su resultado y expresarlo en la GUI
                self.root.ids.resultado.text = main.convertir_binario_a_hexadecimal(num_bin)
                num_dec,num_bin,num_oct = main.convertir_hexadecimal_tabla(num_bin)

                #Crea una lista de las conversiones para mostrarlas en pantalla
                listaNumeros = [num_dec,num_bin,num_oct]
                
                #Abre el popup de conversiones
                popup = TablaConversionPopup()
                tabla_conversiones = popup.ids.tabla_conversiones
                tabla_conversiones.clear_widgets()

                header_conv = ['Decimal','Binario','Octal']
                for i in range(3):
                    tabla_conversiones.add_widget(HeaderConversion(text=str(header_conv[i])))
                #Itera la lista de conversiones para rellenar la tabla
                for i in range(len(listaNumeros)):
                    tabla_conversiones.add_widget(ConversionNumbers(text=str(listaNumeros[i])))
                button = Button(text="OK", size_hint=(None, None), size=(150, 50), font_name='Dependencias\Minecraft.ttf', background_color=(0, 0, 0, 1))
                button.bind(on_press=lambda instance: popup.dismiss())
                tabla_conversiones.add_widget(button)
                popup.open()

            else:
                popup = Popup(title='Alerta', content=Label(text="La paridad no coincide con el numero binario ingresado"), size_hint=(None, None), size=(400, 200))
                popup.open()

    #FUNCION
    #Crea la senalNRZL
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
                main.nrzi_encoding2(num_bin)
            else:
                popup = Popup(title='Alerta', content=Label(text="La paridad no coincide con el numero binario ingresado"), size_hint=(None, None), size=(400, 200))
                popup.open()
    
    #FUNCION
    #Abre el popup para generar el error en la codificacion Hamming
    def generarErrorPopup(self,num_bin):
        if(num_bin == ''):
            popup = Popup(title='Alerta', content=Label(text="Agrega el numero binario de 11 bits para editarlo"), size_hint=(None, None), size=(400, 200))
            popup.open()
        else:
            generarErrorPopup = GenerarErrorPopup()
            generarErrorPopup.open()
    
    #FUNCION
    def generarError(self,bit_posicion,bin_bit,num_bin):
        print(num_bin)
        if(bit_posicion == 'Posicion' or bin_bit == 'Error bit'):
            popup = Popup(title='Alerta', content=Label(text="Agregue la posicion del bit o el binario faltante"), size_hint=(None, None), size=(400, 200))
            popup.open()
        else:
            result,table = main.hamming_encode(num_bin)
            codigo_error = [int(caracter) for caracter in result]

            if(codigo_error[int(bit_posicion) - 1] == int(bin_bit)):
                print(codigo_error,int(bin_bit))
                popup = Popup(title='Alerta', content=Label(text="Intente ingresar otra posicion para generar el error"), size_hint=(None, None), size=(400, 200))
                popup.open()
            else:
                tabla_errores = self.root.ids.tabla_errores
                tabla_errores.clear_widgets()

                codigo_error[int(bit_posicion) - 1] = int(bin_bit)
                decoded_value, parity_table = main.hamming_decode(codigo_error)

                for i in range(15):
                    tabla_errores.add_widget(TablaLabel(text=str(codigo_error[i])))
                
                for tupla in parity_table:
                    tercer_elemento = tupla[2]
                    tercer_elemento.insert(0, ' ')
                    print(tercer_elemento)
                
                
                for tupla in parity_table:
                    tercer_elemento = tupla[2]
                    for elemento in tercer_elemento:
                        tabla_errores.add_widget(TablaLabel(text=str(elemento)))
                
                bit_check = self.root.ids.bit_check
                lista_bits_paridad = [str(tupla[1]) for tupla in parity_table]
                for i in range(4):
                    bit_check.add_widget(CheckBitLabel(text=str(lista_bits_paridad[i])))
                
                compro_box = self.root.ids.compro_box
                lista_comprobacion = [str(tupla[3]) for tupla in parity_table]
                for i in range(4):
                    compro_box.add_widget(CheckBitLabel(text=str(lista_comprobacion[i])))

                
    


   #FUNCION
    #Genera la tabla de paridad de Hamming 15 11
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
            for i in (0,1,3,7):
                    lista_bits.insert(i, ' ')
        
            bitsParidad = ''.join(lista_bits)
        
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
                


if __name__ == '__main__':
    HammingEncoderApp().run()