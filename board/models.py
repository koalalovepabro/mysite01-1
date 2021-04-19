from MySQLdb import connect, OperationalError
from MySQLdb.cursors import DictCursor


def countall():
    try:
        # 연결
        db = conn()

        # cursor 생성
        cursor = db.cursor()

        # SQL 실행
        sql = 'select count(*) from board'
        cursor.execute(sql)

        # 결과 받아오기
        results = cursor.fetchone()

        # 자원 정리
        cursor.close()
        db.close()

        # 결과 반환
        return int(results[0])

    except OperationalError as e:
        print(f'error: {e}')


def findall(startindex, size):
    try:
        # 연결
        db = conn()

        # cursor 생성
        cursor = db.cursor(DictCursor)

        # SQL 실행
        sql = '''
                select a.no,
                       a.title,
                       a.hit,
                       date_format(a.reg_date, '%Y-%m-%d %p %h:%i:%s') as regDate,
                       a.depth,
                       b.name as userName,
                       a.user_no as userNo
                  from board a, user b
                  where a.user_no = b.no
               order by group_no desc, order_no asc
                  limit %s, %s'''
        cursor.execute(sql, (startindex, size))

        # 결과 받아오기
        results = cursor.fetchall()

        # 자원 정리
        cursor.close()
        db.close()

        # 결과 반환
        return results

    except OperationalError as e:
        print(f'error: {e}')


def insert(title, contents, userno):
    try:
        # 연결
        db = conn()

        # cursor 생성
        cursor = db.cursor()

        # SQL 실행
        sql = '''
            insert
              into board
            values (null, %s, %s, 0, now(), (select ifnull( max( group_no), 0) + 1 from board a ), 1, 0, %s)'''

        count = cursor.execute(sql, (title, contents, userno))

        # commit
        db.commit()

        # 자원 정리
        cursor.close()
        db.close()

        # 결과 반환
        return count == 1

    except OperationalError as e:
        print(f'error: {e}')


def update(title, contents, no, userno):
    try:
        # 연결
        db = conn()

        # cursor 생성
        cursor = db.cursor()

        # SQL 실행
        sql = '''
                update board 
                   set title=%s,
                       contents=%s
                 where no=%s
                   and user_no=%s'''
        count = cursor.execute(sql, (title, contents, no, userno))

        # commit
        db.commit()

        # 자원 정리
        cursor.close()
        db.close()

        # 결과 반환
        return count == 1

    except OperationalError as e:
        print(f'error: {e}')


def findbyno(no):
    try:
        # 연결
        db = conn()

        # cursor 생성
        cursor = db.cursor(DictCursor)

        # SQL 실행
        sql = '''
            select	no,
                    title,
                    contents,
                    group_no as groupNo,
                    order_no as orderNo,
                    depth,
                    user_no as userNo
              from  board
             where  no = %s'''
        cursor.execute(sql, (no,))

        # 결과 받아오기
        results = cursor.fetchone()

        # 자원 정리
        cursor.close()
        db.close()

        # 결과 반환
        return results

    except OperationalError as e:
        print(f'error: {e}')


def findby_no_and_userno(no, userno):
    try:
        # 연결
        db = conn()

        # cursor 생성
        cursor = db.cursor(DictCursor)

        # SQL 실행
        sql = '''
            select	no,
                    title,
                    contents,
                    group_no as groupNo,
                    order_no as orderNo,
                    depth,
                    user_no as userNo
              from  board
             where  no = %s
               and  user_no = %s'''
        cursor.execute(sql, (no, userno))

        # 결과 받아오기
        results = cursor.fetchone()

        # 자원 정리
        cursor.close()
        db.close()

        # 결과 반환
        return results

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
