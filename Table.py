from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

class Table(GridLayout):
    def __init__(self, number, **kwargs):
        super(Table, self).__init__(**kwargs)

        # Configurar la estructura de la tabla
        self.cols = 3
        self.rows = 4

        # Agregar celdas a la tabla
        for i in range(1, self.rows+1):
            for j in range(1, self.cols+1):
                self.add_widget(Label(text=f'Fila {i}, Columna {j}'))




class MyApp(App):
    def build(self):
        return Table()


if __name__ == '__main__':
    MyApp().run()
