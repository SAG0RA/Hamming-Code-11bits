import matplotlib.pyplot as plt

def es_hex_invalido(num_hex):
    try:
        # Convertimos el número hexadecimal a entero
        num_int = int(num_hex, 16)

        # Verificamos si el número está dentro del rango de 000 a 7FF
        if 0 <= num_int <= 2047:
            return False
        else:
            return True
    except ValueError:
        # Si no se puede convertir a entero, el número hexadecimal no es válido
        return True
    
def hexaToTabla(num_hex):
    # Convertimos el número hexadecimal a binario
    num_bin = bin(int(num_hex, 16))[2:]
    num_dec = int(num_hex, 16)
    num_oct = oct(num_dec)[2:]
        
    # Añadimos ceros a la izquierda si el número binario tiene menos de 11 bits
    while len(num_bin) < 11:
        num_bin = "0" + num_bin
        
    return num_bin, num_dec, num_oct

def hexaToBin(num_hex):
    # Convertimos el número hexadecimal a binario
    num_bin = bin(int(num_hex, 16))[2:]
    num_dec = int(num_hex, 16)
    num_oct = oct(num_dec)[2:]
        
    # Añadimos ceros a la izquierda si el número binario tiene menos de 11 bits
    while len(num_bin) < 11:
        num_bin = "0" + num_bin
        
    return num_bin

def nrzi_encoding(binary_data):
    # Suponemos que la señal está en nivel bajo antes de t=0
    signal_level = 0

    # Inicializamos las listas de tiempo y amplitud de la señal
    time = [0]
    amplitude = [0]

    # Recorremos cada bit del número binario de entrada
    for bit in binary_data:
        # Si el bit es un 1, invertimos el nivel de la señal
        if bit == '1':
            signal_level = not signal_level

        # Añadimos el tiempo y la amplitud correspondiente al nivel actual de la señal
        time.append(time[-1])
        amplitude.append(signal_level)
        time.append(time[-1] + 1)
        amplitude.append(signal_level)

    # Mostramos la figura de la señal codificada
    plt.step(time, amplitude, where='post')
    plt.title('Codificación NRZI de ' + binary_data)
    plt.xlabel('Tiempo')
    plt.ylabel('Nivel de señal')
    plt.ylim(-0.2, 1.2)
    plt.show()
