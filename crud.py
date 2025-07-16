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

    print("Película encontrada:")
    from pprint import pprint
    pprint(movie)

    campo = input("¿Qué campo desea actualizar? (ej: synopsis, durationMinutes, rating.average): ")
    nuevo_valor = input("Nuevo valor: ")

    # Convertir a int si corresponde
    if campo in ["releaseYear", "durationMinutes", "rating.average", "rating.reviewsCount"]:
        try:
            nuevo_valor = int(nuevo_valor)
        except:
            print("Valor inválido. Debe ser un número entero.")
            return

    collection.update_one(
        {"title": title},
        {"$set": {campo: nuevo_valor}}
    )
    print("Película actualizada.")


def delete_movie(collection):
    print("\n--- Eliminar Película ---")
    title = input("Título de la película a eliminar: ")
    movie = collection.find_one({"title": title})
    if not movie:
        print("Película no encontrada.")
        return

    from pprint import pprint
    pprint(movie)
    confirm = input("¿Está seguro de eliminar esta película? (s/n): ").lower()
    if confirm == 's':
        collection.delete_one({"_id": movie["_id"]})
        print("Película eliminada.")
    else:
        print("Operación cancelada.")