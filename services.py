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


def search(query_string, limit=10):
    """Search for an address or a land parcel by part of its name"""
    url = "{}{}".format(API_URL, FIND_ENDPOINT)
    r = requests.get(url, params={"query": query_string, "limit": limit})

    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        r.raise_for_status()


def geocode():
    """Get coordinates for an address
    TODO"""
    pass


def reverse_geocode():
    """Get address from coordinates
    TODO"""
    pass


def main(args):
    """CLI implementation"""
    if args.search:
        result = search(args.search)
        print(result)


if __name__ == "__main__":
    """Search for an address or a land parcel by part of its name
    TODO implement CLI for geocoding"""
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search",
        help="Search for an address or a land parcel by part of its name")
    args = parser.parse_args()

    main(args)