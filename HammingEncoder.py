from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
import main
import program


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


class CreditosPopup(Popup):
    pass


class TablaConversionPopup(Popup):
    pass


class HammingEncoderApp(App):
    def build(self):
        return HammingEncoder()

    def on_start(self):
        # INICIALIZA LA APLICACION CON VALORES PREDETERMINADOS NECESARIOS COMO
        # LOS HEADERS DE LAS TABLAS,EL TAMANO DE LA APLICACION
        header_paridad = self.root.ids.header_paridad
        header_paridad2 = self.root.ids.header_paridad2
        headers = ['P1', 'P2', 'D1', 'P3', 'D2', 'D3', 'D4',
                   'P4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11']
        headers2 = ['Prueba', 'Check Bit']
        for i in range(15):
            header_paridad.add_widget(HeaderLabel(text=str(headers[i])))
        for i in range(15):
            header_paridad2.add_widget(HeaderLabel(text=str(headers[i])))
        for i in range(2):
            header_paridad2.add_widget(HeaderError(text=str(headers2[i])))

        self.root_window.size = (1000, 600)

    # FUNCION
    # Esta funcion procesa el numero y calcula sus conversiones
    def calcular(self, num_bin):
        # Crea las validaciones necesarias
        if (num_bin == '' or program.es_hex_invalido(num_bin)):
            popup = Popup(title='Alerta', content=Label(
                text="Numero hexadecimal erroneo"), size_hint=(None, None), size=(400, 200))
            popup.open()
        else:

            # Llama diversas funciones para retornar su resultado y expresarlo en la GUI
            self.root.ids.resultado.text = str(program.hexaToBin(num_bin))
            num_dec, num_bin, num_oct = program.hexaToTabla(num_bin)

            # Crea una lista de las conversiones para mostrarlas en pantalla
            listaNumeros = [num_dec, num_bin, num_oct]

            # Abre el popup de conversiones
            popup = TablaConversionPopup()
            tabla_conversiones = popup.ids.tabla_conversiones
            tabla_conversiones.clear_widgets()

            header_conv = ['Decimal', 'Binario', 'Octal']
            for i in range(3):
                tabla_conversiones.add_widget(
                    HeaderConversion(text=str(header_conv[i])))
            # Itera la lista de conversiones para rellenar la tabla
            for i in range(len(listaNumeros)):
                tabla_conversiones.add_widget(
                    ConversionNumbers(text=str(listaNumeros[i])))
            button = Button(text="OK", size_hint=(None, None), size=(
                150, 50), font_name='Dependencias\Minecraft.ttf', background_color=(0, 0, 0, 1))
            button.bind(on_press=lambda instance: popup.dismiss())
            tabla_conversiones.add_widget(button)
            popup.open()

    # FUNCION
    # Crea la senalNRZL
    def senalNRZL(self, num_bin):
        if (num_bin == '' or program.es_hex_invalido(num_bin)):
            popup = Popup(title='Alerta', content=Label(
                text="Numero hexadecimal erroneo"), size_hint=(None, None), size=(400, 200))
            popup.open()
        else:
            program.nrzi_encoding(program.hexaToBin(num_bin))

    # FUNCION
    # Abre el popup para generar el error en la codificacion Hamming
    def generarErrorPopup(self, num_bin):
        if (num_bin == ''):
            popup = Popup(title='Alerta', content=Label(
                text="Agrega el numero binario de 11 bits para editarlo"), size_hint=(None, None), size=(400, 200))
            popup.open()
        else:
            generarErrorPopup = GenerarErrorPopup()
            generarErrorPopup.open()

    # FUNCION
    def generarError(self, bit_posicion, bin_bit, num_bin):
        num_bin2 = program.hexaToBin(num_bin)
        if (bit_posicion == 'Posicion' or bin_bit == 'Error bit'):
            popup = Popup(title='Alerta', content=Label(
                text="Agregue la posicion del bit o el binario faltante"), size_hint=(None, None), size=(400, 200))
            popup.open()
        else:
            result, table = main.hamming_encode(num_bin2)
            codigo_error = [int(caracter) for caracter in result]

            if (codigo_error[int(bit_posicion) - 1] == int(bin_bit)):
                print(codigo_error, int(bin_bit))
                popup = Popup(title='Alerta', content=Label(
                    text="Intente ingresar otra posicion para generar el error"), size_hint=(None, None), size=(400, 200))
                popup.open()
            else:

                bit_check = self.root.ids.bit_check
                compro_box = self.root.ids.compro_box
                tabla_errores = self.root.ids.tabla_errores
                
                tabla_errores.clear_widgets()
                compro_box.clear_widgets()
                bit_check.clear_widgets()

                codigo_error[int(bit_posicion) - 1] = int(bin_bit)
                print(codigo_error)
              

                for i in range(len(codigo_error)):
                    tabla_errores.add_widget(
                        TablaLabel(text=str(codigo_error[i])))

                decoded_value, parity_table = main.hamming_decode(codigo_error)
                for tupla in parity_table:
                    tercer_elemento = tupla[2]
                    tercer_elemento.insert(0, ' ')
                    print(tercer_elemento)

                for tupla in parity_table:
                    tercer_elemento = tupla[2]
                    for elemento in tercer_elemento:
                        tabla_errores.add_widget(
                            TablaLabel(text=str(elemento)))

                lista_bits_paridad = [str(tupla[1]) for tupla in parity_table]
                for i in range(4):
                    bit_check.add_widget(CheckBitLabel(
                        text=str(lista_bits_paridad[i])))

                lista_comprobacion = [str(tupla[3]) for tupla in parity_table]
                for i in range(4):
                    compro_box.add_widget(CheckBitLabel(
                        text=str(lista_comprobacion[i])))

   # FUNCION
    # Genera la tabla de paridad de Hamming 15 11

    def generarTablaParidad(self, num_bin,paridad):
        if (num_bin == ''or program.es_hex_invalido(num_bin) or paridad == 'Paridad'):
            popup = Popup(title='Alerta', content=Label(
                text="Agrega una paridad o el numero hexadecimal faltante"), size_hint=(None, None), size=(400, 200))
            popup.open()
        else:

            label_paridad = self.root.ids.label_paridad
            label_paridad.text = '=> ' + paridad

            tabla_paridad = self.root.ids.tabla_paridad
            tabla_paridad.clear_widgets()
            num_bin2 = program.hexaToBin(num_bin)

            resultado, data = main.hamming_encode(num_bin2,paridad)
            
            lista_bits = list(num_bin2)

        # Agregar los ceros en las posiciones indicadas
            for i in (0, 1, 3, 7):
                lista_bits.insert(i, ' ')

            bitsParidad = ''.join(lista_bits)

            for i in range(15):
                tabla_paridad.add_widget(TablaLabel(text=bitsParidad[i]))

        # Agrega los P1,P2,P3,P4
            listaP = []
            for fila in data:
                listaP.append(fila[:-1])

            listaPString = []
            for lista in listaP:
                string = ''.join(str(elemento) for elemento in lista)
                # eliminamos también la coma y el espacio antes del último elemento
                listaPString.append(string)

            print(listaPString)

            for i in range(4):
                for j, char in enumerate(listaPString[i]):
                    tabla_paridad.add_widget(TablaLabel(text=char))

    # Agregar los elementos de la lista resultado a la última fila
            for i in range(15):
                tabla_paridad.add_widget(TablaLabel(text=str(resultado[i])))

    def creditos(self):
        popup = CreditosPopup()
        popup.open()


if __name__ == '__main__':
    HammingEncoderApp().run()
