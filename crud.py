# crud.py
from models import input_movie_data
from bson.objectid import ObjectId


def create_movie(collection):
    movie = input_movie_data()
    result = collection.insert_one(movie)
    print(f"\nPelícula insertada con ID: {result.inserted_id}")


def read_movies(collection):
    print("\n--- Lista de Películas ---")
    filtro = input("¿Desea aplicar un filtro por título? (s/n): ").lower()
    query = {}
    if filtro == 's':
        title = input("Título exacto: ")
        query = {"title": title}

    projection = {"title": 1, "releaseYear": 1, "rating.average": 1}
    results = collection.find(query, projection)

    print("\n{:<50} {:<10} {:<8}".format("Título", "Año", "Rating"))
    print("-" * 70)
    for movie in results:
        title = movie.get("title", "N/A")
        year = movie.get("releaseYear", "N/A")
        rating = movie.get("rating", {}).get("average", "N/A")
        print("{:<50} {:<10} {:<8}".format(title, year, rating))


def update_movie(collection):
    print("\n--- Actualizar Película ---")
    title = input("Título de la película a actualizar: ")
    movie = collection.find_one({"title": title})
    if not movie:
        print("Película no encontrada.")
        return

    print("\nPelícula encontrada: \n")
    print(f"Título: {movie['title']}")
    print(f"Año: {movie['releaseYear']}")
    print(f"Duración: {movie['durationMinutes']} minutos")
    print(f"Nota promedio: {movie['rating']['average']}")
    print(f"Reseñas: {movie['rating']['reviewsCount']}")
    print(f"Sinopsis: {movie['synopsis']}")

    print("\n¿Qué campo desea actualizar?")
    print("1. Título")
    print("2. Sinopsis")
    print("3. Año de estreno")
    print("4. Duración (minutos)")
    print("5. Nota promedio")
    print("6. Cantidad de reseñas")
    opcion = input("Seleccione una opción (1-6): ")

    campo_map = {
        "1": ("title", str),
        "2": ("synopsis", str),
        "3": ("releaseYear", int),
        "4": ("durationMinutes", int),
        "5": ("rating.average", int),
        "6": ("rating.reviewsCount", int)
    }

    if opcion not in campo_map:
        print("Opción inválida.")
        return

    campo, tipo = campo_map[opcion]
    nuevo_valor = input("Nuevo valor: ")

    try:
        nuevo_valor = tipo(nuevo_valor)
    except ValueError:
        print("Tipo de dato incorrecto.")
        return

    collection.update_one({"_id": movie["_id"]}, {"$set": {campo: nuevo_valor}})
    print("Película actualizada correctamente.")


def delete_movie(collection):
    print("\n--- Eliminar Película ---")
    title = input("Título de la película a eliminar: ")
    movie = collection.find_one({"title": title})
    if not movie:
        print("Película no encontrada.")
        return

    print("\nPelícula encontrada:")
    print(f"Título: {movie['title']}")
    print(f"Año: {movie['releaseYear']}")
    print(f"Duración: {movie['durationMinutes']} minutos")
    print(f"Director: {movie['director']['firstName']} {movie['director']['lastName']}")
    print(f"Nota promedio: {movie['rating']['average']} ({movie['rating']['reviewsCount']} reseñas)")
    print(f"Disponible en: {', '.join(movie.get('availableOn', []))}")

    confirm = input("\n¿Está seguro de eliminar esta película? (s/n): ").lower()
    if confirm == 's':
        collection.delete_one({"_id": movie["_id"]})
        print("Película eliminada.")
    else:
        print("Operación cancelada.")