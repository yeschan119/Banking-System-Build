# Build a Banking System(은행시스템 구현 프로젝트)
Build a Banking System
## purpose
  + 은행DB를 서버로 구축하고 은행시스템을 그대로 구현할 수 있는 Bank System 개발
  
## members
  + 1인 프로젝트
  
## Tech & Skills
  + MySQL
  + Python
  + DataBase
  + AWS

## Project Schedule
  + 1주차 ER-Model을 이용한 스키마 디자인 및 Entity, Relational type 설정
  + 2주차 ER-Model을 Relational Model로 변환 후 AWS RDS, MySQL 환결 설치
  + 3주차 python을 이용한 애플리케이션 구현 및 테스팅
  + 4주차 은행 시스템 애플리케이션 GUI 구성

## 1주차 ER-Model & conceptual DB
  + ER-Model 
![스크린샷 2021-12-05 오전 12 35 22](https://user-images.githubusercontent.com/83147205/144731232-042b9c3b-3e2b-4566-9db8-89077b49c6ed.png)
  
  + conceptual DB
    + Entity type: User, Account, Admin, Log
    + Relationship type: record, manage
    + Entity type attrbitutes
      + User: SSN, Lname, Fname, Bdate, NickName
      + Account: AccNum, SSN, Balance, PassWord
      + Admin: Email, PW
      + Log: LogID, Name, Account, Withdraw, Deposit, LogDate
    + Relationship type attributes: record, manag
 
 ## 2주차 Relational Model로 변환 후 AWS RDS, MySQL 설치
  + Logical DB
  
<img width="774" alt="스크린샷 2021-12-05 오전 1 09 19" src="https://user-images.githubusercontent.com/83147205/144731343-1f14a941-327a-4855-a94f-a04e7033e8bd.png">

  + AWS 서버에 MySQL을 이용한 DB생성
    + 스키마를 참조한 table 생성
      + User table
      + <img width="465" alt="스크린샷 2021-12-05 오전 12 54 11" src="https://user-images.githubusercontent.com/83147205/144731578-cfeb6fa1-b955-4460-909c-2c29ee67eeac.png">
      + Account table
      + <img width="416" alt="스크린샷 2021-12-05 오전 1 21 21" src="https://user-images.githubusercontent.com/83147205/144731584-fe1e009a-022d-4b14-a7c5-d95530786307.png">
      + Log table
      + <img width="539" alt="스크린샷 2021-12-05 오전 1 22 54" src="https://user-images.githubusercontent.com/83147205/144731598-33b6db8d-c002-402a-bfe0-35762b78693c.png">

## 3주차 python을 이용한 애플리케이션 구현 및 테스팅
  + 결과 테스팅 영상

  + [![스크린샷 2021-12-05 오전 11 43 40](https://user-images.githubusercontent.com/83147205/144731461-30f69951-297b-4f0f-aea2-1bfcdd7d8703.png)](https://youtu.be/NZsOyLqf7Js "은행 DB 테스팅 영상")
