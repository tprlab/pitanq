import logging
import PiConf
import time
import math

nyc_lat = 40.7128
nyc_lon = -74.0060

mont_lat= 45.5017
mont_lon = -73.5673

newark_lat = 40.7357
newark_lon = -74.1724

sh_lat = 40.4333
sh_lon = -73.9885

frg_lat = 40.7326
frg_lon = -73.4454

nyc_pos = {"lat" :nyc_lat, "lon" :nyc_lon}
mont_pos = {"lat" :mont_lat, "lon" :mont_lon}
newark_pos = {"lat" :newark_lat, "lon" :newark_lon}
sh_pos = {"lat" :sh_lat, "lon" :sh_lon}
frg_pos = {"lat" :frg_lat, "lon" :frg_lon}






def azimuth(pos1, pos2):
    lat1 = toRadians(pos1["lat"])
    lon1 = toRadians(pos1["lon"])

    lat2 = toRadians(pos2["lat"])
    lon2 = toRadians(pos2["lon"])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    x = math.sin(dlon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)
    return math.atan2(x, y)


def toRadians(a):
    return a * 3.14 / 180;

def toRadians2(a):
    if a < 0:
        return -toRadians(-a)
    arg = a if a <= 180 else a - 360
    return math.radians(arg)



def gps_dist(pos1, pos2):
    if pos1 is None or pos2 is None:
        return -1
    lat1 = pos1["lat"]
    lon1 = pos1["lon"]

    lat2 = pos2["lat"]
    lon2 = pos2["lon"]

    dlat1 = lat1 - lat2
    dlon1 = lon1 - lon2

    dlat = toRadians(dlat1);
    dlon = toRadians(dlon1);

    rlat1 = toRadians(lat1)
    rlat2 = toRadians(lat2)

    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(rlat1) * math.cos(rlat2) * math.sin(dlon / 2) * math.sin(dlon / 2);

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a));

    R = 6371.;
    dist = R * c;

    return dist
        



if __name__ == '__main__': 

    north_az = azimuth(nyc_pos, mont_pos)
    south_az = azimuth(nyc_pos, sh_pos)
    west_az = azimuth(nyc_pos, newark_pos)
    east_az = azimuth(nyc_pos, frg_pos)

    print ("Azimuth: north", north_az, "south", south_az, "west", west_az, "east", east_az)    
    d = gps_dist(nyc_pos, mont_pos)
    print ("Dist", d)    
