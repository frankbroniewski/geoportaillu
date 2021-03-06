# Luxembourgish Geoportal Services
Use this plugin to access the services from the luxembourgish
Geoportal. This first release allows searching for places, addresses and land 
parcels in Luxembourg.

## How to use
The interface mimics the location search bar found in the geoportals web page. 
Start typing in the address search bar and hit search button when done. Select any of the
search results and hit <add> to add the result to your map.

Depending on the type of search result you will get a polygon, a bounding box or a 
point. Land parcels are shown with their true form, larger result sets like 
communes are shown with their bounding box. Addresses will return a point geometry.

The plugin will zoom on the result upon adding it to the map. A special group in the 
layer tree will be created to contain the result(s).

The received result from the geoportal is transformed into your project's CRS.

## Requirements
The Geoportal LU services plugin is a plugin for QGIS 3 and requieres an active internet connection.

The plugin uses the python "requests" package. The package is probably already installed, if 
not you may install it using your favourite package manager like pip or easy_install.

## Found any bugs?
If you found a bug or wish for a certain feature you may use the Github issue tracker
to report so.

## Contact
You can contact me by email hallo@frankbroniewski.com, Twitter @frankbroniewski or any other means
on my homepage www.frankbroniewski.com


## Links
* Luxembourgish Geoportal: https://geoportail.lu/de/
* Requests module: http://docs.python-requests.org/en/master/