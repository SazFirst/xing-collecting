import cx_Oracle
import os

os.environ['DPI_DEBUG_LEVEL'] = '32'

class DB:
    def __init__(self, user_id, password):
        connection = cx_Oracle.connect(user_id, password)
        self.__cursor = connection.cursor()


if __name__ == '__main__':
    connection = cx_Oracle.connect('system','manager','HAN', mode = cx_Oracle.SYSDBA)
    cursor = connection.cursor()

    cursor.execute("select sysdate from dual")

    for name in cursor:
        print("테스트 이름 리스트 : ", name)
