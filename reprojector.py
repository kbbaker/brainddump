import math

def LatLonToMeters(lat, lon ):
    #Converts given lat/lon in WGS84 Datum to XY in Spherical Mercator EPSG:900913
    originShift = 2 * math.pi * 6378137 / 2.0
    mx = lon * originShift / 180.0
    my = math.log( math.tan((90 + lat) * math.pi / 360.0 )) / (math.pi / 180.0)

    my = my * originShift / 180.0
    return mx, my

def MetersToLatLon(mx, my):
    #Converts XY point from Spherical Mercator EPSG:900913 to lat/lon in WGS84 Datum
    originShift = 2 * math.pi * 6378137 / 2.0
    lon = (mx / originShift) * 180.0
    lat = (my / originShift) * 180.0

    lat = 180 / math.pi * (2 * math.atan( math.exp( lat * math.pi / 180.0)) - math.pi / 2.0)
    return lat, lon

def haversine(lon1, lat1, lon2, lat2):
    #Calculate distance on a sphere in m 
    # converting DD to rad 
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    # using haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    m = 6378137 * c
    return m

def newCoordAlongLine(lon1,lat1, lon2, lat2, distance):
    #calculate new point on edge given a distance along the line   
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    bear = math.atan2(math.sin(lon2-lon1)*math.cos(lat2),math.cos(lat1)*math.sin(lat2)-math.sin(lat1)*math.cos(lat2)*math.cos(lon2-lon1))
    dist = distance / 6378137.00000
    newlat = math.asin(math.sin(lat1)*math.cos(dist) + math.cos(lat1)*math.sin(dist)*math.cos(bear))
    newlon = lon1 + math.atan2(math.sin(bear) * math.sin(dist) * math.cos(lat1), math.cos(dist) - math.sin(lat1) * math.sin(newlat))
    newlon = math.fmod((newlon + 3*math.pi), (2*math.pi))-math.pi
    
    return newlon*180/math.pi, newlat*180/math.pi

def boundsArea(mercLon_ll, mercLat_ll, mercLon_ur, mercLat_ur):
    #Calculates area of mercator coordinates
    Lat_ll, Lon_ll = MetersToLatLon(mercLon_ll, mercLat_ll)
    Lat_ur, Lon_ur = MetersToLatLon(mercLon_ur, mercLat_ur)

    baseX = haversine(Lon_ll, Lat_ll, Lon_ur, Lat_ll)
    heightY = haversine(Lon_ll, Lat_ll, Lon_ll, Lat_ur)

    printArea = round((baseX*heightY)/1000000,3)
    return printArea

def pixelSizeFromMercator(bbox, w, h):
    #Calculates area of mercator coordinates
    Lat_ll, Lon_ll = MetersToLatLon(bbox[0], bbox[1])
    Lat_ur, Lon_ur = MetersToLatLon(bbox[2], bbox[3])

    baseX = haversine(Lon_ll, Lat_ll, Lon_ur, Lat_ll)
    heightY = haversine(Lon_ll, Lat_ll, Lon_ll, Lat_ur)
    
    return max(baseX/w, heightY/h)

#bron:
#https://github.com/djvanderlaan/rijksdriehoek

X0      = 155000
Y0      = 463000
PHI0    = 52.15517440
LAM0    = 5.38720621

def rd_to_wgs(x, y):
    """
    Convert rijksdriehoekcoordinates into WGS84 cooridnates. Input parameters: x (float), y (float). 
    """

    if isinstance(x, (list, tuple)):
        x, y = x

    pqk = [(0, 1, 3235.65389),
        (2, 0, -32.58297),
        (0, 2, -0.24750),
        (2, 1, -0.84978),
        (0, 3, -0.06550),
        (2, 2, -0.01709),
        (1, 0, -0.00738),
        (4, 0, 0.00530),
        (2, 3, -0.00039),
        (4, 1, 0.00033),
        (1, 1, -0.00012)]

    pql = [(1, 0, 5260.52916), 
        (1, 1, 105.94684), 
        (1, 2, 2.45656), 
        (3, 0, -0.81885), 
        (1, 3, 0.05594), 
        (3, 1, -0.05607), 
        (0, 1, 0.01199), 
        (3, 2, -0.00256), 
        (1, 4, 0.00128), 
        (0, 2, 0.00022), 
        (2, 0, -0.00022), 
        (5, 0, 0.00026)]

    dx = 1E-5 * ( x - X0 )
    dy = 1E-5 * ( y - Y0 )
    
    phi = PHI0
    lam = LAM0

    for p, q, k in pqk:
        phi += k * dx**p * dy**q / 3600

    for p, q, l in pql:
        lam += l * dx**p * dy**q / 3600

    return [phi,lam]

def wgs_to_rd(phi, lam):
    """
    Convert WGS84 cooridnates into rijksdriehoekcoordinates. Input parameters: phi (float), lambda (float). 
    """

    pqr = [(0, 1, 190094.945),
           (1, 1, -11832.228),
           (2, 1, -114.221),
           (0, 3, -32.391),
           (1, 0, -0.705),
           (3, 1, -2.34),
           (1, 3, -0.608),
           (0, 2, -0.008),
           (2, 3, 0.148)]
    
    pqs = [(1, 0, 309056.544),
           (0, 2, 3638.893),
           (2, 0, 73.077),
           (1, 2, -157.984),
           (3, 0, 59.788),
           (0, 1, 0.433),
           (2, 2, -6.439),
           (1, 1, -0.032),
           (0, 4, 0.092),
           (1, 4, -0.054)]

    dphi = 0.36 * ( phi - PHI0 )
    dlam = 0.36 * ( lam - LAM0 )

    X = X0
    Y = Y0

    for p, q, r in pqr:
        X += r * dphi**p * dlam**q 

    for p, q, s in pqs:
        Y += s * dphi**p * dlam**q

    return [X,Y]

