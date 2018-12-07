import gps
import requests
import datetime
# from subprocess import call
# call(["gpsd", "/dev/serial0", "-N", "-S", "5000"])

session = gps.gps(host="127.0.0.1", port="5000", verbose=0, mode=1)
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

while True:
    try:
        report = session.next()
        if report['class'] == 'TPV':
#             print(report)
            if hasattr(report, 'lat') and hasattr(report, 'lon') and hasattr(report, 'time'):
                data = {}
                data['data'] = {'lat': str(report['lat']), 'lon': str(report['lon']), 'speed': str(report['speed'])}
                data['time'] = str(datetime.datetime.now())
                data['id'] = 'dev'
                r = requests.post(
                        url='https://jltr0puvuk.execute-api.us-east-2.amazonaws.com/default/4764final',
                        json=data)
                print(str(r.text))
    except KeyError:
        pass
    except KeyboardInterrupt:
        quit()
    except StopIteration:
        session = None
        print("GPSD has terminated")