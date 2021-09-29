from datetime import date 


today = date.today()
week_days=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
week_day=today.weekday()
print(week_days[week_day])