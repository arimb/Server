import district_points, wlt, hexafecta
import datetime

# Runs every day at 5:00UTC (0:00ET, 7:00IS)
year = 2022;

doy = datetime.datetime.utcnow().timetuple().tm_yday
if doy%3==0:
    print('Scheduler: District Points')
    district_points.recalc(year)
    print('Scheduler: WLT')
    wlt.recalc(year)
    print('Scheduler: Hexafecta')
    hexafecta.run(year)
elif doy%3==1:
    print('Scheduler: WLT')
    wlt.recalc(year)
    print('Scheduler: Hexafecta')
    hexafecta.run(year)
    print('Scheduler: District Points')
    district_points.recalc(year)
else:
    print('Scheduler: Hexafecta')
    hexafecta.run(year)
    print('Scheduler: District Points')
    district_points.recalc(year)
    print('Scheduler: WLT')
    wlt.recalc(year)
print('Scheduler: Done')