#source: http://zoologie.umons.ac.be/tc/algorithms.aspx

def lam72ToWGS84(X,Y):

    LongRef = 0.076042943
    nLamb = 0.7716421928
    aCarre = 6378388.**2
    bLamb = 6378388. * (1 - (1 / 297.))
    eCarre = (aCarre - bLamb**2) / aCarre
    KLamb = 11565915.812935
     
    eLamb = math.sqrt(eCarre)
    eSur2 = eLamb / 2.
     
    Tan1 = (X - 150000.01256) / (5400088.4378 - Y)
    Lng = LongRef + (1 / nLamb) * (0.000142043 + math.atan(Tan1))
    RLamb = math.sqrt((X - 150000.01256)**2 + (5400088.4378 - Y)**2)
     
    TanZDemi = (RLamb / KLamb)**(1. / nLamb)
    Lati1 = 2 * math.atan(TanZDemi)
     
    while True:
        eSin = eLamb * math.sin(Lati1)
        Mult1 = 1 - eSin
        Mult2 = 1 + eSin
        Mult = (Mult1 / Mult2)**(eLamb / 2.)
        Lat = (math.pi / 2) - (2 * (math.atan(TanZDemi * Mult)))
        Diff = Lat - Lati1
        Lati1 = Lat
        if math.fabs(Diff) < 0.0000000277777:
            break
    
    Haut = 0
    
    SinLat = math.sin(Lat)
    SinLng = math.sin(Lng)
    CoSinLat = math.cos(Lat)
    CoSinLng = math.cos(Lng)
     
    dx = -125.8
    dy = 79.9
    dz = -100.5
    da = -251.0
    df = -0.000014192702
     
    LWf = 1 / 297
    LWa = 6378388
    LWb = (1 - LWf) * LWa
    LWe2 = (2 * LWf) - (LWf * LWf)
    Adb = 1 / (1 - LWf)
     
    Rn = LWa / math.sqrt(1 - LWe2 * SinLat * SinLat)
    Rm = LWa * (1 - LWe2) / (1 - LWe2 * Lat * Lat)**1.5
     
    DLat = -dx * SinLat * CoSinLng - dy * SinLat * SinLng + dz * CoSinLat
    DLat = DLat + da * (Rn * LWe2 * SinLat * CoSinLat) / LWa
    DLat = DLat + df * (Rm * Adb + Rn / Adb) * SinLat * CoSinLat
    DLat = DLat / (Rm + Haut)
     
    DLng = (-dx * SinLng + dy * CoSinLng) / ((Rn + Haut) * CoSinLat)
    Dh = dx * CoSinLat * CoSinLng + dy * CoSinLat * SinLng + dz * SinLat
    Dh = Dh - da * LWa / Rn + df * Rn * Lat * Lat / Adb
     
    LatWGS84 = ((Lat + DLat) * 180) / math.pi
    LngWGS84 = ((Lng + DLng) * 180) / math.pi
    
    return LatWGS84, LngWGS84

def WGS84ToLam72(Lat,Lng):
    Haut = 0
    
    #conversion to radians
    Lat = (math.pi / 180.) * Lat
    Lng = (math.pi / 180.) * Lng
     
    SinLat = math.sin(Lat)
    SinLng = math.sin(Lng)
    CoSinLat = math.cos(Lat)
    CoSinLng = math.cos(Lng)
     
    dx = 125.8
    dy = -79.9
    dz = 100.5
    da = 251.0
    df = 0.000014192702
     
    LWf = 1 / 297.
    LWa = 6378388.
    LWb = (1 - LWf) * LWa
    LWe2 = (2 * LWf) - (LWf * LWf)
    Adb = 1 / (1 - LWf)
     
    Rn = LWa / math.sqrt(1 - LWe2 * SinLat * SinLat)
    Rm = LWa * (1 - LWe2) / (1 - LWe2 * Lat * Lat)**1.5
     
    DLat = -dx * SinLat * CoSinLng - dy * SinLat * SinLng + dz * CoSinLat
    DLat = DLat + da * (Rn * LWe2 * SinLat * CoSinLat) / LWa
    DLat = DLat + df * (Rm * Adb + Rn / Adb) * SinLat * CoSinLat
    DLat = DLat / (Rm + Haut)
     
    DLng = (-dx * SinLng + dy * CoSinLng) / ((Rn + Haut) * CoSinLat)
    Dh = dx * CoSinLat * CoSinLng + dy * CoSinLat * SinLng + dz * SinLat
    Dh = Dh - da * LWa / Rn + df * Rn * Lat * Lat / Adb
     
    LatBel = (Lat + DLat)
    LngBel = (Lng + DLng)
    
    LongRef = 0.076042943
    bLamb = 6378388. * (1 - (1 / 297.))
    aCarre = 6378388.**2
    eCarre = (aCarre - bLamb**2) / aCarre
    KLamb = 11565915.812935
    nLamb = 0.7716421928
    
    eLamb = math.sqrt(eCarre)
    eSur2 = eLamb / 2.
    
    lat = LatBel
    lng = LngBel
    
    eSinLatitude = eLamb * math.sin(lat)
    TanZDemi = (math.tan((math.pi / 4.) - (lat / 2.))) * (((1 + (eSinLatitude)) / (1 - (eSinLatitude)))**(eSur2))
    
    RLamb = KLamb * ((TanZDemi)**nLamb)
    
    Teta = nLamb * (lng - LongRef)
    
    x = 150000 + 0.01256 + RLamb * math.sin(Teta - 0.000142043)
    y = 5400000 + 88.4378 - RLamb * math.cos(Teta - 0.000142043)  
    
    return x, y