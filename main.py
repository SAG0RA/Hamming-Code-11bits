import operator
import matplotlib.pyplot as plt
from functools import reduce

# cadena de prueba 11001101011
# pariedad impar == 1

#0 representa paridad par, 1 paridad impar
def verificar_paridad(binario):
    unos = binario.count('1')
    if unos % 2 == 0:
        return 0
    else:
        return 1

def hex_to_bin(hex_num):
    # Convertimos el número hexadecimal en binario y eliminamos el prefijo "0b"
    bin_num = bin(int(hex_num, 16))[2:]
    
    # Agregamos ceros a la izquierda hasta completar los 11 dígitos
    bin_num = '0' * (11 - len(bin_num)) + bin_num
    
    return bin_num

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

    return num_dec,num_bin,num_oct


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


def graficar_codigo_nrzl(cadena_binaria):
    # Convertimos el número binario a niveles de tensión utilizando NRZ-L
    niveles_tension = codificar_nrzl(cadena_binaria)

    # Graficamos la señal
    plt.plot(range(len(niveles_tension)), niveles_tension, drawstyle='steps-pre')
    plt.xlabel('Tiempo (bits)')
    plt.ylabel('Nivel de tensión')
    plt.ylim(-1.5, 1.5)
    plt.show()


def hamming_encode(data):
    n = len(data)
    # Calculamos el número de bits de paridad necesarios (m)
    for i in range(n):
        if 2**i >= n + i + 1:
            m = i
            break
    else:
        m = i + 1

    # Creamos la palabra de código con los bits de paridad inicializados a 0
    code = [0] * (n + m)
    j = 0
    k = 0
    # Recorremos la palabra de código y vamos insertando los bits de datos
    # y de paridad en las posiciones correspondientes
    for i in range(n + m):
        if i+1 == 2**k:
            k += 1
        else:
            code[i] = int(data[j])
            j += 1

    # Calculamos los bits de paridad
    for i in range(m):
        p = 0
        # Recorremos la palabra de código sumando los bits correspondientes
        # para cada bit de paridad
        for j in range(n + m):
            if ((j+1) & (2**i)) == (2**i):
                p ^= code[j]
        # Asignamos el bit de paridad calculado a la posición correspondiente
        code[2**i-1] = p

    # Creamos una tabla con los datos de paridad y los datos de base
    table = []
    for i in range(m):
        row = []
        for j in range(n + m):
            if ((j+1) & (2**i)) == (2**i):
                row.append(code[j])
            else:
                row.append(' ')
        row.append(code[2**i-1])
        table.append(row)

    return code, table

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
        # parity = sum(parity_bits) % 2
        parity = reduce(operator.xor, parity_bits[1::])
        # Agrega la entrada a la tabla de paridad
        used_bits = [encoded_bits[j] if (j+1) & (2**i) else ' ' for j in range(len(encoded_bits))]
        used_bits.pop(2**i - 1)
        parity_table.append(
            # (i+1, parity, used_bits, "correcto" if parity == encoded_bits[(2**i)-1] else "error"))
            (i+1, parity, used_bits, 0 if parity == parity_bits[0] else 1))

    ######################################################ERROR EN LA DECODIFICACIÓN###################################
    #Se obitene la posicion del bit erroneo
    error_bit = []
    for index in range(len(parity_table)):
        error_bit.append(parity_table[index][3])
    error_bit.reverse()
    #Si la posicion en binario es 0, no hay error, de lo contrario si

    check_if_error_exists = check_error_bit(error_bit, 0)

    if(check_if_error_exists):
        print("No hay error en la decodificacion")
        decoded_value = get_original_data(encoded_bits)
        return decoded_value, parity_table
    else:
        pos_error_bit = 0
        for index in range(len(error_bit)):
            pos_error_bit = pos_error_bit*10+error_bit[index]
        # Se agrega el 0b para que Python pueda realizar la conversion de binario a decimal
        pos_error_bit = int("0b" + str(pos_error_bit), 2) - 1
        print("Hay un error en la posicion: ", pos_error_bit)
        decoded_value = fix_error_bit(encoded_bits, pos_error_bit)
        return decoded_value, parity_table
    

"""
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
    return list(reversed(decoded_value)), parity_table"""

def check_error_bit(error_bit: list, value: int):
    for index in error_bit:
        if index != value:
            return False
    return True

def get_original_data(encoded_bits: list):
    #Se obtienen los indices de los bits  de paridad
    num_parity_bits = 0
    bit_parity_index = []
    while 2 ** num_parity_bits <= len(encoded_bits):
        bit_parity_index.append(2 ** num_parity_bits - 1)
        num_parity_bits += 1
    
    # Se eliminan los bits de paridad y se devuelve el mensaje original
    for index in range(len(bit_parity_index)):
        encoded_bits.pop(bit_parity_index[index]-index)
    return encoded_bits

def fix_error_bit(encoded_bits: list, error_index: int):
    # Se sustituye el valor segun corresponda
    if(encoded_bits[error_index] == 0):
        encoded_bits[error_index] = 1
        # Se obtiene el mensaje original
        decoded_value = get_original_data(encoded_bits)
        return decoded_value
    else:
        encoded_bits[error_index] = 0
        # Se obtiene el mensaje original
        decoded_value = get_original_data(encoded_bits)
        return decoded_value
    pass


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
        
def test():
    # codigo = "00010011001"
    # code, table = hamming_encode(codigo)
    # print('Palabra de código:', code)
    # print('Tabla de paridad:')
    # for row in table:
    #     print(row)
    bits = [1,0,1,1,0,0,0,1,0,1,0,0,1,0,0]
    decoded_value, parity_table = hamming_decode(bits)
    print(f"Valor decodificado: {decoded_value}\n")
    print(f"Tabla de paridad: {parity_table}\n")
    for entry in parity_table:
        print(
            f"Bit {entry[0]}: Paridad {entry[1]}, bits utilizados: {entry[2]} ({entry[3]})\n")


if __name__ == '__main__':
    test()
