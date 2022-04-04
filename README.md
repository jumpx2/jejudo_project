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
![Mar-31-2022 16-18-17](https://user-images.githubusercontent.com/81940655/160999657-82192294-eb56-4166-8d19-a9295a6c2da8.gif)
Metabase로 시각화 진행
![Animation](https://user-images.githubusercontent.com/81940655/161478510-ff86a387-aa58-4e42-a0ba-092da88adbd1.gif)
