import district_points, wlt, hexafecta
import datetime

# Runs every day at 5:00UTC (0:00ET, 7:00IS)

doy = datetime.datetime.utcnow().timetuple().tm_yday
if doy%3==0:
    print('Scheduler: District Points')
    district_points.run()
    print('Scheduler: WLT')
    wlt.run()
    print('Scheduler: Hexafecta')
    hexafecta.run()
elif doy%3==1:
    print('Scheduler: WLT')
    wlt.run()
    print('Scheduler: Hexafecta')
    hexafecta.run()
    print('Scheduler: District Points')
    district_points.run()
else:
    print('Scheduler: Hexafecta')
    hexafecta.run()
    print('Scheduler: District Points')
    district_points.run()
    print('Scheduler: WLT')
    wlt.run()
print('Scheduler: Done')