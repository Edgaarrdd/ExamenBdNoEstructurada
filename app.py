# app.py
from crud import create_movie, read_movies, update_movie, delete_movie
from db import connect_db


def menu():
    print("\n--- Index Movies ---")
    print("1. Agregar película")
    print("2. Ver películas")
    print("3. Actualizar película")
    print("4. Eliminar película")
    print("5. Salir")


def main():
    db = connect_db()
    collection = db["movies"] # llamada a la colección de películas
    while True:
        menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            create_movie(collection) #llamada a la función para crear una película
        elif opcion == "2":
            read_movies(collection) # llamada a la función para leer las películas
        elif opcion == "3":
            update_movie(collection) # llamada a la función para actualizar una película
        elif opcion == "4":
            delete_movie(collection) # llamada a la función para eliminar una película
        elif opcion == "5":
            print("Saliendo de la aplicación.")
            break
        else:
            print("Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    main()