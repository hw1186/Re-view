import pymysql
import os
import requests
from bs4 import BeautifulSoup

conn = pymysql.connect(
    host='localhost',
    user='root',
    password=os.environ['PASSWORD'],
    db='ANIME2',
    charset='utf8'
)
cursor = conn.cursor()

def insertANIME_INFO(title, img_src, country, air_dt):
    print(title, img_src, country, air_dt)
    cursor.execute(f'INSERT INTO ANIME_INFO_TB(ANIME_NM, IMG_SRC, COUNTRY_NM, AIR_DT) VALUES("{title}", "{img_src}", "{country}", "{air_dt}")')

def insertANIME_GENRE(title, genre):
    print(title, genre)
    cursor.execute(f'INSERT INTO ANIME_GENRE_TB(ANIME_NM, GENRE) VALUES("{title}", "{genre}")')


def getInfo(title):
    # 제목, 장르, 제작국가, 방영일 return
    global img_src, genre, country, air_date

    url = f"https://ohli24.net/c/{title}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    # 이미지 추출
    try:
        div = soup.select('div.image > div > img')[0]
        img_src = div.get('src')

        if img_src.startswith('../'):
            img_src = img_src.replace('..', 'https://ohli24.net')
    except:
        img_src = '-에러- 알아서 넣자~'    

    # 장르, 제작국가, 방영일 추출
    infos = soup.select('div.list > p')
    for info in infos:
        info = info.text

        if '장르' in info:
            genre = info.replace('\n장르\n', '').replace('\n', '')

        elif '제작국가' in info:
            country = info.replace('\n제작국가\n', '').replace('\n', '')

        elif '방영일' in info:
            air_date = info.replace('\n방영일\n', '').replace('\n', '')

            # 정신 나간 예외 처리
            air_date = air_date.replace('년 ', '-')
            air_date = air_date.replace('월 ', '-')
            air_date = air_date.replace('일', '-')

            air_date = air_date.replace('. ', '-')
            air_date = air_date.replace('.', '-')[:10]

            if len(air_date) != 10 or "일" in air_date or 'xx' in air_date:
                air_date = '0000:00:00'

    return img_src, genre, country, air_date

def setTitle():
    bo_table = {'ing':1, 'fin':42, 'theater':15, 's':5}

    # 방영중, 완결, 극장판, 스페셜
    for table in bo_table.keys():
        # 각 테이블에 맞는 페이지 수 만큼 반복
        for page in range(bo_table[table]):
            print(f"\n============= {table} ============= {page + 1} =============\n")
            url = f"https://ohli24.net/bbs/board.php?bo_table={table}&page={page + 1}"
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')

            titles = soup.select('div.post-title')
            for title in titles:
                title = title.text.replace('\n', '')[:-1]
                if title[0] == ' ':
                    title = title[1:]

                if title == '어째서 여기에 선생님이?!' and table == 's':
                    continue

                infos = getInfo(title)
                insertANIME_INFO(title, infos[0], infos[2], infos[3])
                
                for genre in infos[1].split(', '):
                    insertANIME_GENRE(title, genre)

if __name__ == "__main__":
    title, infos = setTitle()