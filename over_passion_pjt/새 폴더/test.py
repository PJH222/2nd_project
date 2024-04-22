import datetime as dt


now = dt.datetime.strptime("2023-11-04","%Y-%m-%d")
start_date = now - dt.timedelta(days=5)
end_date = now

print(dt.datetime.date(start_date), dt.datetime.date(end_date))