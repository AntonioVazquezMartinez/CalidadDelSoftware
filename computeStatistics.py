"""
Este script es para el cálculo de estadísticas descriptivas a partir de un archivo txt.
Este script calcula media, mediana, moda, varianza y desviación estándar.
"""
import sys
import time

def read_file(file_path):
    """Lee un archivo y extrae una lista de números flotantes."""
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                item = line.strip()
                if not item:
                    continue
                try:
                    number = float(item)
                    data.append(number)
                except ValueError:
                    print(f"Error: Dato inválido '{item}' en línea {line_num}.")
    except FileNotFoundError:
        print(f"Error: El archivo '{file_path}' no fue encontrado.")
        return None

    return data


def calculate_mean(data):
    """Calcula la media aritmética de una lista de números."""
    if not data:
        return 0.0
    return sum(data) / len(data)


def calculate_median(data):
    """Calcula la mediana de una lista de números."""
    if not data:
        return 0.0

    sorted_data = sorted(data)
    n_elements = len(sorted_data)
    mid = n_elements // 2

    if n_elements % 2 == 1:
        return sorted_data[mid]
    return (sorted_data[mid - 1] + sorted_data[mid]) / 2


def calculate_mode(data):
    """Calcula la moda (el valor más frecuente) de una lista de números."""
    if not data:
        return 0.0

    frequency = {}
    for num in data:
        frequency[num] = frequency.get(num, 0) + 1

    max_count = 0
    mode_val = data[0]

    for num, count in frequency.items():
        if count > max_count:
            max_count = count
            mode_val = num

    return mode_val


def calculate_variance(data, mean):
    """Calcula la varianza muestral de una lista de números."""
    if len(data) < 2:
        return 0.0

    sum_sq_diff = sum((x - mean) ** 2 for x in data)
    return sum_sq_diff / (len(data) - 1)


def calculate_std_dev(variance):
    """Calcula la desviación estándar a partir de la varianza."""
    return variance ** 0.5


def main():
    """Función principal para coordinar la lectura y cálculos estadísticos."""
    start_time = time.time()

    if len(sys.argv) < 2:
        print("Usage: python Compute_statistics.py <File path>")
        return

    file_param = sys.argv[1]
    data = read_file(file_param)

    if data is None or not data:
        print("Error: No se pudieron procesar datos válidos.")
        return

    mean = calculate_mean(data)
    median = calculate_median(data)
    mode_val = calculate_mode(data)
    variance = calculate_variance(data, mean)
    std_dev = calculate_std_dev(variance)

    end_time = time.time()
    execution_time = end_time - start_time

    # Preparar resultados
    results = (
        f"Mean: {mean}\n"
        f"Median: {median}\n"
        f"Mode: {mode_val}\n"
        f"Variance: {variance}\n"
        f"Standard Deviation: {std_dev}\n"
        f"Execution Time: {execution_time:.4f} seconds\n"
    )

    print(results)

    try:
        with open("StatisticsResults.txt", 'w', encoding='utf-8') as f_out:
            f_out.write(results)
    except IOError as err:
        print(f"Error al escribir el archivo de resultados: {err}")


if __name__ == "__main__":
    main()