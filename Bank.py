import mysql.connector
import pandas as pd
from datetime import date
import sys
import getpass
import time

print('''
    
    Welcom to HanYang Bank.
    
    은행 서비스 메뉴얼
    ===========================================================
    사용자 모드
        본인 등록
        계좌 생성
        입출금
        잔고 확인
        비밀번호 변경
        
    관리자 모드
        전체 사용자목록 확인
        전체 계좌목록 확인
        입출금 내역 확인
        사용자 정보 삭제
        계좌 삭제
        관리자 목록
        관리자 추가
        관리자 삭제
    ===========================================================
    ''')


def user_manual():
    print('''
        0. 서비스 종료
        1. 본인 등록
        2. 계좌 생성
        3. 입출금
        4. 잔고 확인
        5. 계좌 비밀번호 변경
        6. 사용자 닉네임 변경
        7. 관리자 모드
        ''')


def admin_manual():
    print('''
        0. 이전 단계
        1. 사용자 정보
        2. 계좌 정보
        3. 입출금 내역
        4. 관리자 목록
        5. 관리자 추가
        6. 사용자 정보 삭제
        7. 계좌 삭제
        8. 관리자 삭제
    ''')


class OpenDB:
    def __init__(self):
        self.host = 'localhost'
        self.DB = 'HBank'
        self.table = None
        self.user_table = 'User'
        self.account = 'Account'
        self.Log = 'Log'
        self.user = 'HanYang'
        self.pw = '1939'
        self.withdraw = False  # 출금이 이루어질 때만 True로 바뀐다.
        self.deposit = False   # 입금이 이루어질 때만 True로 바뀐다.
        self.cursor = object()
        self.DB_connector = object()

    def connect_db(self):
        try:
            self.DB_connector = mysql.connector.connect(host=self.host,
                                                   database=self.DB,
                                                   user=self.user,
                                                   password=self.pw)
            self.cursor = self.DB_connector.cursor()
        except mysql.connector.Error as error:
            print("Failed creating table into HBank DB {}".format(error))
    def close_db(self):
        self.DB_connector.commit()
    # table을 생성하는 함수

    def create_table(self, table_name):
        self.table = table_name
        # mysql모둘을 이용하여 DB에 접속
        try:
            # connect to DB
            self.cursor.execute("DROP TABLE if exists " + self.table)
            # write query to create table
            table_query = []
            print("Input query to table: \n")
            table_query = input("msyql> ")

            self.cursor.execute(table_query)
            print(self.table + " table is created...")
            self.DB_connector.commit()
        except mysql.connector.Error as error:
            print("Failed creating table into HBank DB {}".format(error))

    # 사용자를 DB에 추가하는 함수
    def insert_user_to_db(self):
        try:

            SSN = input("주민번호를 입력하세요: ")
            # 이름 성 순서로 띄어쓰기로 입력하면 이름과 성이 따로 저장된다.
            Name = str(input("이름을 입력하세요: ")).split(' ')
            Lname = Name[0]
            Fname = Name[1]
            Bdate = input("생년월일을 입력하세요: ")
            NickName = input("닉네임을 설정하세요: ")
            sql = "insert into " + self.user_table + \
                " values({},'{}','{}','{}','{}');".format(SSN, Lname, Fname, Bdate, NickName)

            self.cursor.execute(sql)
            self.DB_connector.commit()
            print("사용자 계정이 생성되었습니다.")
        except mysql.connector.Error as error:
            print("Failed inserting user data into User table {}".format(error))

    # 사용자가 계좌를 생성하는 함수
    def create_account_to_db(self):
        try:
            account = input("계좌번호를 입력하세요: ")
            pw = input("비밀번호를 설정하세요: ")
            balance = input("돈을 넣어주세요: ")
            check_count = 1   # 주민번호 오류 횟수
            while check_count <= 3:
                Ussn = int(input("주민번호를 입력하세요: "))
                sql_user_list = "Select * from User"
                self.cursor.execute(sql_user_list)
                user_data = self.cursor.fetchall()
                column = ['SSN', 'Lname', 'Fname', 'Bdate','NickName']
                user_data = pd.DataFrame(user_data, columns=column)
                users = list(user_data['SSN'].values)
                if Ussn in users:
                    sql = "insert into " + self.account + \
                        " values({}, {}, {}, {})".format(
                            account, balance, Ussn, pw)
                    self.cursor.execute(sql)
                    self.DB_connector.commit()
                    print("계좌 생성이 완료되었습니다.")
                    return
                else:

                    print("해당 주민번호는 존재하지 않습니다. 다시 입력하세요. 남은 횟수 {}번".format(
                        3-check_count))
                    check_count += 1
            print("계좌생성에 실패하였습니다.")
            return
        except mysql.connector.Error as error:
            print("Failed creating account into Account table {}".format(error))

    # 입출금이 발생할 때마다 로그테이블에 기록하는 함수
    def write_log(self, cursor, account, cash):
        try:
            sql = "Select Lname, Fname from User, Account Acc where User.SSN = Acc.Ussn and Acc.AccNum = {}".format(
                account)
            cursor.execute(sql)
            name = cursor.fetchall()[0]
            name = name[0] + ' ' + name[1]
            curdate = str(date.today())
            if self.withdraw == True:
                sql = "insert into " + self.Log + "(Account, Name, Withdraw, Deposit, LogDate) values({}, '{}', {}, {},'{}')".format(account,
                                                                                                                                     name, cash, '0', curdate)
            else:
                sql = "insert into " + self.Log + "(Account, Name, Withdraw, Deposit, LogDate) values({}, '{}', {}, {},'{}')".format(account,
                                                                                                                                     name, '0', cash, curdate)
            cursor.execute(sql)
            print("Log data has recorded.")
        except mysql.connector.Error as error:
            print("Failed writing log into Log table {}".format(error))

    # 계좌 입출금을 수행하는 함수
    def update_account(self, table):
        try:
            choose = int(input("입금 1, 출금 2: "))
            account = input("계좌번호를 입력하세요: ")
            login_count, i = 3, 1  # 세 번 이상 입력이 틀릴 경우 접속 제한
            while i <= login_count:
                # 비밀번호를 화면상에서 숨기기위해 getpass 사용
                pw = getpass.getpass('비밀번호를 입력하세요:')
                login_query = "Select PassWord, Balance from Account where AccNum = {}".format(
                    account)
                self.cursor.execute(login_query)
                # select로 데이터를 불러오는 경우 ([...],[,,,])형식이기에 [0]을 취하면 리스트만 남는다.
                login = self.cursor.fetchall()[0]
                password = login[0]  # [password, balance]
                if int(password) == int(pw):
                    balance = login[1]
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
                balance = int(balance) + int(cash)
                # deposit을 True로 해 놓으면 로그 데이터에서 입금 여부를 확인한다.
                self.deposit = True
            else:
                cash = input("출금할 금액을 입력하세요: ")
                balance = (int(balance) - int(cash))
                if balance < 0:
                    print("잔고가 없습니다.")
                    return
                self.withdraw = True
            sql = "update " + table + " Set Balance = {} where AccNum = {}".format(balance, account)
            self.cursor.execute(sql)
            # 로그 테이블을 호출하여 입출금 내용을 자동으로 기록
            self.write_log(self.cursor, account, cash)
            if self.deposit == True:
                print("입금이 완료되었습니다. 현재 잔고는 {}원 입니다.".format(balance))
                self.deposit = False
            else:
                print("출금이 완료되었습니다. 현재 잔고는 {}입니다.".format(balance))
                self.withdraw = False
            self.DB_connector.commit()
            return
        except mysql.connector.Error as error:
            print("Failed updating data into Account table {}".format(error))
            return
    # 현재 잔고를 확인할 수 있는 함수

    def check_balance(self):
        try:
            connector = mysql.connector.connect(host=self.host,
                                                database=self.DB,
                                                user=self.user,
                                                password=self.pw)
            cursor = connector.cursor()

            account = input("계좌번호를 입력하세요: ")
            counter, i = 3, 1
            while i <= counter:
                pw = getpass.getpass('비밀번호를 입력하세요:')
                login_query = "Select PassWord, Balance from Account where AccNum = {}".format(
                    account)
                cursor.execute(login_query)
                login = cursor.fetchall()
                if bool(login):
                    login = login[0]
                else:
                    print("계좌번호가 일치하지 않습니다.")
                    return
                if int(login[0]) == int(pw):
                    print("현재 잔고는 {}원 입니다.".format(login[1]))
                    connector.commit()
                    return
                else:
                    print("비밀번호가 일치하지 않습니다. 남은 시도횟수 {}번".format(counter-i))
                    i += 1

        except mysql.connector.Error as error:
            print("Failed checking balance from MySQL table {}".format(error))
            return

    def password_update(self):
        try:
            account = input("계좌번호를 입력하세요: ")
            counter, i = 3, 1
            while i <= counter:
                pw = getpass.getpass('비밀번호를 입력하세요:')
                login_query = "Select PassWord, Balance from Account where AccNum = {}".format(
                    account)
                self.cursor.execute(login_query)
                login = self.cursor.fetchall()
                if bool(login):
                    login = login[0]
                else:
                    print("계좌번호가 일치하지 않습니다.")
                    return
                if int(login[0]) == int(pw):
                    new_pw = input("새로운 비밀번호 입력: ")
                    pw_update = "update Account set PassWord = {} where AccNum = '{}'".format(new_pw, account)
                    self.cursor.execute(pw_update)
                    self.DB_connector.commit()
                    print("비밀번호 재설정 완료!")
                    return
                else:
                    print("비밀번호가 일치하지 않습니다. 남은 시도횟수 {}번".format(counter-i))
                    i += 1

        except mysql.connector.Error as error:
            print("Failed update password from MySQL table {}".format(error))
            return
        
    def change_nickname(self):
        try:
            ssn = input("주민번호를 입력하세요: ")
            old_nick = input('기존 닉네임을 입력하세요:')
            login_query = "Select NickName from User where SSN = {} and NickName = '{}'".format(
                ssn, old_nick)
            self.cursor.execute(login_query)
            login = self.cursor.fetchall()
            if bool(login):
                login = login[0]
            else:
                print("해당 정보가 존재하지 않습니다.")
                return

            new_nick = input("새로운 닉네임 입력: ")
            pw_update = "update User set NickName = '{}' where SSN = {}".format(
                new_nick, ssn)
            self.cursor.execute(pw_update)
            self.DB_connector.commit()
            print("닉네임 재설정 완료!")
            return

        except mysql.connector.Error as error:
            print("Failed update NickName from MySQL table {}".format(error))
            return
    ################################### Admin Mode ###################################
    # 관리자모드에서 전체 사용자 명단을 보게 하는 함수

    def get_user_list(self, cursor):
        sql_user_cnt = "select count(*) as cnt from User"
        cursor.execute(sql_user_cnt)
        user_count = cursor.fetchall()[0]
        print("\n전체 유저 인원수: ", user_count[0], '명\n')
        sql_user_account = "select Lname, count(*) as numOfaccount from User, Account where SSN = Ussn group by Lname"
        cursor.execute(sql_user_account)
        user_accounts = cursor.fetchall()
        print("각 유저당 보유 계좌 개수:")
        for acc_num in user_accounts:
            print(acc_num[0], ': ', acc_num[1])
        print()
        print("전체 사용자 목록:")
        sql_user_list = "Select * from User"
        cursor.execute(sql_user_list)
        user_data = cursor.fetchall()
        column = ['SSN', 'Lname', 'Fname', 'Bdate','NickName']
        user_data = pd.DataFrame(user_data, columns=column)
        return user_data

    # 데이터베이스에 저장된 전체 계좌 목록을 보여주는 함수
    def get_account_list(self, cursor):
        print()
        account_summary = "select count(AccNum), sum(Balance) from Account"
        cursor.execute(account_summary)
        account_summary = cursor.fetchall()
        summary_column = ['total_cnt', 'total_sum']
        account_summary = pd.DataFrame(account_summary, columns=summary_column)
        print("전체 계좌 개수: ", account_summary['total_cnt'].values[0])
        print("전체 은행 잔고: ", account_summary['total_sum'].values[0])

        balance = 100000
        vip_members = "select Lname, Fname, Balance from User, Account where Ussn = SSN and  Balance >= {} order by Balance".format(
            balance)
        cursor.execute(vip_members)
        vip = cursor.fetchall()
        vip_column = ['Lname', 'Fname', 'Balance']
        vip = pd.DataFrame(vip, columns=vip_column)
        print("\nvip 명단")
        print(vip)
        print()
        print("\n전체 계좌")
        sql_total_list = "Select * from Account"
        cursor.execute(sql_total_list)
        account_data = cursor.fetchall()
        column = ['AccNum', 'Balance', 'Ussn', 'Password']
        account_data = pd.DataFrame(account_data, columns=column)
        return account_data

    # 계좌를 삭제할 수 있는 함수
    def delete_account(self, cursor):
        account = int(input("계좌번호: "))

        accounts = self.get_account_list(cursor)

        accounts = list(accounts['AccNum'].values)
        if account in accounts:
            sql = "Delete from Account Where AccNum = {}".format(account)
            cursor.execute(sql)
            print("계좌 {} 삭제 완료".format(account))
            return
        else:
            print("일치하는 계좌가 존재하지 않습니다.")
            return

    # 사용자를 삭제할 수 있는 함수
    def delete_user(self, cursor):
        ssn = int(input("주민번호 입력: "))
        users = self.get_user_list(cursor)
        users = list(users['SSN'].values)
        if ssn in users:
            # SSN이 Account table의 FK 이므로 Account 계정을 먼저 삭제해줘야 한다.
            sql1 = "Delete from Account where Ussn = {}".format(ssn)
            cursor.execute(sql1)
            sql2 = "Delete from User Where SSN = {}".format(ssn)
            cursor.execute(sql2)
            print("사용자 {} 삭제 완료".format(ssn))
            return
        else:
            print("일치하는 사용자 데이터가 존재하지 않습니다.")
            return

    # 로그 데이터를 보여주는 함수
    def get_log_data(self, cursor):
        print("\nSummary of Log:")
        sql1 = "select Name, sum(withdraw), sum(deposit) from Log group by Name"
        cursor.execute(sql1)
        summary = cursor.fetchall()
        column1 = ['이름', '출금액', '입금액']
        summary = pd.DataFrame(summary, columns=column1)
        print(summary)
        print("\nTotal of Log:")
        sql2 = "Select * from Log"
        cursor.execute(sql2)
        log = cursor.fetchall()
        column = ["LogID", "Account", "Name", "Withdraw", "Deposit", "LogDate"]
        log = pd.DataFrame(log, columns=column)
        return log

    # 관리자를 추가해주는 함수
    def add_admin_member(self, cursor):
        ID = input("아이디 혹은 이메일주소 입력: ")
        PW = input("비밀번호 입력: ")
        sql = "insert into Admin values('{}', {})".format(ID, PW)
        cursor.execute(sql)
        print("관리자 {}님이 추가되었습니다.".format(ID))

    # 관리자 목록을 보여주는 함수
    def print_admin_list(self, cursor):
        sql = "Select * from Admin"
        cursor.execute(sql)
        admin_list = cursor.fetchall()
        column = ["아이디", "비밀번호"]
        admin_list = pd.DataFrame(admin_list, columns=column)
        return admin_list

    # 사용자를 삭제할 수 있는 함수
    def delete_admin(self, cursor):
        ID = input("관리자 아이디: ")
        admin = self.print_admin_list(cursor)

        admins = list(admin['아이디'].values)
        if ID in admins:
            sql = "Delete from Admin Where Admin_ID = '{}'".format(ID)
            cursor.execute(sql)
            print("관리자 {} 삭제 완료".format(ID))
            return
        else:
            print("일치하는 관리자 데이터가 존재하지 않습니다.")
            return


