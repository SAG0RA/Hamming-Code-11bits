import matplotlib.pyplot as plt

# cadena de prueba 11001101011
# pariedad impar == 1

#0 representa paridad par, 1 paridad impar
def verificar_paridad(binario):
    unos = binario.count('1')
    if unos % 2 == 0:
        return 0
    else:
        return 1


def verificar_binario(num_bin):
    """Verifica que el número ingresado sea binario y tenga 11 bits."""
    if len(num_bin) != 11:
        print("El número ingresado no tiene 11 bits.")
        return False
    elif not all(d in "01" for d in num_bin):
        print("El número ingresado no es binario.")
        return False
    else:
        return True


def verificar_rango(num_dec):
    """Verifica que el número decimal esté en el rango permitido."""
    if num_dec < 0 or num_dec > 2047:
        print("El número ingresado está fuera del rango permitido (0 a 2047).")
        return False
    else:
        return True


def convertir_binario_a_hexadecimal(num_bin):
    """Convierte el número binario a hexadecimal con un formato de 3 dígitos."""
    num_dec = int(num_bin, 2)
    num_hex = format(num_dec, "03X")
    return num_hex


def convertir_hexadecimal_tabla(num_hex):
    """Convierte el número hexadecimal a octal, binario y decimal y muestra los resultados en una tabla."""
    num_dec = int(num_hex, 16)
    num_bin = format(num_dec, "011b")
    num_oct = format(num_dec, "o")

    print("Números equivalentes al número hexadecimal", num_hex)
    print("Decimal\t\tBinario\t\tOctal")
    print(f"{num_dec}\t\t{num_bin}\t\t{num_oct}")


def codificar_nrzl(cadena_binaria):
    """Codifica una cadena binaria utilizando la codificación NRZ-L."""
    niveles_tension = []
    nivel_actual = -1
    for bit in cadena_binaria:
        if bit == '0':
            niveles_tension.append(nivel_actual)
        else:
            nivel_actual *= -1
            niveles_tension.append(nivel_actual)
    return niveles_tension


def graficar_codigo_nrzl(cadena_binaria):
    # Convertimos el número binario a niveles de tensión utilizando NRZ-L
    niveles_tension = codificar_nrzl(cadena_binaria)

    # Graficamos la señal
    plt.plot(range(len(niveles_tension)), niveles_tension, drawstyle='steps-pre')
    plt.xlabel('Tiempo (bits)')
    plt.ylabel('Nivel de tensión')
    plt.ylim(-1.5, 1.5)
    plt.show()


def nrzi_plot(binary_string):
    signal = [1]  # Comenzamos con un nivel alto
    for bit in binary_string:
        if bit == '0':
            signal.append(signal[-1])  # No cambia el nivel
        else:
            signal.append(-signal[-1])  # Cambia el nivel

    plt.plot(signal)
    plt.ylim(-1.5, 1.5)  # Limitamos el eje y a dos niveles
    plt.title("Código NRZI de {}".format(binary_string))
    plt.xlabel("Tiempo")
    plt.ylabel("Nivel de señal")
    plt.show()


def hamming_decode(encoded_bits):
    # Calcula el número de bits de paridad necesarios
    num_parity_bits = 0
    while 2 ** num_parity_bits <= len(encoded_bits):
        num_parity_bits += 1

    # Inicializa la tabla de paridad
    parity_table = []
    for i in range(num_parity_bits):
        # Obtiene los bits correspondientes a esta posición de paridad
        parity_bits = [encoded_bits[j]
                       for j in range(len(encoded_bits)) if (j+1) & (2**i)]
        # Calcula la paridad para estos bits
        parity = sum(parity_bits) % 2
        # Agrega la entrada a la tabla de paridad
        used_bits = [encoded_bits[j] for j in range(
            len(encoded_bits)) if (j+1) & (2**i) and j != (2**i)-1]
        parity_table.append(
            (i+1, parity, used_bits, "correcto" if parity == encoded_bits[(2**i)-1] else "error"))

    # Invierte la lista de bits para facilitar el procesamiento
    encoded_bits = list(reversed(encoded_bits))

    # Inicializa el valor decodificado
    decoded_value = []

    # Decodifica cada bit
    for i in range(num_parity_bits, len(encoded_bits)):
        # Ignora los bits de paridad
        if (i+1) & i:
            decoded_value.append(encoded_bits[i])

    # Invierte el valor decodificado y devuelve el valor y la tabla de paridad
    return list(reversed(decoded_value)), parity_table


def programa(paridad,num_bin):
    """Función principal que solicita al usuario un número binario y lo convierte a hexadecimal."""
    # while True:
        # paridad = int(input("Ingrese un 0 si desea paridad par o 1 si desea impar: \n"))
        # num_bin = input("Ingrese un número binario de 11 bits: ")
    if verificar_binario(num_bin) and (paridad == verificar_paridad(num_bin)):
        num_hex = convertir_binario_a_hexadecimal(num_bin)
        if verificar_rango(int(num_bin, 2)):
            print(
                f"El número binario {num_bin} es equivalente al número hexadecimal {num_hex}.")
            convertir_hexadecimal_tabla(num_hex)
            #graficar_codigo_nrzl(num_bin)


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
        time.append(time[-1] + 1)
        amplitude.append(signal_level)

    # Mostramos la figura de la señal codificada
    plt.plot(time, amplitude)
    plt.title('Codificación NRZI de ' + binary_data)
    plt.xlabel('Tiempo')
    plt.ylabel('Nivel de señal')
    plt.ylim(-0.2, 1.2)
    plt.show()


def nrzi_encoding2(binary_data):
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


def test():
    # Decoding a Hamming code.
    # codigo = "0110101"
    # code, table = hamming_encode(codigo)
    # print('Palabra de código:', code)
    # print('Tabla de paridad:')
    # for row in table:
    #     print(row)
    # bits = [1, 0, 1, 1, 0, 1, 0]
    # decoded_value, parity_table = hamming_decode(bits)
    # print("Valor decodificado:", decoded_value)
    # print("Tabla de paridad:")
    # for entry in parity_table:
    #     print(
    #         f"Bit {entry[0]}: Paridad {entry[1]}, bits utilizados: {entry[2]} ({entry[3]})")
    bits = '10100101011'
    nrzi_encoding2(bits)

if __name__ == '__main__':
    test()
