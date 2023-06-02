import sqlite3
from random import randint, choice


class Database:
    def __init__(self, filename):
        self.conn = sqlite3.connect(filename)
        self.cur = self.conn.cursor()

        # main table
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users(
           user_id INT PRIMARY KEY,
           username TEXT NULL,
           name_ TEXT NULL,
           sex TEXT NULL,
           city TEXT NULL,
           age INT NULL,
           description TEXT NULL,
           mbti TEXT NULL,
           tags TEXT NULL,
           last_msg_id INT NULL,
           last_id_profile INT NULL,
           photo BLOB NULL,
           start_age INT NULL,
           end_age INT NULL,
           sort_city TEXT NULL,
           time_end_get INT NULL);
        """)

        self.cur.execute("""CREATE TABLE IF NOT EXISTS users_state(
                   user_id INT PRIMARY KEY,
                   state_ TEXT,
                   active TEXT);
                """)

        self.cur.execute("""CREATE TABLE IF NOT EXISTS mbti_pr(
                           mbti1 TEXT,
                           mbti2 TEXT,
                           pr INT);
                        """)

        self.cur.execute("""CREATE TABLE IF NOT EXISTS likes(
                                   id1 INT,
                                   id2 INT);
                                """)

        self.conn.commit()

    def add_user(self, id_user, username):
        sql = """
                INSERT INTO users (user_id, username)
                VALUES (?, ?)
                """

        self.cur.execute(sql, (id_user, username))
        self.conn.commit()

    def add_user_state(self, id_user, s, a):
        sql = """
        INSERT INTO users_state (user_id, state_, active)
        VALUES (?, ?, ?)
        """

        self.cur.execute(sql, (id_user, s, a))
        self.conn.commit()

    def replace_state(self, id_user, s):
        sql = """UPDATE users_state SET state_ = ? WHERE user_id = ?"""

        self.cur.execute(sql, (s, id_user))
        self.conn.commit()

    def replace_time_end_get(self, id_user, time_end_get_):
        sql = """UPDATE users SET time_end_get = ? WHERE user_id = ?"""

        self.cur.execute(sql, (time_end_get_, id_user))
        self.conn.commit()

    def get_time_end_get(self, id_user):
        sql = """SELECT time_end_get from users where user_id = ?"""
        self.cur.execute(sql, (id_user,))
        return self.cur.fetchone()[0]

    def replace_active(self, id_user, active):
        sql = """UPDATE users_state SET active = ? WHERE user_id = ?"""

        self.cur.execute(sql, (active, id_user))
        self.conn.commit()

    def replace_name(self, id_user, name):
        sql = """UPDATE users SET name_ = ? WHERE user_id = ?"""

        self.cur.execute(sql, (name, id_user))
        self.conn.commit()

    def replace_city(self, id_user, city):
        sql = """UPDATE users SET city = ? WHERE user_id = ?"""

        self.cur.execute(sql, (city, id_user))
        self.conn.commit()

    def replace_sort_city(self, id_user, city):
        sql = """UPDATE users SET sort_city = ? WHERE user_id = ?"""

        self.cur.execute(sql, (city, id_user))
        self.conn.commit()

    def replace_sex(self, id_user, sex_):
        sql = """UPDATE users SET sex = ? WHERE user_id = ?"""

        self.cur.execute(sql, (sex_, id_user))
        self.conn.commit()

    def replace_age(self, id_user, age):
        sql = """UPDATE users SET age = ? WHERE user_id = ?"""

        self.cur.execute(sql, (age, id_user))
        self.conn.commit()

    def replace_start_age(self, id_user, age):
        sql = """UPDATE users SET start_age = ? WHERE user_id = ?"""

        self.cur.execute(sql, (age, id_user))
        self.conn.commit()

    def replace_end_age(self, id_user, age):
        sql = """UPDATE users SET end_age = ? WHERE user_id = ?"""

        self.cur.execute(sql, (age, id_user))
        self.conn.commit()

    def replace_description(self, id_user, description):
        sql = """UPDATE users SET description = ? WHERE user_id = ?"""

        self.cur.execute(sql, (description, id_user))
        self.conn.commit()

    def replace_mbti(self, id_user, mbti):
        sql = """UPDATE users SET mbti = ? WHERE user_id = ?"""

        self.cur.execute(sql, (mbti, id_user))
        self.conn.commit()

    def count_row_users(self, id_user):
        sql = """ SELECT COUNT(*) FROM users"""
        self.cur.execute(sql)
        return self.cur.fetchone()[0]

    def get_state(self, id_user):
        sql = """ SELECT state_ from users_state where user_id = ?"""
        self.cur.execute(sql, (id_user,))
        return self.cur.fetchone()[0]

    def get_last_msg_id(self, id_user):
        sql = """ SELECT last_msg_id from users where user_id = ?"""
        self.cur.execute(sql, (id_user,))
        return self.cur.fetchone()[0]

    def get_sex(self, id_user):
        sql = """ SELECT sex from users where user_id = ?"""
        self.cur.execute(sql, (id_user,))
        return self.cur.fetchone()[0]

    def get_s_age(self, id_user):
        sql = """ SELECT start_age from users where user_id = ?"""
        self.cur.execute(sql, (id_user,))
        return self.cur.fetchone()[0]

    def get_end_age(self, id_user):
        sql = """ SELECT end_age from users where user_id = ?"""
        self.cur.execute(sql, (id_user,))
        return self.cur.fetchone()[0]

    def get_sort_city(self, id_user):
        sql = """ SELECT sort_city from users where user_id = ?"""
        self.cur.execute(sql, (id_user,))
        return self.cur.fetchone()[0]

    def replace_last_msg_id(self, id_user, id):
        sql = """UPDATE users SET last_msg_id = ? WHERE user_id = ?"""

        self.cur.execute(sql, (id, id_user))
        self.conn.commit()

    def get_mbti(self, id_user):
        sql = """ SELECT mbti from users where user_id = ?"""
        self.cur.execute(sql, (id_user,))
        return self.cur.fetchone()[0]

    def get_random_profile(self, id_user):
        sql = """ SELECT * from users where user_id != ?"""

        self.cur.execute(sql, (id_user,))
        info = self.cur.fetchall()
        return info[randint(0, len(info) - 1)]

    def get_all_profiles(self, id_user):
        sql = """ SELECT * from users where user_id != ?"""

        self.cur.execute(sql, (id_user,))
        info = self.cur.fetchall()
        return info

    def get_all_id(self, id_user):
        sql = """ SELECT user_id from users where user_id != ?"""

        self.cur.execute(sql, (id_user,))
        info = self.cur.fetchall()
        return info

    def get_my_profile(self, id_user):
        sql = """ SELECT * from users where user_id == ?"""

        self.cur.execute(sql, (id_user,))
        info = self.cur.fetchone()
        return info

    def add_tags_str(self, id_user, tags):
        sql = """UPDATE users SET tags = ? WHERE user_id = ?"""
        self.cur.execute(sql, (tags, id_user))
        self.conn.commit()

    def get_tags(self, id_user):
        sql = """ SELECT tags from users where user_id = ?"""
        self.cur.execute(sql, (id_user,))
        return self.cur.fetchone()[0]

    def get_match_pr(self, mbti1_, mbti2_):
        sql = """ SELECT pr from mbti_pr where mbti1 = ? AND mbti2 = ?"""
        self.cur.execute(sql, (mbti1_, mbti2_))
        pr = self.cur.fetchone()
        return pr

    def add_like(self, id_user1, id_user2):
        sql = """
                INSERT INTO likes (id1, id2)
                VALUES (?, ?)
                """

        self.cur.execute(sql, (id_user1, id_user2))
        self.conn.commit()

    def del_like(self, id_user1, id_user2):
        sql = """DELETE from likes where id1 = ? AND id2 = ?"""
        self.cur.execute(sql, (id_user1, id_user2))
        self.conn.commit()

    def replace_last_id_profile(self, id_user, id):
        sql = """UPDATE users SET last_id_profile = ? WHERE user_id = ?"""

        self.cur.execute(sql, (id, id_user))
        self.conn.commit()

    def get_last_id_profile(self, id_user):
        sql = """SELECT last_id_profile from users where user_id = ?"""
        self.cur.execute(sql, (id_user,))
        return self.cur.fetchone()[0]

    def get_liked_id_by_user(self, user_id):
        sql = """ SELECT id1 from likes where id2 = ?"""
        self.cur.execute(sql, (user_id,))
        data = self.cur.fetchall()
        ids = []
        for p in data:
            ids.append(p[0])
        return ids

    def replace_photo(self, blob_data, id_user):
        sql = """UPDATE users SET photo = ? WHERE user_id = ?"""

        self.cur.execute(sql, (blob_data, id_user))
        self.conn.commit()

    def get_photo(self, id_user):
        sql = """SELECT photo from users where user_id = ?"""
        self.cur.execute(sql, (id_user,))
        return self.cur.fetchone()[0]
