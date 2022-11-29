import pymysql

conn = pymysql.connect(
    host='127.0.0.1', 
    user='root', 
    password='NamchunSQL!@', 
    db='ANIME', 
    charset='utf8'
)
cursor = conn.cursor()

query = 'select * from users_info_tb where user_nm = "asdf"'
cursor.execute(query.upper())

result = cursor.fetchall()
print(result)