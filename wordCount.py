"""
Script para el conteo de frecuencia de palabras en un archivo de texto.
Se lee un archivo (.txt), cuenta las ocurrencias de cada palabra y reporta los resultados.
"""

import sys
import time


def get_word_frequencies(file_path):
    """
    Lee un archivo y devuelve un diccionario con la frecuencia de palabras.
    Retorna None si ocurre un error de lectura.
    """
    frequencies = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                # split() sin argumentos maneja múltiples espacios automáticamente
                words = line.split()
                for word in words:
                    # Uso de .get() para simplificar la lógica if-else
                    frequencies[word] = frequencies.get(word, 0) + 1

    except FileNotFoundError:
        print(f"Error: El archivo '{file_path}' no fue encontrado.")
        return None
    except UnicodeDecodeError:
        print(f"Error: No se pudo decodificar '{file_path}'. Verifique el formato.")
        return None
    except OSError as err:
        print(f"Error inesperado leyendo el archivo: {err}")
        return None
    return frequencies


def main():
    """Función principal para coordinar el conteo y reporte de palabras."""
    start_time = time.time()
    if len(sys.argv) < 2:
        print("Usage: python wordCount.py fileWithData.txt")
        return

    file_path = sys.argv[1]
    # Obtenemos datos o None si falló
    frequency_dict = get_word_frequencies(file_path)
    if frequency_dict is None:
        # El error ya fue impreso en la función
        return

    if not frequency_dict:
        print("No se encontraron palabras para procesar.")
        return
    end_time = time.time()
    elapsed_time = end_time - start_time
    # Construcción de resultados
    results_list = [f"{'WORD':<30} {'FREQUENCY':<10}", "-" * 40]
    # Ordenar alfabéticamente por palabra
    sorted_words = sorted(frequency_dict.keys())
    for word in sorted_words:
        count = frequency_dict[word]
        results_list.append(f"{word:<30} {count:<10}")
    time_report = f"\nExecution Time: {elapsed_time:.6f} seconds"
    results_list.append(time_report)
    final_output = "\n".join(results_list)
    print("\nResultados de Frecuencia de Palabras:")
    print(final_output)
    try:
        output_filename = "WordCountResults.txt"
        with open(output_filename, 'w', encoding='utf-8') as f_out:
            f_out.write(final_output)
        print(f"\nResultados guardados en '{output_filename}'")
    except IOError as err:
        print(f"Error al escribir el archivo de resultados: {err}")


if __name__ == "__main__":
    main()