import gps

gs = gps.gps("localhost", "2947")
gs.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

for i in range(0,10):
    report = gs.next()
    print (report)
