from MySQLdb import connect, OperationalError
from MySQLdb.cursors import DictCursor


def findbyno(no):
    try:
        db = conn()
        cursor = db.cursor(DictCursor)

        sql = 'select no, name, email, gender from user where no=%s'
        cursor.execute(sql, (no,))
        result = cursor.fetchone()

        # 자원 정리
        cursor.close()
        db.close()

        return result

    except OperationalError as e:
        print(f'error: {e}')


def findby_email_and_password(email, password):
    try:
        # 연결
        db = conn()

        # cursor 생성
        cursor = db.cursor(DictCursor)

        # SQL 실행
        sql = 'select no, name from user where email=%s and password = %s'
        cursor.execute(sql, (email, password))

        # 결과 받아오기
        result = cursor.fetchone()

        # 자원 정리
        cursor.close()
        db.close()

        # 결과 반환
        return result

    except OperationalError as e:
        print(f'error: {e}')


def insert(name, email, password, gender):
    try:
        # 연결
        db = conn()

        # cursor 생성
        cursor = db.cursor()

        # SQL 실행
        sql = 'insert into user values(null, %s, %s, %s, %s, now())'
        count = cursor.execute(sql, (name, email, password, gender))

        # commit
        db.commit()

        # 자원 정리
        cursor.close()
        db.close()

        # 결과 반환
        return count == 1

    except OperationalError as e:
        print(f'error: {e}')


def update(name, password):
    try:
        db = conn()
        cursor = db.cursor()

        if password == '':
            sql = '''
                update user
                   set name=%s, gender=%s
                 where no=%s 
            '''
            t = (name, gender, no)
        else:
            sql = '''
                update user
                   set name=%s, password=password(%s), gender=%s
                 where no=%s 
            '''
            t = (name, password, gender, no)

        cursor.execute(sql, t)
        conn.commit()

        # 자원 정리
        cursor.close()
        conn.close()

    except OperationalError as e:
        print(f'error: {e}')


def conn():
    return connect(
        user='webdb',
        password='webdb',
        host='localhost',
        port=3306,
        db='webdb',
        charset='utf8')


