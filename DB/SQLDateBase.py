import sqlite3


class SQLighter:

    def __init__(self, db):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(db, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def get_subscriptions(self, status_sub=True):
        """Получаем всех активных подписчиков бота"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM `users` WHERE `status_sub` = ?", (status_sub,)).fetchall()

    def get_user(self):
        """Получаем всех подписчиков бота"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM `users` ").fetchall()

    def subscriber_exists(self, user_id):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `users` WHERE `user_id` = ?', (user_id,)).fetchall()
            return result

    def add_subscriber(self, user_id, username, first_name, last_name, status_sub=True):
        """Добавляем нового подписчика"""
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO users (`user_id`,`status_sub`,`username`,'first_name','last_name') VALUES(?,?,?,?,?)",
                (user_id, status_sub, username, first_name, last_name))

    def update_subscription(self, user_id, status_sub):
        """Обновляем статус подписки пользователя"""
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `status_sub` = ? WHERE `user_id` = ?", (status_sub, user_id))

    def delete_subscription(self, user_id):
        """Удаляем пользователя"""
        with self.connection:
            return self.cursor.execute("DELETE from users where user_id = ?",
                                       (user_id,))

    def referral_code_1(self, id, user_id):
        """Добавляем реферальный код"""
        with self.connection:
            return self.cursor.execute(
                "UPDATE `users` SET 'input_referral_code' = ?  WHERE `user_id` = ?",
                (id, user_id,))

    def referral_code_2(self, id):
        """Увеличиваем число подписчиков"""
        with self.connection:
            return self.cursor.execute(
                "UPDATE `users` SET personal_sub = personal_sub + 1  WHERE `id` = ?",
                (id,))

    def subscriber_exists_id(self, id):
        """Проверяем, есть ли уже юзер в базе по id в базе"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `users` WHERE `id` = ?', (id,)).fetchall()
            return result

    def commit_subscription(self):
        with self.connection:
            return self.connection.commit()

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()
