import datetime
b_date = datetime.date(2001,6,3)
t_date = datetime.date.today()

if t_date.day == b_date.day:
    if t_date.month == b_date.month:
        age = t_date.year - b_date.year
        name = 'Carson'
        print(f'Happy {age} Birthday {name}')
else:
    print("no birthday for you!")
