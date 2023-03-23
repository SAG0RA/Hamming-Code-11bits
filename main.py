import matplotlib.pyplot as plt
import math

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
                row.append('-')
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
        
def test():
    # codigo = "00010011001"
    # code, table = hamming_encode(codigo)
    # print('Palabra de código:', code)
    # print('Tabla de paridad:')
    # for row in table:
    #     print(row)
    bits = [0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0]
    decoded_value, parity_table = hamming_decode(bits)
    print("Valor decodificado:", decoded_value)
    print("Tabla de paridad:")
    for entry in parity_table:
        print(
            f"Bit {entry[0]}: Paridad {entry[1]}, bits utilizados: {entry[2]} ({entry[3]})")


if __name__ == '__main__':
    test()
