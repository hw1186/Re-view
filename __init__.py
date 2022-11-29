from flask import *
from flask_mail import Mail, Message
from AnimeDB import AnimeDB
from math import ceil
import UserDB

def calcuLimit(result, currentPage):
    limit = 20
    if len(result) / currentPage < limit:
        limit = len(result) % limit
    
    return limit



app = Flask(__name__)
Adb = AnimeDB()

default = Adb.getMainInfo(None)
limit = calcuLimit(default, currentPage=1)
end = ceil(len(default)/20)



@app.route('/')
def main():
    return render_template('main.html', result=default, currentPage=1, limit=20, end=end, session=session)



@app.route('/page=<int:currentPage>')
def go_to(currentPage):
    limit = calcuLimit(default, currentPage)
    end = ceil(len(default)/20)

    return render_template('main.html', result=default, currentPage=currentPage, limit=limit, end=end)



@app.route('/search', methods=["POST", "GET"])
def search():
    anime_nm = request.form['anime_nm']

    if anime_nm:            
        return redirect(f'/search={anime_nm}&page=1')
    else:
        return redirect(url_for('main'))



@app.route('/search=<anime_nm>&page=<int:currentPage>')
def search_page(anime_nm, currentPage):
    if anime_nm:
        result = Adb.getMainInfo(anime_nm)
        limit = calcuLimit(result, currentPage)
        end = ceil(len(result)/20)

        return render_template('main.html', result=result, currentPage=currentPage, limit=limit, anime_nm=anime_nm, end=end)
    
    else:
        return redirect(url_for('main'))



@app.route('/anime_num=<int:anime_num>', methods=["POST", "GET"])
def review(anime_num):
    result = Adb.seq_to_animeInfo(anime_num)              # ANIME_NM, IMG_SRC
    anime_nm = result[0][0]

    comments = Adb.get_comments(anime_nm)                 # USER_NM, COMMENT, CREATE_DT
    comments_cnt = Adb.get_comment_count(anime_nm)[0][0]  # COMMENTS_CNT

    if request.method == "GET":
        return render_template('review.html', result=result, comments=comments, cnt=comments_cnt)
    else:
        if not session:
            flash('Login first')
            return redirect(url_for('login'))
        else:
            comment = request.form['comment']
            Adb.create_comment(anime_nm=anime_nm, user_nm=session['id'], comment=comment)

            return redirect(f'/anime_num={anime_num}')



@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template('register.html')
    else:
        username = request.form['username']
        password = request.form['password']
        password_confirm = request.form['password_confirm']
        email = request.form['email']

        if not (username and password and password_confirm and email):
            flash("Please enter all of them")
            return redirect(url_for('register'))

        elif password != password_confirm:
            flash("Password Incorrect")
            return redirect(url_for('register'))

        else:
            if UserDB.isExist(username):
                flash("A user with this username already exists")
                return redirect(url_for('register'))
            else:
                UserDB.register(username, password, email)
                flash(f"{username}님 환영합니다")
                return redirect(url_for('main'))



@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        username = request.form['username']
        password = request.form['password']

        if not (username and password):
            flash("Please enter all of them")
            return redirect(url_for('login'))
            
        else:
            if not UserDB.isExist(username):
                flash("Username doesn't exist")
                return redirect(url_for('login'))

            elif not UserDB.check_password(username, password):
                flash("Password Incorrect")
                return redirect(url_for('login'))

            else:
                session['id'] = username
                flash("로그인 성공")
                return redirect(url_for('main'))



@app.route('/logout')
def logout():
    session.pop('id', None)
    return redirect(url_for('main'))

@app.route('/user=<user_nm>', methods=["POST", "GET"])
def user_page(user_nm):
    # return render_template('user_page.html', user_nm=user_nm)
    if request.method == "GET":
        return render_template('user_page.html', user_nm=user_nm)
    else:
        feedback = request.form.get('ssti') or None
        html = '''
            <html>
                <center>
                    "%s"
                    <br>
                    <p>피드백 잘 수용하겠습니다!</p>
                </center>
            </html>
        ''' % feedback

        return render_template_string(html)

@app.route('/mypage')
def mypage(): 
    username = session['id']
    return redirect(f'user={username}')
    # return render_template('user_page.html', user_nm=session['id'])

@app.route('/hidden')
def hidden(): return render_template('hidden.html')

@app.route('/about')
def about(): return render_template('about.html')

@app.route('/bug_bounty')
def bug_bounty(): return render_template('bug_bounty.html')

@app.route('/test')
def test(): return render_template('test.html')





if __name__ == "__main__":
    app.secret_key = "SCA{H3ll0_W0r1d!}"
    app.run(debug=True, host='0.0.0.0', port=80)
