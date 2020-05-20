#!/bin/bash

# copy the plugin files to the QGIS plugin folder of the current user
# delete the existing plugin beforehand

PLUGIN_DIR="$HOME/.local/share/QGIS/QGIS3/profiles/default/python/plugins/geoportail_lu/"
SRC_DIR="$PWD"

# remove the old stuff
rm -rf "$PLUGIN_DIR"

mkdir -p "$PLUGIN_DIR"
# copy over the new things
cp -a "$SRC_DIR/"*.py "$SRC_DIR/"README.md "$SRC_DIR/"*.txt \
      "$SRC_DIR/"*.ui "$SRC_DIR/"resources.qrc "$SRC_DIR/"icon.png \
      "$SRC_DIR/"LICENSE "$SRC_DIR/"i18n \
      "$PLUGIN_DIR"