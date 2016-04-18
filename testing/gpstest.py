#!/usr/bin/env python
import gps

session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
f = open("/home/pi/robo-ops/output", "w")

while True:
    try:
        report = session.next()
#print report
        print session.fix.latitude
        data = str(session.fix.latitude) + "\n"
        f.write(data)
        if report['class'] == 'TPV':
            if hasattr(report, 'class'):
#print report.lat
                pass
    except KeyError:
        pass
    except KeyboardInterrupt:
        quit()
    except StopIteration:
        session = None
        print "GPS has stopped"
