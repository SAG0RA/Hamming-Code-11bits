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


def programa():
    """Función principal que solicita al usuario un número binario y lo convierte a hexadecimal."""
    while True:
        paridad = int(input("Ingrese un 0 si desea paridad par o 1 si desea impar: \n"))
        num_bin = input("Ingrese un número binario de 11 bits: ")
        if verificar_binario(num_bin) and (paridad == verificar_paridad(num_bin)):
            num_hex = convertir_binario_a_hexadecimal(num_bin)
            if verificar_rango(int(num_bin, 2)):
                print(
                    f"El número binario {num_bin} es equivalente al número hexadecimal {num_hex}.")
                convertir_hexadecimal_tabla(num_hex)
                graficar_codigo_nrzl(num_bin)
                break


if __name__ == '__main__':
    programa()
