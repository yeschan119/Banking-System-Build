# Build a Banking System
Banking System Implementation Project

[한국어 🇰🇷](README.ko.md)

## Purpose
  + Develop a banking system that builds a bank database as a server and fully implements core banking system functionality

## Members
  + Solo project

## Tech & Skills
  + MySQL
  + Python
  + Database
  + AWS

## Project Schedule
  + Week 1: Schema design using an ER model and definition of entity and relationship types
  + Week 2: Convert ER model to a relational model and set up AWS RDS and MySQL environment
  + Week 3: Application implementation and testing using Python
  + Week 4: GUI development for the banking system application

## Week 1: ER Model & Conceptual Database
  + ER Model
![ER Model](https://user-images.githubusercontent.com/83147205/144731232-042b9c3b-3e2b-4566-9db8-89077b49c6ed.png)
  
  + Conceptual Database
    + Entity types: User, Account, Admin, Log
    + Relationship types: Record, Manage
    + Entity type attributes
      + User: SSN, Lname, Fname, Bdate, NickName
      + Account: AccNum, SSN, Balance, Password
      + Admin: Email, PW
      + Log: LogID, Name, Account, Withdraw, Deposit, LogDate
    + Relationship type attributes: Record, Manage

## Week 2: Conversion to Relational Model and AWS RDS / MySQL Setup
  + Logical Database

<img width="774" alt="Logical DB" src="https://user-images.githubusercontent.com/83147205/144731343-1f14a941-327a-4855-a94f-a04e7033e8bd.png">

  + Database creation using MySQL on AWS server
    + Create tables based on the schema
      + User table
      + <img width="465" alt="User Table" src="https://user-images.githubusercontent.com/83147205/144731578-cfeb6fa1-b955-4460-909c-2c29ee67eeac.png">
      + Account table
      + <img width="416" alt="Account Table" src="https://user-images.githubusercontent.com/83147205/144731584-fe1e009a-022d-4b14-a7c5-d95530786307.png">
      + Log table
      + <img width="539" alt="Log Table" src="https://user-images.githubusercontent.com/83147205/144731598-33b6db8d-c002-402a-bfe0-35762b78693c.png">

## Week 3: Application Implementation and Testing Using Python
  + Test result video

  + [![Banking DB Test Video](https://user-images.githubusercontent.com/83147205/144731461-30f69951-297b-4f0f-aea2-1bfcdd7d8703.png)](https://youtu.be/NZsOyLqf7Js "Banking DB Test Video")
