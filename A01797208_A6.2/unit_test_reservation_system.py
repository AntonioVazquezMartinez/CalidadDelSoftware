"""
Script para las pruebas de unit test de el sistema de reservaciones.
"""

import unittest
import os
from reservation_system import FileManager, Hotel, Customer, Reservation


class TestHotelReservationSystem(unittest.TestCase):
    """Clase principal para el unit test"""

    def setUp(self):
        """Configuración inicial antes de cada prueba"""
        Hotel.FILE_NAME = "test_hotels.json"
        Customer.FILE_NAME = "test_customers.json"
        Reservation.FILE_NAME = "test_reservations.json"

        self._clean_files()

    def tearDown(self):
        """Limpieza después de cada prueba"""
        self._clean_files()

    def _clean_files(self):
        """Funcion para eliminar los archivos de prueba si existen"""
        for file in [Hotel.FILE_NAME, Customer.FILE_NAME,
                     Reservation.FILE_NAME]:
            if os.path.exists(file):
                os.remove(file)

    def test_create_hotel_success_and_duplicate(self):
        """Prueba la creación de un hotel y el rechazo de duplicados"""
        result = Hotel.create_hotel("H1", "Hotel Central", 10)
        self.assertTrue(result)

        # Se intenta crear el mismo hotel
        result_dup = Hotel.create_hotel("H1", "Hotel Central", 10)
        self.assertFalse(result_dup)

    def test_display_hotel(self):
        """Prueba la lectura de datos de un hotel existente y no existente"""
        Hotel.create_hotel("H1", "Hotel Norte", 5)

        info = Hotel.display_hotel("H1")
        self.assertIsNotNone(info)
        self.assertEqual(info["name"], "Hotel Norte")

        info_none = Hotel.display_hotel("H99")
        self.assertIsNone(info_none)

    def test_create_customer(self):
        """Prueba la creación de clientes y el manejo de IDs duplicados"""
        result = Customer.create_customer("C1", "Ana Lopez", "ana@correo.com")
        self.assertTrue(result)

        result_dup = Customer.create_customer("C1", "Ana Lopez",
                                              "ana@correo.com")
        self.assertFalse(result_dup)

    def test_create_reservation_logic(self):
        """Prueba la lógica de reservación y validación de disponibilidad."""
        Hotel.create_hotel("H1", "Hotel Sur", 1)
        Customer.create_customer("C1", "Luis", "luis@correo.com")

        # Realizar una reservacion exitosa
        result = Reservation.create_reservation("R1", "C1", "H1")
        self.assertTrue(result)

        # Verificar que la disponibilidad bajo a 0
        hotel_data = FileManager.load_data(Hotel.FILE_NAME)
        self.assertEqual(hotel_data["H1"]["available_rooms"], 0)

        # Tener una falla por falta de habitaciones
        result_full = Reservation.create_reservation("R2", "C1", "H1")
        self.assertFalse(result_full)

        # Generar una falla por cliente o hotel inexistente
        self.assertFalse(Reservation.create_reservation("R3", "C99", "H1"))
        self.assertFalse(Reservation.create_reservation("R4", "C1", "H99"))

    def test_file_manager_invalid_json(self):
        """Prueba que el FileManager maneje archivos corruptos sin crashear"""
        with open(Hotel.FILE_NAME, 'w', encoding='utf-8') as file:
            file.write("{ esto no es un json valido }")

        data = FileManager.load_data(Hotel.FILE_NAME)
        self.assertEqual(data, {})

    def test_delete_hotel(self):
        """Prueba la eliminación de un hotel existente
        y el manejo de uno inexistente."""
        Hotel.create_hotel("H2", "Hotel Borrar", 10)

        # Se tiene una eliminacion exitosa
        self.assertTrue(Hotel.delete_hotel("H2"))

        # Intenta eliminar un hotel que ya no existe
        self.assertFalse(Hotel.delete_hotel("H2"))

    def test_modify_hotel(self):
        """Prueba la modificación de atributos de un hotel."""
        Hotel.create_hotel("H3", "Hotel Viejo", 20)

        # Realizar una modificacion exitosa
        self.assertTrue(Hotel.modify_hotel("H3",
                        name="Hotel Nuevo", total_rooms=25))

        # Verificar que los cambios se guardaron
        data = FileManager.load_data(Hotel.FILE_NAME)
        self.assertEqual(data["H3"]["name"], "Hotel Nuevo")
        self.assertEqual(data["H3"]["total_rooms"], 25)

        # Intentar modificar un hotel inexistente
        self.assertFalse(Hotel.modify_hotel("H99", name="Fantasma"))

    def test_display_customer(self):
        """Prueba la visualización de datos de un cliente"""
        Customer.create_customer("C2", "Carlos", "carlos@mail.com")

        info = Customer.display_customer("C2")
        self.assertIsNotNone(info)
        self.assertEqual(info["name"], "Carlos")

        info_none = Customer.display_customer("C99")
        self.assertIsNone(info_none)

    def test_delete_customer(self):
        """Prueba la eliminación de un cliente"""
        Customer.create_customer("C3", "Diana", "diana@mail.com")

        self.assertTrue(Customer.delete_customer("C3"))
        self.assertFalse(Customer.delete_customer("C3"))

    def test_modify_customer(self):
        """Prueba la actualización de información de un cliente"""
        Customer.create_customer("C4", "Elena", "elena@mail.com")

        self.assertTrue(Customer.modify_customer("C4", email="nuevo@mail.com"))

        data = FileManager.load_data(Customer.FILE_NAME)
        self.assertEqual(data["C4"]["email"], "nuevo@mail.com")
        self.assertFalse(Customer.modify_customer("C99", name="Nadie"))

    def test_cancel_reservation(self):
        """Prueba la cancelación y la restauración de
        habitaciones disponibles"""
        Hotel.create_hotel("H4", "Hotel Cancelacion", 5)
        Customer.create_customer("C5", "Fernando", "fer@mail.com")
        Reservation.create_reservation("R2", "C5", "H4")

        # Verificacion de la disponibilidad bajo a 4
        hotel_data_before = FileManager.load_data(Hotel.FILE_NAME)
        self.assertEqual(hotel_data_before["H4"]["available_rooms"], 4)

        # Hacer una cancelacion de la reservacion
        self.assertTrue(Reservation.cancel_reservation("R2"))

        # Verificar que la disponibilidad regreso a 5
        hotel_data_after = FileManager.load_data(Hotel.FILE_NAME)
        self.assertEqual(hotel_data_after["H4"]["available_rooms"], 5)

        # Hacer un intento cancelar una reservacion que ya no existe
        self.assertFalse(Reservation.cancel_reservation("R2"))


if __name__ == '__main__':
    unittest.main()

