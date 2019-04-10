import gps
import logging

class gpss:
    gpss = gps.gps(host="localhost", port="2947")
    gpss.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

    def getRaw(self):
        try:
            return self.gpss.next()
        except:
            logging.exception("Cannot get gps data")
        return None
            

    def getCoords(self):
        r = self.getRaw()
        if r is None:
            return None, None
        print (r)

        if r['class'] == 'TPV':
            if hasattr(r, 'lon'):
                return r.lat, r.lon
        return None, None

    def close(self):
        self.gpss.close()



if __name__ == '__main__': 
    
    g = gpss()

    for i in range(0,10):
        lat, lon = g.getCoords()
        print(i, lat, lon)

