import enum
import geopy.distance

coords_1 = (31.930136409113683, 35.04317074969149)
coords_2 = (31.91498613120065, 35.00535497668031)

print (geopy.distance.distance(coords_1, coords_2).km)