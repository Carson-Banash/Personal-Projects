import sqlite3

connection = sqlite3.connect('st.db')

cursor = connection.cursor()

sec = ['Grain','Oil','Industrial','Bonds','Gold','Silver']

board_data = [None]

for security in sec:

    while True:
        data = int(input("what is the value for %s: " % (security)))
        if data < 200 and data > 0 and data % 5 == 0:
            board_data.append(data*10)
            break

print(board_data)

cursor.execute("INSERT INTO board_info VALUES (?,?,?,?,?,?,?)", (board_data))
connection.commit()
# res = cursor.execute("SELECT name FROM board_info")
# res.fetchone()

connection.close()