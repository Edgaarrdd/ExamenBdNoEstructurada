# crud.py
from models import input_movie_data
from bson.objectid import ObjectId

# Crea una nueva película solicitando los datos al usuario y guardándola en MongoDB

def create_movie(collection):
    movie = input_movie_data()
    result = collection.insert_one(movie)
    print(f"\nPelícula insertada con ID: {result.inserted_id}")

# Lista las películas con opción de aplicar filtro por título y ver detalles completos

def read_movies(collection):
    print("\n--- Lista de Películas ---")
    filtro = input("¿Desea aplicar un filtro por título? (s/n): ").lower()
    query = {}
    if filtro == 's':
        title = input("Título exacto: ")
        query = {"title": title}

    projection = {"title": 1, "releaseYear": 1, "rating.average": 1}
    results = list(collection.find(query, projection))  # método find devuelve un cursor; lo convertimos a lista

    if not results:
        print("No se encontraron películas.")
        return

    # Imprime resumen de películas
    print("\n{:<50} {:<10} {:<8}".format("Título", "Año", "Rating"))
    print("-" * 70)
    for idx, movie in enumerate(results, 1):
        title = movie.get("title", "N/A") # metodo get devuelve el valor de la clave si existe, o "N/A" si no
        year = movie.get("releaseYear", "N/A") # método get devuelve el año de lanzamiento o "N/A" si no existe
        rating = movie.get("rating", {}).get("average", "N/A") # método get devuelve la nota promedio o "N/A" si no existe
        print("{:<2}. {:<45} {:<10} {:<8}".format(idx, title[:45], year, rating))

    # Opción para ver detalles de una película específica
    ver_detalles = input("\n¿Desea ver detalles de alguna película? (s/n): ").lower()
    if ver_detalles == 's':
        opcion = input("Ingrese el número de la película: ")
        if opcion.isdigit():
            opcion = int(opcion)
            if 1 <= opcion <= len(results):
                detalle = collection.find_one({"_id": results[opcion - 1]["_id"]}) # método find_one busca un documento por su ID
                print("\n--- Detalles de la Película ---")
                print(f"Título: {detalle['title']}")
                print(f"Año: {detalle['releaseYear']}")
                print(f"Duración: {detalle['durationMinutes']} minutos")
                print(f"Director: {detalle['director']['firstName']} {detalle['director']['lastName']} ({detalle['director']['birthYear']})")
                print(f"Nota promedio: {detalle['rating']['average']} ({detalle['rating']['reviewsCount']} reseñas)")
                print(f"Sinopsis: {detalle['synopsis']}")
                print(f"Disponible en: {', '.join(detalle.get('availableOn', []))}")
                print(f"Géneros: {', '.join(detalle.get('genre', []))}")
                print(f"Palabras clave: {', '.join(detalle.get('keywords', []))}")
            else:
                print("Número fuera de rango.")
        else:
            print("Entrada inválida.")

# Permite actualizar campos seleccionados de una película existente

def update_movie(collection):
    print("\n--- Actualizar Película ---")
    title = input("Título de la película a actualizar: ")
    movie = collection.find_one({"title": title}) #método find_one busca un documento por su título
    if not movie:
        print("Película no encontrada.")
        return

    # Muestra datos básicos de la película encontrada
    print("\nPelícula encontrada: \n")
    print(f"Título: {movie['title']}")
    print(f"Año: {movie['releaseYear']}")
    print(f"Duración: {movie['durationMinutes']} minutos")
    print(f"Nota promedio: {movie['rating']['average']}")
    print(f"Reseñas: {movie['rating']['reviewsCount']}")
    print(f"Sinopsis: {movie['synopsis']}")

    # Muestra menú de campos actualizables
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

    # Realiza la actualización
    collection.update_one({"_id": movie["_id"]}, {"$set": {campo: nuevo_valor}}) #método update_one actualiza un documento específico
    print("Película actualizada correctamente.")

# Elimina una película después de mostrar listado, confirmar selección y confirmar borrado

def delete_movie(collection):
    print("\n--- Eliminar Película ---")

    # Muestra lista de películas disponibles
    movies = list(collection.find({}, {"title": 1, "releaseYear": 1})) #metodo find obtiene todas las películas con título y año
    if not movies:
        print("No hay películas para eliminar.")
        return

    print("\nPelículas disponibles:")
    for idx, m in enumerate(movies, 1): # método enumerate agrega un índice a cada película
        print(f"{idx}. {m['title']} ({m['releaseYear']})")

    opcion = input("\nSeleccione el número de la película a eliminar: ")
    if not opcion.isdigit() or not (1 <= int(opcion) <= len(movies)): #método isdigit verifica si la entrada es un número
        print("Selección inválida.")
        return

    seleccionada = collection.find_one({"_id": movies[int(opcion)-1]['_id']})

    # Muestra detalles antes de confirmar eliminación
    print("\nPelícula seleccionada:")
    print(f"Título: {seleccionada['title']}")
    print(f"Año: {seleccionada['releaseYear']}")
    print(f"Duración: {seleccionada['durationMinutes']} minutos")
    print(f"Director: {seleccionada['director']['firstName']} {seleccionada['director']['lastName']}")
    print(f"Nota promedio: {seleccionada['rating']['average']} ({seleccionada['rating']['reviewsCount']} reseñas)")
    print(f"Disponible en: {', '.join(seleccionada.get('availableOn', []))}")

    confirm = input("\n¿Está seguro de eliminar esta película? (s/n): ").lower()
    if confirm == 's':
        collection.delete_one({"_id": seleccionada["_id"]}) # metodo delete_one elimina el documento
        print("Película eliminada.")
    else:
        print("Operación cancelada.")