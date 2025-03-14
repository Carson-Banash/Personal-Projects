import sqlite3
import random

connection = sqlite3.connect('intro.db')

cursor = connection.cursor()
    # id INTEGER PRIMARY KEY AUTOINCREMENT,

# cursor.execute("""CREATE TABLE test_info (
#     ID INTEGER PRIMARY KEY AUTOINCREMENT,
#     test1 INTEGER,
#     test2 INTEGER,
#     test3 INTEGER
# )
# """)

# start_values = [None, 100, 100, 100]

# cursor.execute("INSERT INTO test_info VALUES (?,?,?,?)", (start_values))
# connection.commit()

# connection.commit()

poss = random.randint(1,3)
movement = random.choice([-5,5,-10,10,-20,20])

print(poss, movement)

#print(data)



cursor.execute("SELECT * FROM test_info WHERE ID=(SELECT max(ID) FROM test_info);")
tpl_result = cursor.fetchone()
result = [*tpl_result]
result[0] = None
print(result)

old = result[poss]
new = old + movement 
result[poss] = new
print(result)

cursor.execute("INSERT INTO test_info VALUES (?,?,?,?)", (result))
connection.commit()


# b = [4, 5, 6, 2, 10]

# # Add corresponding elements using list comprehension
# c = [a[i] + b[i] for i in range(len(a))]

# # Print the result
# print(c)

# res = cursor.execute("SELECT name FROM board_info")
# res.fetchone()

connection.close()