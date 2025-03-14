import datetime
b_date = datetime.date(2001,6,3)
p_date = datetime.date(2022,6,3)
t_date = datetime.date.today()

if p_date.day == t_date.day:
        age = p_date.year - b_date.year
        name = 'Carson'
        print(f'Happy {age} Birthday {name}')
else:
    print("no birthday for you!")
