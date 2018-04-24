# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GeoportailLU
                                 A QGIS plugin
 Use services from the luxembourgish Geoportal in QGIS
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2018-04-20
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Dipl. Geogr. Frank Broniewski
        email                : hallo@frankbroniewski.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import os.path
import json

from osgeo import ogr
from osgeo import osr

from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

from qgis.core import QgsProject, QgsGeometry, QgsFeature, QgsVectorLayer

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .geoportail_lu_dialog import GeoportailLUDialog

from .services import search


class GeoportailLU:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'GeoportailLU_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = GeoportailLUDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Geoportal LU')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'Geoportal LU')
        self.toolbar.setObjectName(u'Geoportal LU')

        # shortcuts
        self.project = QgsProject.instance()
        self.root = self.project.layerTreeRoot()
        self.crs = self.project.crs().authid()

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('GeoportailLU', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToWebMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/geoportail_lu/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u''),
            status_tip=self.tr(u'Geoportal LU'),
            callback=self.run,
            parent=self.iface.mainWindow())

        self.dlg.searchButton.clicked.connect(self.update_search)
        self.dlg.addButton.clicked.connect(self.add_result)


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginWebMenu(
                self.tr(u'&Geoportal LU'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        # get the current CRS from the project in case it changed since
        # project load
        self.crs = self.project.crs().authid()
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()


    def update_search(self):
        """Update the search field with results from input and geoportal
        results"""
        dlg = self.dlg.searchField
        # stopp signal from emitting events while loading results
        dlg.blockSignals(True)

        if len(dlg.currentText()) > 1:
            search_text = dlg.currentText()
            # remove possible entries
            dlg.clear()
            dlg.addItem(search_text)
            # results is a GeoJSON FeatureCollection
            # update combobox with new values
            results = search(dlg.currentText(), 9)
            for result in results['features']:
                dlg.addItem(result['properties']['label'], result)
            dlg.showPopup()

        dlg.blockSignals(False)
        return


    def add_result(self):
        """Get the selected search result from the search field and add it as
        a layer to the map"""
        dlg = self.dlg.searchField

        if dlg.currentIndex() > 0:
            result = dlg.currentData()
            geometry_type = result['geometry']['type']
            properties = result['properties']

            project_crs = int(self.crs.replace('EPSG:', ''))

            # create the geometry from json and reproject eventually
            ogr_geom = ogr.CreateGeometryFromJson(
                json.dumps(result['geometry']))
            # reproject to project's CRS if necessary
            if project_crs != 4326:
                source_srs = osr.SpatialReference()
                source_srs.ImportFromEPSG(4326)
                target_srs = osr.SpatialReference()
                target_srs.ImportFromEPSG(project_crs)
                transformation = osr.CoordinateTransformation(source_srs,
                                                              target_srs)
                ogr_geom.Transform(transformation)

            # create the QGIS Geometry and create fields
            geometry = QgsGeometry.fromWkt(ogr_geom.ExportToWkt())
            # layer string
            fields = '&'.join(['field={}:string(200)'.format(k)
                               for k, v in properties.items()])
            create_opts = '{}?crs=epsg:{}&{}'.format(geometry_type,
                                                     project_crs, fields)
            result_layer = QgsVectorLayer(create_opts, properties['label'],
                                          'memory')
            fields = result_layer.fields()
            # add feature if layer is valid
            if result_layer.isValid():
                data_provider = result_layer.dataProvider()
                feature = QgsFeature()
                feature.setGeometry(geometry)
                feature.setFields(fields)
                for k, v in properties.items():
                    # feature.setAttribute(k, v)
                    feature[k] = v
                data_provider.addFeatures([feature])
                result_layer.updateExtents()
                # add result to map layer tree
                self.project.addMapLayer(result_layer, False)
                # add a group for storing selected search results as memory
                # layer
                group = self._get_group(self.tr(u'Search Results'))
                group.addLayer(result_layer)
                # zoom to feature & update map
                extent = geometry.boundingBox()
                self.iface.mapCanvas().zoomToFeatureExtent(extent)
                self.iface.mapCanvas().refresh()
                result_layer.triggerRepaint()
            else:
                msg = 'Cannot load result layer'
                self.iface.messageBar().pushCritical('Search Error', msg)

        else:
            self.iface.messageBar().pushInfo('Info', 'Nothing do show!')


    def _get_group(self, group_name):
        """Get a Layer Tree group by its name. If the group is not found
        it is created."""
        group = self.root.findGroup(group_name)

        if group is None:
            group = self.root.addGroup(group_name)

        return group