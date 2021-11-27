import mysql.connector
import pandas as pd
from datetime import date
import re

print('''
    Welcom to HanYang Bank.
    You can do following things.
    ===========================================================
    1. create table.
    2. insert User Info, Account Info
    3. update User Info, Account Info
    4. delete User Info, Account Info, Manager Info.
    5. Select User Info, Account Info, Manager Info, Log Info.
    ===========================================================
    ''')


def user_manual():
    print('''
        0. 완료
        1. 본인 추가
        2. 계좌 생성
        3. 입출금
        4. 잔고 확인
        5. 관리자 모드
        ''')


def admin_manual():
    print('''
        0. 완료
        1. 사용자 목록
        2. 계좌 목록
        3. 계좌 삭제
        4. 입출금 내역
    ''')


class OpenDB:
    def __init__(self):
        self.host = 'db-1.cjfiturksrlr.ap-northeast-2.rds.amazonaws.com'
        self.DB = 'HBank'
        self.table = None
        self.user_table = 'User'
        self.account = 'Account'
        self.Log = 'Log'
        self.user = 'yeschan'
        self.pw = 'yeschan119'
        self.withdraw = False
        self.deposit = False

    def create_table(self, table_name):
        self.table = table_name
        try:
            DB_connector = mysql.connector.connect(host=self.host,
                                                   database=self.DB,
                                                   user=self.user,
                                                   password=self.pw)
            cursor = DB_connector.cursor()
            # connect to DB
            cursor.execute("DROP TABLE if exists " + self.table)
            # write query to create table
            table_query = []
            print("Input query to table: \n")
            table_query = input("msyql> ")
            #cursor.execute("Create table " + self.table + table_query)
            cursor.execute(table_query)
            print(self.table + " table is created...")
        except mysql.connector.Error as error:
            print("Failed creating table into HBank DB {}".format(error))

    def insert_user_to_db(self):
        try:
            sql_connector = mysql.connector.connect(host=self.host,
                                                    database=self.DB,
                                                    user=self.user,
                                                    password=self.pw)
            cursor = sql_connector.cursor()

            '''
            ➣ read data row by row
            ➣ query to insert data to the DB.table
            ➣ insert into DB.table values (%s, %s, %s, %s, %s, %s)
            '''

            SSN = input("주민번호를 입력하세요: ")
            Name = str(input("이름을 입력하세요: ")).split(' ')
            Lname = Name[0]
            Fname = Name[1]
            Bdate = input("생년월일을 입력하세요: ")

            sql = "insert into " + self.user_table + \
                " values({},'{}','{}','{}');".format(SSN, Lname, Fname, Bdate)

            cursor.execute(sql)
            sql_connector.commit()

            print("사용자 계정이 생성되었습니다.")
        except mysql.connector.Error as error:
            print("Failed inserting user data into User table {}".format(error))

    def create_account_to_db(self):
        try:
            sql_connector = mysql.connector.connect(host=self.host,
                                                    database=self.DB,
                                                    user=self.user,
                                                    password=self.pw)
            cursor = sql_connector.cursor()

            account = input("계좌번호를 입력하세요: ")
            pw = input("암호를 설정하세요: ")
            balance = input("돈을 넣어주세요: ")
            Ussn = input("주민번호를 입력하세요: ")
            sql = "insert into " + self.account + \
                " values({}, {}, {}, {})".format(account, balance, Ussn, pw)

            cursor.execute(sql)
            sql_connector.commit()
            print("계좌 생성이 완료되었습니다.")
        except mysql.connector.Error as error:
            print("Failed creating account into Account table {}".format(error))

    def write_log(self, cursor, account, cash):
        try:
            sql = "Select Lname, Fname from User, Account Acc where User.SSN = Acc.Ussn and Acc.AccNum = {}".format(
                account)
            cursor.execute(sql)
            name = cursor.fetchall()[0]
            name = name[0] + ' ' + name[1]
            print(name)
            if self.withdraw == True:
                sql = "insert into " + self.Log + "(Account, Name, Withdraw, Deposit) values({}, '{}', {}, {})".format(account,
                                                                                                                       name, cash, '0')
            else:
                sql = "insert into " + self.Log + "(Account, Name, Withdraw, Deposit) values({}, '{}', {}, {})".format(account,
                                                                                                                       name, '0', cash)
            cursor.execute(sql)
            print("Log data has recorded.")
        except mysql.connector.Error as error:
            print("Failed writing log into Log table {}".format(error))

    def update_data(self, table):
        try:
            sql_connector = mysql.connector.connect(host=self.host,
                                                    database=self.DB,
                                                    user=self.user,
                                                    password=self.pw)
            cursor = sql_connector.cursor()
            choose = int(input("입금 1, 출금 2: "))
            account = input("계좌번호를 입력하세요: ")
            login_count, i = 3, 1
            while i <= login_count:
                pw = input("비밀번호를 입력하세요: ")
                login_query = "Select PassWord, Balance from Account where AccNum = {}".format(
                    account)
                cursor.execute(login_query)
                login = cursor.fetchall()[0]
                password = login[0]
                print(password, pw)
                if int(password) == int(pw):
                    balance = login[1]
                    #balance = re.sub(r'[^0-9]','',balance)
                    break
                elif i == login_count:
                    print("비밀번호 입력횟수를 초과하였습니다.")
                    return
                else:
                    print("비밀번호가 맞지 않습니다.")
                    print("다시 시도하세요. 시도횟수 {}번 남음".format(login_count - i))
                    i += 1

            if choose == 1:
                cash = input("입금할 금액을 입력하세요: ")
                balance = str(int(balance) + int(cash))
                self.deposit = True
            else:
                cash = input("출금할 금액을 입력하세요: ")
                balance = (int(balance) - int(cash))
                if balance < 0:
                    print("잔고가 없습니다.")
                    return
                self.withdraw = True
            sql = "update " + table + \
                " set Balance = {} where AccNum = {}".format(balance, account)
            cursor.execute(sql)
            self.write_log(cursor, account, cash)
            sql_connector.commit()
            self.withdraw = False
            self.deposit = False
            print("입출금이 완료되었습니다.")
            return
        except mysql.connector.Error as error:
            print("Failed updating data into Account table {}".format(error))
            return

    def check_balance(self):
        try:
            connector = mysql.connector.connect(host=self.host,
                                                database=self.DB,
                                                user=self.user,
                                                password=self.pw)
            cursor = connector.cursor()
            print("You're connected to db")

            account = input("계좌번호를 입력하세요: ")
            counter, i = 3, 1
            while i <= counter:
                pw = input("비밀번호를 입력하세요: ")
                login_query = "Select PassWord, Balance from Account where AccNum = {}".format(
                    account)
                cursor.execute(login_query)
                login = cursor.fetchall()[0]
                password = login[0]
                print(password, pw)
                if int(password) == int(pw):
                    print("현재 잔고는 {}원 입니다.".format(login[1]))
                    connector.commit()
                    return
                else:
                    print("비밀번호가 일치하지 않습니다.")
                    i += 1

        except mysql.connector.Error as error:
            print("Failed fetching trained_words from MySQL table {}".format(error))
            return

    ################################### Admin Mode ###################################

    def get_user_list(self, cursor):
        sql = "Select * from User"
        cursor.execute(sql)
        user_data = cursor.fetchall()
        column = ['SSN', 'Lname', 'Fname', 'Bdate']
        user_data = pd.DataFrame(user_data, columns=column)
        print(user_data)

    def get_account_list(self, cursor):
        sql = "Select * from Account"
        cursor.execute(sql)
        account_data = cursor.fetchall()
        column = ['AccNum', 'Balance', 'Ussn', 'Password']
        account_data = pd.DataFrame(account_data, columns=column)
        print(account_data)

    def delete_account(self, cursor):
        account = input("계좌번호: ")
        pw = input("비밀번호: ")
        sql = "Delete from Account Where AccNum = {} and PassWord = {}".format(
            account, pw)
        cursor.execute(sql)
        print("계좌 {} 삭제 완료".format(account))

    def get_log_data(self, cursor):
        sql = "Select * from Log"
        cursor.execute(sql)
        log = cursor.fetchall()
        column = ["LogID", "Account", "Name", "Withdraw", "Deposit", "LogDate"]
        log = pd.DataFrame(log, columns=column)
        print(log)

