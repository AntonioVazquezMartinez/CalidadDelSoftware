"""Este script simula una ejecución normal del sistema de reservas,
   mostrando cómo se crean, modifican y
   eliminan hoteles, clientes y reservaciones.
"""
from reservation_system import Hotel, Customer, Reservation


def main():
    """Función principal para simular una ejecución normal
       del sistema de reservas."""
    print("--- INICIANDO SISTEMA DE RESERVACIONES ---")

    print("\nCreando registros...")
    Hotel.create_hotel("H1", "Hotel Tec", 5)
    Customer.create_customer("C1", "Juan Perez", "juanPerez@gmail.com")

    Hotel.display_hotel("H1")
    Customer.display_customer("C1")

    print("\nModificando cliente...")
    Customer.modify_customer("C1", email="juan_Perez@gmail.com")
    Customer.display_customer("C1")

    print("\nCreando reservación...")
    Reservation.create_reservation("R1", "C1", "H1")
    Hotel.display_hotel("H1")

    print("\nCancelando reservación...")
    Reservation.cancel_reservation("R1")
    Hotel.display_hotel("H1")

    print("\nBorrando registros...")
    Hotel.delete_hotel("H1")
    Customer.delete_customer("C1")


if __name__ == "__main__":
    main()
