# app.py
from crud import create_movie, read_movies, update_movie, delete_movie
from db import connect_db


def menu():
    print("\n--- Aplicación CRUD de Películas ---")
    print("1. Agregar película")
    print("2. Ver películas")
    print("3. Actualizar película")
    print("4. Eliminar película")
    print("5. Salir")


def main():
    db = connect_db()
    collection = db["movies"]

    while True:
        menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            create_movie(collection)
        elif opcion == "2":
            read_movies(collection)
        elif opcion == "3":
            update_movie(collection)
        elif opcion == "4":
            delete_movie(collection)
        elif opcion == "5":
            print("Saliendo de la aplicación.")
            break
        else:
            print("Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    main()