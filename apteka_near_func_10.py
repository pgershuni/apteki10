# Определяем функцию, считающую расстояние между двумя точками, заданными координатами
import math

def lonlat_distance(a, b):
    degree_to_meters_factor = 111 * 1000  # 111 километров в метрах
    a_lon, a_lat = a.split()
    a_lon, a_lat = float(a_lon), float( a_lat)
    b_lon, b_lat = float(b[0]), float(b[1])
    # Берем среднюю по широте точку и считаем коэффициент для нее.
    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)
    # Вычисляем смещения в метрах по вертикали и горизонтали.
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor
    # Вычисляем расстояние между точками.
    distance = math.sqrt(dx * dx + dy * dy)
    return distance

def get_spn(toponym):
    upperCorner = [float(x) for x in toponym['boundedBy']['Envelope']['upperCorner'].split()]
    lower_corner = [float(x) for x in toponym['boundedBy']['Envelope']['lowerCorner'].split()]
    delta_1 = str(abs(upperCorner[0] - lower_corner[0]))
    delta_2 = str(abs(upperCorner[1] - lower_corner[1]))
    return delta_1, delta_2


def get_spn_two_points(toponym1,toponym2):
    upperCorner1 = [float(x) for x in toponym1['boundedBy']['Envelope']['upperCorner'].split()]
    lower_corner1 = [float(x) for x in toponym1['boundedBy']['Envelope']['lowerCorner'].split()]

    upperCorner2 = [float(x) for x in toponym2['boundedBy'][0]]
    lower_corner2 = [float(x) for x in toponym2['boundedBy'][1]]

    delta_1 = max(abs(upperCorner1[0] - lower_corner2[0]), abs(upperCorner2[0] - lower_corner1[0]))
    delta_2 = max(abs(upperCorner1[1] - lower_corner2[1]), abs(upperCorner2[1] - lower_corner1[1]))
    #print('get_spn_two_points', delta_1, delta_2)
    return delta_1, delta_2