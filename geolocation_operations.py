__author__ = "Rahul Malhotra"

from pprint import pprint

from geopy.geocoders import Photon
from geopy.distance import geodesic

geolocator = Photon(user_agent="myGeocoder")


def get_lat_long(street_address: str) -> (float, float):
    """

    :param street_address:
    :return:
    """
    location = geolocator.geocode(f"{street_address}")
    print(location.address)
    print((location.latitude, location.longitude))
    pprint(location.raw)
    return location.latitude, location.longitude


def get_street_address(latitude: float, longitude: float) -> str:
    """

    :param latitude:
    :param longitude:
    :return:
    """
    reverse_location = geolocator.reverse(f"{latitude}, {longitude}")
    print(reverse_location.address)
    pprint(reverse_location.raw)
    return reverse_location.address


def distance_between_locations(first_geolocation: tuple, second_geolocation: tuple) -> float:
    distance_in_kms = geodesic(first_geolocation, second_geolocation).km
    return distance_in_kms


if __name__ == "__main__":
    durocher = get_lat_long(street_address="Rue Durocher,Montreal")
    goyer = get_lat_long(street_address="Rue Goyer,Montreal")
    dist = distance_between_locations(durocher, goyer)
    print(dist)
