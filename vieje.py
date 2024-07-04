import geopy.distance
import googlemaps
import sys

#aaaaa
gmaps = googlemaps.Client(key='TU_API_KEY')

def obtener_coordenadas(ciudad):
    geocode_result = gmaps.geocode(ciudad)
    if not geocode_result:
        return None
    location = geocode_result[0]['geometry']['location']
    return (location['lat'], location['lng'])

def calcular_distancia(ciudad_origen, ciudad_destino):
    coords_origen = obtener_coordenadas(ciudad_origen)
    coords_destino = obtener_coordenadas(ciudad_destino)
    if not coords_origen or not coords_destino:
        print("No se pudieron obtener las coordenadas de una o ambas ciudades.")
        return None, None
    distancia_km = geopy.distance.distance(coords_origen, coords_destino).km
    distancia_millas = geopy.distance.distance(coords_origen, coords_destino).miles
    return distancia_km, distancia_millas

def obtener_duracion_viaje(ciudad_origen, ciudad_destino, medio_transporte):
    now = datetime.now()
    directions_result = gmaps.directions(ciudad_origen, ciudad_destino, mode=medio_transporte, departure_time=now)
    if not directions_result:
        print("No se pudo obtener la duración del viaje.")
        return None
    duration = directions_result[0]['legs'][0]['duration']['text']
    return duration

while True:
    ciudad_origen = input("Ingrese la Ciudad de Origen (o 's' para salir): ")
    if ciudad_origen.lower() == 's':
        break
    ciudad_destino = input("Ingrese la Ciudad de Destino: ")
    medio_transporte = input("Ingrese el medio de transporte (driving, walking, bicycling, transit): ")

    distancia_km, distancia_millas = calcular_distancia(ciudad_origen, ciudad_destino)
    if distancia_km and distancia_millas:
        print(f"Distancia: {distancia_km:.2f} km ({distancia_millas:.2f} millas)")
        duracion_viaje = obtener_duracion_viaje(ciudad_origen, ciudad_destino, medio_transporte)
        if duracion_viaje:
            print(f"Duración del viaje: {duracion_viaje}")
        else:
            print("No se pudo calcular la duración del viaje.")
        print(f"Narrativa del viaje de {ciudad_origen} a {ciudad_destino} usando {medio_transporte}:")
        print(f"El viaje desde {ciudad_origen} hasta {ciudad_destino} cubre una distancia de {distancia_km:.2f} km, "
              f"lo que equivale a {distancia_millas:.2f} millas. Utilizando {medio_transporte}, el viaje tiene una "
              f"duración aproximada de {duracion_viaje}.")
    else:
        print("No se pudo calcular la distancia.")
