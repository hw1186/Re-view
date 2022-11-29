import os
import pymysql

conn = pymysql.connect(
    host='localhost', 
    user='root', 
    password=os.environ['PASSWORD'], 
    db='ANIME2', 
    charset='utf8'
)
cursor = conn.cursor()

class AnimeDB():    

    def getMainInfo(self, search_name):
        if search_name:
            query = f'SELECT ANIME_NUM, ANIME_NM, IMG_SRC FROM ANIME_INFO_TB WHERE ANIME_NM LIKE "%{search_name}%"'
            cursor.execute(query)

        else:
            cursor.execute("SELECT ANIME_NUM, ANIME_NM, IMG_SRC FROM ANIME_INFO_TB")

        return cursor.fetchall()

    def seq_to_animeInfo(self, anime_num):
        cursor.execute(f"SELECT ANIME_NM, IMG_SRC FROM ANIME_INFO_TB WHERE ANIME_NUM = {anime_num}")

        return cursor.fetchall()

    def create_comment(self, anime_nm, user_nm, comment):
        cursor.execute(f"INSERT INTO COMMENTS_TB(ANIME_NM, USER_NM, COMMENT) VALUES('{anime_nm}', '{user_nm}', '{comment}')")
        conn.commit()

        return True

    def get_comments(self, anime_nm):
        cursor.execute(f"SELECT USER_NM, COMMENT, CREATE_DT FROM COMMENTS_TB WHERE ANIME_NM = '{anime_nm}'")
        
        return cursor.fetchall()

    def get_comment_count(self, anime_nm):
        cursor.execute(f"SELECT COUNT(COMMENT) FROM COMMENTS_TB WHERE ANIME_NM = '{anime_nm}'")

        return cursor.fetchall()

db = AnimeDB()