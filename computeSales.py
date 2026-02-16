import json
import sys
import time


def load_json_file(filename):
    """Carga un archivo JSON y maneja errores de lectura."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{filename}'.")
        return None
    except json.JSONDecodeError:
        print(f"Error: El archivo '{filename}' "
              f"no tiene un formato JSON válido.")
        return None
    except Exception as e:
        print(f"Error inesperado leyendo '{filename}': {e}")
        return None


def create_price_lookup(catalogue):
    """
    Convierte la lista de catálogo en un diccionario para búsqueda rápida.

    Cumple con el Requerimiento 6 para manejar miles de items eficientemente.
    """
    price_dict = {}
    for item in catalogue:
        # Intentamos obtener claves comunes para el nombre del producto
        title = item.get("title") or item.get("name") or item.get("Product")
        price = item.get("price") or item.get("Price")

        if title and price is not None:
            price_dict[title] = price
    return price_dict


def compute_total_cost(price_dict, sales_record):
    """Calcula el costo total y maneja errores de datos inválidos."""
    total_cost = 0.0

    for sale in sales_record:
        # Intentamos obtener claves comunes para producto y cantidad
        product_name = (
            sale.get("Product") or sale.get("title") or sale.get("name")
        )
        quantity = sale.get("Quantity") or sale.get("quantity")

        if not product_name or quantity is None:
            print(f"Error de datos: Registro de venta incompleto -> {sale}")
            continue

        try:
            # Verificar si el producto existe en el catálogo
            if product_name in price_dict:
                item_price = price_dict[product_name]
                cost = item_price * quantity
                total_cost += cost
            else:
                print(f"Error: El producto '{product_name}' "
                      f"no existe en el catálogo.")
        except (TypeError, ValueError) as e:
            print(f"Error calculando costo para '{product_name}': {e}")
            continue

    return total_cost


def main():
    # Iniciar conteo de tiempo
    start_time = time.time()

    # Validación de argumentos de línea de comandos
    if len(sys.argv) != 3:
        print("Uso incorrecto. Formato requerido:")
        print("python computeSales.py priceCatalogue.json salesRecord.json")
        sys.exit(1)

    catalogue_file = sys.argv[1]
    sales_file = sys.argv[2]

    # Cargarmos archivos
    catalogue_data = load_json_file(catalogue_file)
    sales_data = load_json_file(sales_file)

    if catalogue_data is None or sales_data is None:
        sys.exit(1)

    # Procesamos los datos
    # Y se convierten de una lista a dict para búsqueda O(1)
    price_lookup = create_price_lookup(catalogue_data)

    # Calcular total de ventas
    total_sales = compute_total_cost(price_lookup, sales_data)

    # Calcular el tiempo transcurrido
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Formatear para que sea una salida legible
    output_lines = [
        "TOTAL SALES REPORT",
        "-" * 30,
        f"Total Cost: ${total_sales:,.2f}",
        f"Execution Time: {elapsed_time:.4f} seconds",
        "-" * 30
    ]

    output_string = "\n".join(output_lines)

    print("\n" + output_string)

    # Los resultados se guardan en archivo SalesResults.txt
    try:
        with open("SalesResults.txt", "w", encoding='utf-8') as f:
            f.write(output_string)
        print("\nResultados guardados en 'SalesResults.txt'.")
    except Exception as e:
        print(f"Error al escribir el archivo de resultados: {e}")


if __name__ == "__main__":
    main()