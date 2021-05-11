import pymysql


class ConnectDB:
    def __init__(self):
        self.conn = pymysql.connect(host='haulistix-dev.cj3nslaldrrf.us-west-1.rds.amazonaws.com',
                                    user='haulistix',
                                    passwd='PGHQ3AYBnpsKYsbP',
                                    port=53306,
                                    db='haulistix_test',
                                    charset='utf8')

    def connect_select(self, sql):
        cur = self.conn.cursor()
        cur.execute(sql)
        data = cur.fetchone()
        cur.close()
        self.conn.close()
        return data

    def connect_delete(self, sql):
        cur = self.conn.cursor()
        data = cur.execute(sql)
        self.conn.commit()
        cur.close()
        self.conn.close()


if __name__ == "__main__":
    execute = 'DELETE FROM `sys_user` WHERE user_name LIKE "AutoTesttest%"'
    select = 'SELECT user_name FROM `sys_user`'
    ConnectDB().connect_delete(execute)
    # ConnectDB().connect_select(select)
