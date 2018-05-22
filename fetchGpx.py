import urllib2
import gpxpy.parser as parser

url_of_gpx = 'xxxxxxxxxxx'

file_from_url = urllib2.urlopen(url)

gpx_file = file_from_url.read()

# parse gpx
gpx_parser = parser.GPXParser(file)
gpx_parser.parse()

gpx = gpx_parser.gpx
number_of_points = gpx.get_points_no()

print number_of_points