# create tables


def create_table(DB):
    table_name = input("Insert table name: ")
    DB.create_table(table_name)


def update_table(DB):
    print('''
        1. User
        2. ACCOUNT
        ''')
    while True:
        choose_table = int(input("choose a table:"))
        if choose_table == 1:
            DB.update_data('User')
        elif choose_table == 2:
            DB.update_data('Account')
        else:
            break


def Admin_Mode(DB):
    try:
        connector = mysql.connector.connect(host='db-1.cjfiturksrlr.ap-northeast-2.rds.amazonaws.com',
                                            database='HBank',
                                            user='yeschan',
                                            password='yeschan119')
        cursor = connector.cursor()
        sql = ("Select * from Admin")
        cursor.execute(sql)
        admin = cursor.fetchall()
        column = ['ID', 'Password']
        admin = pd.DataFrame(admin, columns=column)
        print(admin['ID'])
        print(admin['Password'])
        counter, i = 3, 1
        while i <= counter:
            ID = input("관리자 아이디 입력: ")
            PW = input("관리자 암호 입력: ")
            if ID in admin['ID'] and PW in admin['PassWord']:
                print("관리자 확인 완료!")
                break
            else:
                print("아이디 혹은 비밀번호 잘못 입력.")
                i += 1
        if i > counter:
            print("접근 권한이 없습니다.")
            return
    except mysql.connector.Error as error:
        print("Failed connecting DB {}".format(error))
        return
    while True:
        admin_manual()
        choose = int(input("choose one: "))
        if choose == 0:
            break
        elif choose == 1:
            DB.get_user_list(cursor)
        elif choose == 2:
            DB.get_account_list(cursor)
        elif choose == 3:
            DB.delete_account(cursor)
        elif choose == 4:
            DB.get_log_data(cursor)
        else:
            break
    connector.commit()
    return


def main_func(DB):

    while True:
        user_manual()
        choose = int(input("choose one: "))
        if choose == 0:
            break
        elif choose == 1:
            DB.insert_user_to_db()  # 사용자 추가
        elif choose == 2:
            DB.create_account_to_db()  # 계좌 생성
        elif choose == 3:
            DB.update_data('Account')  # 입출금
        elif choose == 4:
            DB.check_balance()  # 계좌 잔고
        elif choose == 5:
            Admin_Mode(DB)  # 관리자 모드
        else:
            break


if __name__ == '__main__':
    bank = OpenDB()
    main_func(bank)