def create_table(DB):
    table_name = input("Insert table name: ")
    DB.create_table(table_name)

# 관리자 계정 관리 함수


def Admin_Mode(DB):
    try:
        connector = mysql.connector.connect(host='localhost',
                                            database='HBank',
                                            user='HanYang',
                                            password='1939')
        cursor = connector.cursor()
        sql = ("Select * from Admin")
        cursor.execute(sql)
        admin = cursor.fetchall()
        column = ['ID', 'Password']
        admin = pd.DataFrame(admin, columns=column)
        admin_id = list(admin['ID'])
        admin_pw = list(admin['Password'])
        counter, i, auth = 3, 1, False
        while i <= counter and auth == False:
            ID = input("관리자 아이디 입력: ")
            PW = getpass.getpass('비밀번호를 입력:')
            for id, pw in zip(admin_id, admin_pw):
                if ID == id and int(PW) == int(pw):
                    print("관리자 확인 완료!")
                    auth = True
                    break
            else:
                print("아이디 혹은 비밀번호 잘못 입력. 남은 시도횟수 {}번".format(counter-i))
                i += 1
        if auth == False:
            print("접근 권한이 없습니다.")
            return
    except mysql.connector.Error as error:
        print("Failed connecting DB {}".format(error))
        return
    while True:
        admin_manual()
        choose = int(input("원하는 관리자서비스 선택: "))
        if choose == 0:
            break
        elif choose == 1:
            users = DB.get_user_list(cursor)
            print(users)
        elif choose == 2:
            accounts = DB.get_account_list(cursor)
            print(accounts)
        elif choose == 3:
            log = DB.get_log_data(cursor)
            print(log)
        elif choose == 4:
            admin_list = DB.print_admin_list(cursor)
            print(admin_list)
        elif choose == 5:
            DB.add_admin_member(cursor)
        elif choose == 6:
            DB.delete_user(cursor)
        elif choose == 7:
            DB.delete_account(cursor)
        elif choose == 8:
            DB.delete_admin(cursor)
        else:
            print("잘못 선택하였습니다.")
    connector.commit()
    return


def main_func(DB):
    DB.connect_db()
    while True:
        user_manual()
        choose = int(input("원하는 서비스를 선택하세요: "))
        if choose == 0:
            DB.close_db()
            print("서비스를 종료합니다.")
            time.sleep(1)
            break
        elif choose == 1:
            DB.insert_user_to_db()  # 사용자 추가
        elif choose == 2:
            DB.create_account_to_db()  # 계좌 생성
        elif choose == 3:
            DB.update_account('Account')  # 입출금
        elif choose == 4:
            DB.check_balance()  # 계좌 잔고
        elif choose == 5:
            DB.password_update()
        elif choose == 6:
            DB.change_nickname()
        elif choose == 7:
            Admin_Mode(DB)  # 관리자 모드
        else:
            print("잘못 선택하였습니다.")


if __name__ == '__main__':

    bank = OpenDB()
    main_func(bank)
