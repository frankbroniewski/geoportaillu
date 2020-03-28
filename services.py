"""Use the Geoportal API of the luxembourgish adminstration of cadastre 
and topography to search for an address, land parcel or associated 
coordinates.
This module offers methods for fulltextsearch, geocode and 
reverse_geocode and a CLI implementation 
"""
import requests


API_URL = "https://apiv3.geoportail.lu/"
FIND_ENDPOINT = "fulltextsearch"
GEOCODE_ENDPOINT = "geocode/search"
REVERSE_GEOCODE_ENDPOINT = "geocode/reverse"


def do_request(url, params):
    """perform a GET request to URL with the PARAMS"""
    r = requests.get(url, params=params)
    
    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        r.raise_for_status()


def search(query_string, limit=10):
    """Search for an address or a land parcel by part of its name"""
    url = "{}{}".format(API_URL, FIND_ENDPOINT)
    response = do_request(url, {"query": query_string, "limit": limit})
    
    return response


def geocode(query_string):
    """Get coordinates for an address
    num, street, zip, locality"""
    url = "{}{}".format(API_URL, GEOCODE_ENDPOINT)
    response = do_request(url, {"queryString": query_string})
    
    return response


def reverse_geocode(coords):
    """Get address from coordinates
    coords = 'easting northing' """
    coord = coords.split(' ')
    url = "{}{}".format(API_URL, REVERSE_GEOCODE_ENDPOINT)
    response = do_request(url, {"easting": coord[0], "northing": coord[1]})
    
    return response


def main(args):
    """CLI implementation"""
    if args.search:
        result = search(args.search)
        print(result)
        
    if args.geocode:
        result = geocode(args.geocode)
        print(result)
    
    if args.reverse:
        result = reverse_geocode(args.reverse)
        print(result)


if __name__ == "__main__":
    """Search for an address or a land parcel by part of its name"""
    import argparse

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-s", "--search",
        help="Search for an address or a land parcel by part of its name")
    group.add_argument("-g", "--geocode",
        help="Geocode an address. Pattern number, street, zip, locality")
    group.add_argument("-r", "--reverse", 
        help="Reverse geocode a location to an address")
    args = parser.parse_args()

    main(args)
