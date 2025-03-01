import district_points, wlt, hexafecta, alliance_distribution
import datetime

# Runs every day at 5:00UTC (0:00ET, 7:00IS)
year = 2025

doy = datetime.datetime.utcnow().timetuple().tm_yday
if doy%4==0:
    # print('Scheduler: District Points')
    # district_points.recalc(year)
    print('Scheduler: WLT')
    wlt.recalc(year)
    print('Scheduler: Hexafecta')
    hexafecta.run(year)
    print('Scheduler: Alliance Distribution')
    alliance_distribution.recalc(year)
elif doy%4==1:
    print('Scheduler: WLT')
    wlt.recalc(year)
    print('Scheduler: Hexafecta')
    hexafecta.run(year)
    print('Scheduler: Alliance Distribution')
    alliance_distribution.recalc(year)
    # print('Scheduler: District Points')
    # district_points.recalc(year)
elif doy%4==2:
    print('Scheduler: Hexafecta')
    hexafecta.run(year)
    print('Scheduler: Alliance Distribution')
    alliance_distribution.recalc(year)
    # print('Scheduler: District Points')
    # district_points.recalc(year)
    print('Scheduler: WLT')
    wlt.recalc(year)
else:
    print('Scheduler: Alliance Distribution')
    alliance_distribution.recalc(year)
    # print('Scheduler: District Points')
    # district_points.recalc(year)
    print('Scheduler: WLT')
    wlt.recalc(year)
    print('Scheduler: Hexafecta')
    hexafecta.run(year)
print('Scheduler: Done')