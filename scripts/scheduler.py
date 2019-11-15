import district_points, wlt, hexafecta
import datetime

# Runs every day at 8:00UTC (3:00ET, 10:00IS)

day = datetime.datetime.utcnow().weekday()
if day == 0:    # Monday
    print('Scheduler: District Points')
    district_points.run()
elif day == 1:  # Tuesday
    print('Scheduler: WLT')
    wlt.run()
elif day == 2:  # Wednesday
    print('Scheduler: Hexafecta')
    hexafecta.run()
else:           # Thu-Sun
    print('Scheduler: Nothing Run')