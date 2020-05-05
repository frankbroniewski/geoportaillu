import unittest
import requests
from requests.exceptions import ConnectionError
import urllib

import services

class TestServices(unittest.TestCase):

    def test_endpoint(self):
        url = "https://apiv3.geoportail.lu/"
        try:
            urllib.request.urlopen(url)
        except urllib.error.URLError as e:
            self.fail("Cannot connect to %s: %s" % (url, e))
