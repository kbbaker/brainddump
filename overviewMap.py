__author__ = 'Kevin'

import mapnik
# Setup the map
map_canvas = mapnik.Map(500, 500)
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

# Create a symbolizer to draw the lines
style = mapnik.Style()
rule = mapnik.Rule()
track_stk = mapnik.Stroke()
track_stk.width = 5
line_symbolizer = mapnik.LineSymbolizer(track_stk)
line_symbolizer.smooth = 1
rule.symbols.append(line_symbolizer)
style.rules.append(rule)
map_canvas.append_style('GPS_tracking_line', style)

# Create a layer to hold the ponts
layer = mapnik.Layer('GPS_tracking_line')
layer.datasource = mapnik.Ogr(file="route.kml", layer_by_index=1)
layer.styles.append('GPS_tracking_line')
map_canvas.layers.append(layer)

# Create a layer to hold the ponts
layer = mapnik.Layer('GPS_tracking_points')
layer.datasource = mapnik.Ogr(file="route.kml", layer_by_index=0)
layer.styles.append('GPS_tracking_points')
map_canvas.layers.append(layer)

# Save the map
map_canvas.zoom_all()
mapnik.render_to_file(map_canvas, 'GPS_tracking_points.png', 'png')