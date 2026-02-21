"""
Script para el sistema de reservaciones.
Con este se manejaran las operaciones de Hoteles, Clientes y Reservaciones.
"""

import json
import os


class FileManager:
    """Clase utilitaria para manejar la lectura
    y escritura de archivos JSON."""
    @staticmethod
    def load_data(filename):
        """Cargamos los datos desde un archivo JSON manejando errores
        de formato o inexistencia."""
        if not os.path.exists(filename):
            return {}
        try:
            with open(filename, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError as error:
            print(f"Error: Datos inválidos en {filename}. Detalles: {error}")
            return {}
        except IOError as error:
            print(f"Error: No se pudo leer {filename}. Detalles: {error}")
            return {}

    @staticmethod
    def save_data(filename, data):
        """Guarda un diccionario de datos en un archivo JSON."""
        try:
            with open(filename, 'w') as file:
                json.dump(data, file, indent=4)
        except IOError as error:
            print(f"Error al guardar en {filename}: {error}")


class Hotel:
    """Con esta clase se representa y maneja las operaciones del Hotel."""
    FILE_NAME = "hotels.json"

    def __init__(self, hotel_id, name, total_rooms):
        self.hotel_id = hotel_id
        self.name = name
        self.total_rooms = total_rooms
        self.available_rooms = total_rooms

    @classmethod
    def create_hotel(cls, hotel_id, name, total_rooms):
        """Crea un hotel y lo guarda en el archivo."""
        data = FileManager.load_data(cls.FILE_NAME)
        if hotel_id in data:
            print(f"El hotel con ID {hotel_id} ya existe.")
            return False
        data[hotel_id] = {
            "name": name,
            "total_rooms": total_rooms,
            "available_rooms": total_rooms
        }
        FileManager.save_data(cls.FILE_NAME, data)
        return True

    @classmethod
    def display_hotel(cls, hotel_id):
        """Muestra la información de un hotel específico."""
        data = FileManager.load_data(cls.FILE_NAME)
        hotel_info = data.get(hotel_id)
        if hotel_info:
            print(f"Hotel {hotel_id}: {hotel_info['name']} - "
                  f"Habitaciones disponibles: {hotel_info['available_rooms']}")
            return hotel_info
        print("Hotel no encontrado.")
        return None

    @classmethod
    def delete_hotel(cls, hotel_id):
        """Elimina un hotel del registro."""
        data = FileManager.load_data(cls.FILE_NAME)
        if hotel_id in data:
            del data[hotel_id]
            FileManager.save_data(cls.FILE_NAME, data)
            print(f"Hotel {hotel_id} eliminado exitosamente.")
            return True
        print("Error: Hotel no encontrado.")
        return False

    @classmethod
    def modify_hotel(cls, hotel_id, **kwargs):
        """
        Modifica la información de un hotel.
        Acepta argumentos por nombre, ej: name="Nuevo Nombre"
        """
        data = FileManager.load_data(cls.FILE_NAME)
        if hotel_id in data:
            for key, value in kwargs.items():
                if key in data[hotel_id]:
                    data[hotel_id][key] = value
            FileManager.save_data(cls.FILE_NAME, data)
            print(f"Hotel {hotel_id} modificado exitosamente.")
            return True
        print("Error: Hotel no encontrado.")
        return False


class Customer:
    """Con esta clase se  representa y maneja las operaciones de un Cliente."""

    FILE_NAME = "customers.json"

    @classmethod
    def create_customer(cls, customer_id, name, email):
        """Crea un cliente y lo guarda en el archivo."""
        data = FileManager.load_data(cls.FILE_NAME)
        if customer_id in data:
            print(f"El cliente con ID {customer_id} ya existe.")
            return False

        data[customer_id] = {"name": name, "email": email}
        FileManager.save_data(cls.FILE_NAME, data)
        return True

    @classmethod
    def delete_customer(cls, customer_id):
        """Elimina un cliente del registro."""
        data = FileManager.load_data(cls.FILE_NAME)
        if customer_id in data:
            del data[customer_id]
            FileManager.save_data(cls.FILE_NAME, data)
            print(f"Cliente {customer_id} eliminado exitosamente.")
            return True
        print("Error: Cliente no encontrado.")
        return False

    @classmethod
    def display_customer(cls, customer_id):
        """Muestra la información de un cliente específico."""
        data = FileManager.load_data(cls.FILE_NAME)
        customer_info = data.get(customer_id)
        if customer_info:
            print(f"Cliente {customer_id}: {customer_info['name']} "
                  f"({customer_info['email']})")
            return customer_info
        print("Error: Cliente no encontrado.")
        return None

    @classmethod
    def modify_customer(cls, customer_id, **kwargs):
        """Modifica la información de un cliente."""
        data = FileManager.load_data(cls.FILE_NAME)
        if customer_id in data:
            for key, value in kwargs.items():
                if key in data[customer_id]:
                    data[customer_id][key] = value
            FileManager.save_data(cls.FILE_NAME, data)
            print(f"Cliente {customer_id} modificado exitosamente.")
            return True
        print("Error: Cliente no encontrado.")
        return False


class Reservation:
    """Clase que maneja la creación y cancelación de reservaciones."""

    FILE_NAME = "reservations.json"

    @classmethod
    def create_reservation(cls, reservation_id, customer_id, hotel_id):
        """Crea una reservación vinculando cliente y hotel."""
        hotels = FileManager.load_data(Hotel.FILE_NAME)
        customers = FileManager.load_data(Customer.FILE_NAME)
        reservations = FileManager.load_data(cls.FILE_NAME)

        if customer_id not in customers:
            print("Error: El cliente no existe.")
            return False
        if hotel_id not in hotels:
            print("Error: El hotel no existe.")
            return False
        if hotels[hotel_id]['available_rooms'] <= 0:
            print("Error: No hay habitaciones disponibles.")
            return False

        # Reducir disponibilidad
        hotels[hotel_id]['available_rooms'] -= 1
        FileManager.save_data(Hotel.FILE_NAME, hotels)

        # Crear reservación
        reservations[reservation_id] = {
            "customer_id": customer_id,
            "hotel_id": hotel_id
        }
        FileManager.save_data(cls.FILE_NAME, reservations)
        print(f"Reservación {reservation_id} creada con éxito.")
        return True

    @classmethod
    def cancel_reservation(cls, reservation_id):
        """Cancela una reservación y libera la habitación del hotel."""
        reservations = FileManager.load_data(cls.FILE_NAME)

        if reservation_id not in reservations:
            print("Error: Reservación no encontrada.")
            return False

        hotel_id = reservations[reservation_id]['hotel_id']
        hotels = FileManager.load_data(Hotel.FILE_NAME)

        # Aumentar disponibilidad en el hotel correspondiente
        if hotel_id in hotels:
            hotels[hotel_id]['available_rooms'] += 1
            FileManager.save_data(Hotel.FILE_NAME, hotels)

        # Eliminar la reservación
        del reservations[reservation_id]
        FileManager.save_data(cls.FILE_NAME, reservations)
        print(f"Reservación {reservation_id} cancelada con éxito.")
        return True

