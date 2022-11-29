import pymysql
import os
from hashlib import sha256

conn = pymysql.connect(
    host='localhost', 
    user='root', 
    password=os.environ['PASSWORD'], 
    db='ANIME2', 
    charset='utf8'
)
cursor = conn.cursor()
        
def isExist(username):
    cursor.execute(f'SELECT * FROM USERS_INFO_TB WHERE USER_NM = "{username}"')
    
    if cursor.fetchall():
        return True
    return False

def register(username, password, email):
    password = sha256(password.encode('utf-8')).hexdigest()
    cursor.execute(f'INSERT INTO USERS_INFO_TB(USER_NM, PASSWORD, EMAIL) VALUES("{username}", "{password}", "{email}")')
    conn.commit()

    return True

def check_password(username, password):
    cursor.execute(f'SELECT PASSWORD FROM USERS_INFO_TB WHERE USER_NM = "{username}"')

    cmp_password = cursor.fetchall()[0][0]
    if cmp_password != sha256(password.encode('utf-8')).hexdigest():
        return False
    return True