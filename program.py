import matplotlib.pyplot as plt

def es_hex_valido(num_hex):
    try:
        # Convertimos el número hexadecimal a entero
        num_int = int(num_hex, 16)

        # Verificamos si el número está dentro del rango de 000 a 7FF
        if 0 <= num_int <= 2047:
            return True
        else:
            return False
    except ValueError:
        # Si no se puede convertir a entero, el número hexadecimal no es válido
        return False
    
def hexaToBin(num_hex):
    # Convertimos el número hexadecimal a binario
    num_bin = bin(int(num_hex, 16))[2:]
    num_dec = int(num_hex, 16)
    num_oct = oct(num_dec)[2:]
        
    # Añadimos ceros a la izquierda si el número binario tiene menos de 11 bits
    while len(num_bin) < 11:
        num_bin = "0" + num_bin
        
    return num_bin, num_dec, num_oct

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

def llenarLista(listaDatos):
    posiciones = [0, 1, 3, 7]
    nuevaLista = []
    for i in range(15):
        if i in posiciones:
            nuevaLista.append('')
        else:
            nuevaLista.append(listaDatos[0])
            listaDatos = listaDatos[1::]
    return nuevaLista

def hamming_encode(dato, paridad='par'):
    listaDato = [int(x) for x in dato]
    nuevaLista = llenarLista(listaDato)

    p1 = nuevaLista[2] ^ nuevaLista[4] ^ nuevaLista[6] ^ nuevaLista[8] ^ nuevaLista[10] ^ nuevaLista[12] ^ nuevaLista[14]
    p2 = nuevaLista[2] ^ nuevaLista[5] ^ nuevaLista[6] ^ nuevaLista[9] ^ nuevaLista[10] ^ nuevaLista[13] ^ nuevaLista[14]
    p3 = nuevaLista[4] ^ nuevaLista[5] ^ nuevaLista[6] ^ nuevaLista[11] ^ nuevaLista[12] ^ nuevaLista[13] ^ nuevaLista[14]
    p4 = nuevaLista[8] ^ nuevaLista[9] ^ nuevaLista[10] ^ nuevaLista[11] ^ nuevaLista[12] ^ nuevaLista[13] ^ nuevaLista[14]
    
    listPari = [p1,p2,p3,p4]

    if paridad == 'impar':
        for p in range(4):
            listPari[p] = int(not listPari[p])

    nuevaLista[0] = listPari[0]
    nuevaLista[1] = listPari[1]
    nuevaLista[3] = listPari[2]
    nuevaLista[7] = listPari[3]

    return "".join(str(num) for num in nuevaLista)

def hamming_decode(dato, paridad='par'):
    return

def main():
    numero = '00a'
    if es_hex_valido(numero):
        num_bin, num_dec, num_oct = hexaToBin(numero)
        print(num_bin, num_dec, num_oct)
        # nrzi_encoding(num_bin)
        print(hamming_encode(num_bin, 'impar'))
        
    else:
        print("Error")

if __name__ == '__main__':
    main()