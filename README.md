# jejudo_project

- 공공 API를 사용해 제주도 음식점 이용객 예측 모델입니다.   
- 모델 예측을 진행함과 동시에 naver api를 사용해  
  선택한 음식 종류 중 comment가 많은 TOP5의 정보를 추출합니다.  

---
- 로그인 관련 DB는 SQLite3를 사용  
- 데이터를 입력받고 대시보드에 추가하는 DB는 psycopg2를 사용해 postgresql에 연결  

---

- Jinja 문법을 사용해 Template 작성  

---

- heroku를 사용해 배포  
- Dashboard -> docker를 통해 metabase를 실행 
