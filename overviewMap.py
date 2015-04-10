__author__ = 'Kevin'

import mapnik
# Setup the map
map_canvas = mapnik.Map(width_in_px, height_in_px)
map_canvas.background = mapnik.Color('rgb(0,0,0,0)') # transparent

# Create a symbolizer to draw the points
style = mapnik.Style()
rule = mapnik.Rule()
point_symbolizer = mapnik.MarkersSymbolizer()
point_symbolizer.allow_overlap = True
point_symbolizer.opacity = 0.5 # semi-transparent
rule.symbols.append(point_symbolizer)
style.rules.append(rule)
map_canvas.append_style('GPS_tracking_points', style)

# Create a layer to hold the ponts
layer = mapnik.Layer('GPS_tracking_points')
layer.datasource = mapnik.Ogr(file="Laatste_100_km_Parijs_Roubaix_2015.kmz", layer_by_index=0)
layer.styles.append('GPS_tracking_points')
map_canvas.layers.append(layer)

# Save the map
map_canvas.zoom_all()
mapnik.render_to_file(map_canvas, 'GPS_tracking_points.png', 'png')