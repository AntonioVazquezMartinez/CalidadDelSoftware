"""
Script para la conversión de números decimales a binario y hexadecimal.
Procesa un archivo de texto (.txt), realiza las conversiones y guarda los resultados.
"""

import sys
import time

# Constantes de mapeo para hexadecimal
HEX_MAP = "0123456789ABCDEF"


def to_binary(number):
    """Convierte un número entero a su representación binaria."""
    if number == 0:
        return "0"
    binary_str = ""
    absolute_value = abs(number)
    while absolute_value > 0:
        remainder = absolute_value % 2
        binary_str = str(remainder) + binary_str
        absolute_value //= 2
    if number < 0:
        binary_str = "-" + binary_str
    return binary_str


def to_hexadecimal(number):
    """Convierte un número entero a su representación hexadecimal."""
    if number == 0:
        return "0"
    hex_str = ""
    absolute_value = abs(number)
    while absolute_value > 0:
        remainder = absolute_value % 16
        hex_char = HEX_MAP[remainder]
        hex_str = hex_char + hex_str
        absolute_value //= 16
    if number < 0:
        hex_str = "-" + hex_str
    return hex_str


def process_file(file_path):
    """
    Lee datos numéricos de un archivo y los convierte.
    Retorna una lista con los resultados formateados.
    """
    results = [f"{'NUMBER':<15} {'BINARY':<25} {'HEXADECIMAL':<20}", "-" * 60]
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                item = line.strip()
                if not item:
                    continue
                try:
                    number = int(float(item))
                    bin_val = to_binary(number)
                    hex_val = to_hexadecimal(number)
                    results.append(f"{number:<15} {bin_val:<25} {hex_val:<20}")
                except ValueError:
                    print(f"Error: Dato inválido '{item}' en línea {line_num}.")
    except FileNotFoundError:
        print(f"Error: El archivo '{file_path}' no fue encontrado.")
        return None
    return results


def main():
    """Función de entrada principal."""
    start_time = time.time()

    if len(sys.argv) < 2:
        print("Usage: python convertNumbers.py fileWithData.txt")
        return

    path = sys.argv[1]
    results_list = process_file(path)

    if results_list is None:
        return

    if len(results_list) <= 2:
        print("No se encontraron datos válidos para convertir.")

    elapsed_time = time.time() - start_time
    time_report = f"\nExecution Time: {elapsed_time:.6f} seconds"
    results_list.append(time_report)

    final_output = "\n".join(results_list)
    print("\nResultados de Conversión:")
    print(final_output)

    try:
        with open("ConvertionResults.txt", "w", encoding='utf-8') as file_out:
            file_out.write(final_output)
        print("\nResultados guardados en 'ConvertionResults.txt'")
    except IOError as error:
        print(f"Error al escribir el archivo: {error}")


if __name__ == "__main__":
    main()