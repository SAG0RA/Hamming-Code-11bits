import operator
import matplotlib.pyplot as plt
from functools import reduce

# cadena de prueba 11001101011
# pariedad impar == 1






def hamming_encode(data, parity='par'):
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
        if parity == 'impar':
            code[2**i-1] = int(not p)
        else:
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
            (i+1, parity, used_bits, "correcto" if parity == parity_bits[0] else "error"))

    ######################################################ERROR EN LA DECODIFICACIÓN###################################
    #Se obitene la posicion del bit erroneo
    error_bit = []
    for index in range(len(parity_table)):
        error_bit.append(parity_table[index][3])

    error_bit.reverse()

    for i in range(len(error_bit)):
        if error_bit[i] == 'correcto':
            error_bit[i] = 0
        else:
            error_bit[i] = 1
    print(error_bit)
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
        
def test():
    # codigo = "00010011001"
    # code, table = hamming_encode(codigo)
    # print('Palabra de código:', code)
    # print('Tabla de paridad:')
    # for row in table:
    #     print(row)
    bits = [1,0,1,1,0,0,0,1,1,1,0,0,1,0,0]
    decoded_value, parity_table = hamming_decode(bits)
    print(f"Valor decodificado: {decoded_value}\n")
    print(f"Tabla de paridad: {parity_table}\n")
    for entry in parity_table:
        print(
            f"Bit {entry[0]}: Paridad {entry[1]}, bits utilizados: {entry[2]} ({entry[3]})\n")


if __name__ == '__main__':
    test()
