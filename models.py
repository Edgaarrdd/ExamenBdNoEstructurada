# models.py

def input_movie_data():
    print("\n--- Ingresar nueva película ---")
    title = input("Título: ")
    release_year = int(input("Año de estreno: "))

    # Géneros
    genre = input("Géneros (separados por coma): ").split(",")
    genre = [g.strip() for g in genre if g.strip()]

    # Director
    print("\n--- Datos del director ---")
    first_name = input("Nombre: ")
    last_name = input("Apellido: ")
    birth_year = int(input("Año de nacimiento: "))
    director = {
        "firstName": first_name,
        "lastName": last_name,
        "birthYear": birth_year
    }

    # Cast
    print("\n--- Reparto (mínimo un actor) ---")
    cast = []
    while True:
        actor = input("Nombre del actor (deja vacío para terminar): ")
        if not actor:
            break
        character = input("Nombre del personaje: ")
        role_type = input("Tipo de rol (Principal/Secundario): ")
        cast.append({
            "actorName": actor,
            "characterName": character,
            "roleType": role_type
        })

    # Sinopsis y duración
    synopsis = input("Sinopsis: ")
    duration = int(input("Duración en minutos: "))

    # Rating
    print("\n--- Calificación ---")
    average = int(input("Nota promedio (entero): "))
    reviews_count = int(input("Cantidad de reseñas: "))
    rating = {
        "average": average,
        "reviewsCount": reviews_count
    }

    # Producción
    print("\n--- Producción ---")
    studio = input("Estudio: ")
    country = input("País: ")
    budget = int(input("Presupuesto (USD): "))
    production = {
        "studio": studio,
        "country": country,
        "budgetUSD": budget
    }

    # Keywords y plataformas
    keywords = input("Palabras clave (separadas por coma): ").split(",")
    keywords = [k.strip() for k in keywords if k.strip()] # lista de palabras clave 
    available_on = input("Disponibilidad (plataformas separadas por coma): ").split(",")
    available_on = [a.strip() for a in available_on if a.strip()]

    is_award_winner = input("¿Ganadora de premios? (s/n): ").lower() == 's'

    movie = { # diccionario que representa la película
        "title": title,
        "releaseYear": release_year,
        "genre": genre,
        "director": director,
        "cast": cast,
        "synopsis": synopsis,
        "durationMinutes": duration,
        "rating": rating,
        "production": production,
        "keywords": keywords,
        "availableOn": available_on,
        "isAwardWinner": is_award_winner
    }

    return movie