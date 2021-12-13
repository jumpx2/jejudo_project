import os
from flask import Flask, render_template, redirect, session, request
from form import RegisterForm
from form import LoginForm
from models import NewPerson
from models import db
from flask_wtf.csrf import CSRFProtect
import pickle
import pandas as pd
import sklearn
import category_encoders
import numpy as np
from flask_sqlalchemy import SQLAlchemy
import requests
import json
import psycopg2

app = Flask(__name__)
csrf = CSRFProtect(app)
csrf.init_app(app)

base = os.path.abspath(os.path.dirname(__file__))
dbfile = os.path.join(base, 'login.db')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']= True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['SECRET_KEY'] = "secretkey123123123"
app.config['WTF_CSRF_SECRET_KEY'] = "secretkey123123123"

db.init_app(app)
db.app = app
db.create_all()



@app.route('/')
def mainpage():
    userid = session.get('userid',None)
    return render_template('main.html', userid=userid)

@app.route('/newper', methods=['GET', 'POST'])
def newper():
    form = RegisterForm()
    if form.validate_on_submit():
      newp = NewPerson()
      newp.userid = form.data.get('userid')
      newp.username = form.data.get('username')
      newp.password = form.data.get('password')

      db.session.add(newp)
      db.session.commit()

      print('yes')

      return redirect('/')
      
    return render_template('newper.html',form=form)

@app.route('/login/', methods=['GET', 'POST'])
def login():
  forms = LoginForm()
  if forms.validate_on_submit():
    print('{} 로그인 했습니다.'.format(forms.data.get('userid')))
    session['userid'] = forms.data.get('userid')
    return redirect('/home')
  return render_template('login.html', form=forms)
  
@app.route('/logout', methods=['GET'])
def logout():
  session.pop('userid', None)
  return redirect('/')


@app.route('/home')
def home():
  return render_template('home.html')


@app.route('/about')
def about():
  return render_template('about.html')


@app.route('/Portfolio')
def portfolio():
  if request.method =='GET':
    
    req = request.query_string
    String = req.decode('utf-8')
    color = String.split('&')
    colors = []
    for i in color:
      value = i.replace('color=', '')
      colors.append(value)

    if colors != ['']:
      with open('pipe.pkl', 'rb') as pickle_file:
        model = pickle.load(pickle_file)

      X_test = pd.DataFrame(index = ['base_year_month', 'base_year', 'biz_type', 'sex', 'age_range','day_of_week'],
                          data=[colors[1], int(2021), colors[0], colors[2], colors[3]+str('대'), colors[4]], columns=['0']).T
      
      if X_test['base_year_month'].values[0] == type(str):
        X_test['base_year_month'] = int(X_test['base_year_month'])

      if X_test['biz_type'].values[0] == 'beef':
        X_test['biz_type'].values[0] = '고기'

      elif X_test['biz_type'].values[0] == 'korean_food':
        X_test['biz_type'].values[0] = '한식'

      elif X_test['biz_type'].values[0] == 'japaness_food':
        X_test['biz_type'].values[0] = '일식'

      elif X_test['biz_type'].values[0] == 'western_food':
        X_test['biz_type'].values[0] = '양식'

      elif X_test['biz_type'].values[0] == 'chiness_food':
        X_test['biz_type'].values[0] = '중식'

      elif X_test['biz_type'].values[0] == 'bunsik':
        X_test['biz_type'].values[0] = '분식'

      elif X_test['biz_type'].values[0] == 'dessert':
        X_test['biz_type'].values[0] = '디저트'

      elif X_test['biz_type'].values[0] == 'fusion':
        X_test['biz_type'].values[0] = '퓨전'

      elif X_test['biz_type'].values[0] == 'buffet':
        X_test['biz_type'].values[0] = '부페'

      elif X_test['biz_type'].values[0] == 'fast_food':
        X_test['biz_type'].values[0] = '패스트푸드'

      else:
        X_test['biz_type'].values[0] = '기타'

      if X_test['sex'].values[0] == 'male':
        X_test['sex'].values[0] = '남자'
      else:
        X_test['sex'].values[0] = '여자'
      if X_test['day_of_week'].values[0] == 'mon':
        X_test['day_of_week'].values[0] = '월'
      elif X_test['day_of_week'].values[0] == 'tue':
        X_test['day_of_week'].values[0] = '화'
      elif X_test['day_of_week'].values[0] == 'wen':
        X_test['day_of_week'].values[0] = '수'
      elif X_test['day_of_week'].values[0] == 'thu':
        X_test['day_of_week'].values[0] = '목'
      elif X_test['day_of_week'].values[0] == 'fri':
        X_test['day_of_week'].values[0] = '금'
      elif X_test['day_of_week'].values[0] == 'sat':
        X_test['day_of_week'].values[0] = '토'
      else:
        X_test['day_of_week'].values[0] = '일'

      if X_test['biz_type'].values[0] == '고기':
        X_test['biz_type'].values[0] = '고기요리'
      else:
        X_test['biz_type'].values[0]
        
      user_count = model.predict(X_test)
      user_count = np.round(user_count, 1)

      user = user_count[0]
      month = X_test['base_year_month'].values[0]
      year = X_test['base_year'].values[0]
      biztype = X_test['biz_type'].values[0]
      sex = X_test['sex'].values[0]
      age =X_test['age_range'].values[0]
      week = X_test['day_of_week'].values[0]

      
      if type(X_test) == series:
        def postgre():
          connection = psycopg2.connect(
          host="castor.db.elephantsql.com",
          database="ksscqlnz",
          user="ksscqlnz",
          password="b60wugaYTpdHgnMDucQAENPIFSkMLncg")

          cur = connection.cursor()
          return connection, cur
      connection, cur = postgre()

      cur.execute(""" INSERT INTO jeju (base_year_month, base_year, bize_type, sex, age_range, day_of_week, user_count) 
      VALUES (%s, %s, %s, %s, %s, %s, %s);""",(month, year, biztype, sex, age, week, user))
      
      connection.commit()
      cur.close()
      connection.close()
      

    else:
      user_count=0

    if user_count != 0:

      client_id = 'gOskwwQzbEutCU9wQ90k'
      client_key = '5Na6Pkwa_w'
      
      
      if X_test['biz_type'].values[0] == '고기':
        X_test['biz_type'].values[0] = '고기요리'
      else:
        X_test['biz_type'].values[0]
      

      naver_url = 'https://openapi.naver.com/v1/search/local?display=5&sort=comment&query=제주도 '+ X_test['biz_type'].values[0]
      headers = {"X-Naver-Client-Id":client_id, "X-Naver-Client-Secret":client_key}
      response = requests.get(naver_url, headers=headers)
      names = []
      roads = []
      url = 'http://127.0.0.1:3000/public/dashboard/cb6e2602-7cb7-4f81-9ce1-d6064e6de495'
      data = response.json()
      for i in data['items']:
        title = i['title']
        road = i['roadAddress']
        names.append(title)
        roads.append(road)
    else:
      names =''
      roads =''
      url = ''

  return render_template('Portfolio.html', user_count=user_count, names=names, roads=roads, url=url)


if __name__ == '__main__':  
  csrf = CSRFProtect(app)
  csrf.init_app(app)

  base = os.path.abspath(os.path.dirname(__file__))
  dbfile = os.path.join(base, 'login.db')

  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
  app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']= True
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
  app.config['SECRET_KEY'] = "secretkey123123123"
  app.config['WTF_CSRF_SECRET_KEY'] = "secretkey123123123"

  db.init_app(app)
  db.app = app
  db.create_all()

  app.run(host='127.0.0.1', port=5000, debug=True)
