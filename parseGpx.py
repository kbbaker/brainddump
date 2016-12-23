__author__ = 'Kevin'

import gpxpy.parser as parser
import urllib2
import json
import time
import itertools
import glob
from os import path

def encode_coords(wktstring, inverse=False):
    '''Encodes a polyline using Google's polyline algorithm

    See http://code.google.com/apis/maps/documentation/polylinealgorithm.html
    for more information.

    :param coords: Coordinates to transform (list of tuples in order: latitude,
    longitude).
    :type coords: list
    :returns: Google-encoded polyline string.
    :rtype: string
    '''

    result = []

    prev_lat = 0
    prev_lng = 0
    coords = fromWkt(wktstring)
    if inverse:
        coords = coords[::-1]

    for x, y in coords:
        lat, lng = int(y * 1e5), int(x * 1e5)

        d_lat = _encode_value(lat - prev_lat)
        d_lng = _encode_value(lng - prev_lng)

        prev_lat, prev_lng = lat, lng

        result.append(d_lat)
        result.append(d_lng)

    return ''.join(c for r in result for c in r)

def _split_into_chunks(value):
    while value >= 32: #2^5, while there are at least 5 bits

        # first & with 2^5-1, zeros out all the bits other than the first five
        # then OR with 0x20 if another bit chunk follows
        yield (value & 31) | 0x20
        value >>= 5
    yield value

def _encode_value(value):
    # Step 2 & 4
    value = ~(value << 1) if value < 0 else (value << 1)

    # Step 5 - 8
    chunks = _split_into_chunks(value)

    # Step 9-10
    return (chr(chunk + 63) for chunk in chunks)

def decode(point_str):
    '''Decodes a polyline that has been encoded using Google's algorithm
    http://code.google.com/apis/maps/documentation/polylinealgorithm.html

    This is a generic method that returns a list of (latitude, longitude)
    tuples.

    :param point_str: Encoded polyline string.
    :type point_str: string
    :returns: List of 2-tuples where each tuple is (latitude, longitude)
    :rtype: list

    '''

    # sone coordinate offset is represented by 4 to 5 binary chunks
    coord_chunks = [[]]
    for char in point_str:

        # convert each character to decimal from ascii
        value = ord(char) - 63

        # values that have a chunk following have an extra 1 on the left
        split_after = not (value & 0x20)
        value &= 0x1F

        coord_chunks[-1].append(value)

        if split_after:
                coord_chunks.append([])

    del coord_chunks[-1]

    coords = []

    for coord_chunk in coord_chunks:
        coord = 0

        for i, chunk in enumerate(coord_chunk):
            coord |= chunk << (i * 5)

        #there is a 1 on the right if the coord is negative
        if coord & 0x1:
            coord = ~coord #invert
        coord >>= 1
        coord /= 100000.0

        coords.append(coord)

    # convert the 1 dimensional list to a 2 dimensional list and offsets to
    # actual values
    points = []
    prev_x = 0
    prev_y = 0
    for i in xrange(0, len(coords) - 1, 2):
        if coords[i] == 0 and coords[i + 1] == 0:
            continue

        prev_x += coords[i + 1]
        prev_y += coords[i]
        # a round to 6 digits ensures that the floats are the same as when
        # they were encoded
        points.append((round(prev_x, 6), round(prev_y, 6)))

    return points

def toWkt(array):
    geom = 'LINESTRING (%s)'
    coords = []
    for coord in array:
        coords.append('%s %s'%(coord[0],coord[1]))
    return geom%','.join(coords)


def build_url(coords, timestamp):
    url= "https://router.project-osrm.org/match/v1/driving/" #fill in server for OSRM match
    location = "%s,%s"
    locations = []
    for coord in coords:
        locations.append(location%(coord[0],coord[1]))
    url += ';'.join(locations)
    #print ','.join(map(str,timestamp))
    param = "?timestamps=" + ';'.join(map(str,timestamp))
    url += param
    return url

def fetch_result(url):
    #fetch result from route json#
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    result = json.load(response)

    return result

fileList = ['activity_1146328787.gpx']
f = open('output', 'w')

keys = ['file_name','gpx_index','gpx_point_x', 'gpx_point_y', 'match_point_x', 'match_point_y', 'way_id', 'gpx_height', 'gpx_speed']
f.write(';'.join(keys) + '\n')


for file in fileList:

    gpx_file = open('gpx/' + file, 'r' ) #fill in gpx to parse

    #parse gpx
    gpx_parser = parser.GPXParser( gpx_file )
    gpx_parser.parse()

    gpx_file.close()

    gpx = gpx_parser.gpx
    number_of_points = gpx.get_points_no()
    tracks =  gpx.tracks
    #initiate output arrays
    coords = []
    timestamp = []
    indices = []
    elevation = []
    speed = []

    i = 0

    index = 0
    for track_no in range(len(tracks)):
        track = tracks[track_no]
        for segment_no in range(len(track.segments)):
            segment = track.segments[segment_no]
            for point_no in range(len(segment.points)):
                point = segment.points[point_no]
                speed_at_point = segment.get_speed(point_no)
                if speed_at_point == None:
                    speed_at_point = 0
                #iterate in slices of 50 over gpx points
                #also check if the slice is smaller than 50 at the end of the gpx points array
                if i < 50 and index < number_of_points - 1:
                    coords.append((point.longitude,point.latitude))
                    timestamp.append(int(time.mktime(point.time.timetuple())))
                    indices.append(index)
                    elevation.append(point.elevation)
                    speed.append(speed_at_point)
                    i += 1
                else:
                    #fetch match based on slice
                    i = 2
                    url = build_url(coords, timestamp)
                    print url
                    try:
                        result = fetch_result(url)
                        tracepoints = result['tracepoints']
                        result['matchings']
                        #print resulting geometry on OSM Way
                        for geom in result['matchings']:
                            print toWkt(decode(geom['geometry']))
                        #fetch output for json response
                        for j,coord in enumerate(coords):
                            if tracepoints[j] != None:
                                match = tracepoints[j]['location']
                                #wayInfo = json.loads(tracepoints[j]['name'])
                                wayInfo = [0,0]
                                coord = {'file_name': file,'gpx_index':indices[j],'gpx_point_x':coord[0], 'gpx_point_y':coord[1], 'match_point_x':match[0], 'match_point_y':match[1], 'way_id':wayInfo[0], 'gpx_height':elevation[j], 'gpx_speed':speed[j]}
                                output = []
                                for key in keys:
                                    output.append(str(coord[key]))
                                f.write(';'.join(output))
                                f.write('\n')
                        #create overlap between slices to avoid missing end point in match
                    except:
                        print "bad url"
                    coords = coords[-2:]
                    timestamp = timestamp[-2:]
                    indices = indices[-2:]
                    elevation = elevation[-2:]
                    speed = speed[-2:]
                index += 1
