import sqlite3


class Database:

    __accounts_table = """
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            access INTEGER DEFAULT 0 NOT NULL
        );
    """

    __approvals_table = """
        CREATE TABLE IF NOT EXISTS approvals (
            message_id INTEGER NOT NULL PRIMARY KEY,
            approver_id INTEGER NOT NULL,
            requester_id INTEGER NOT NULL
        );
    """

    def __init__(self):
        # Establishing connection
        self.con = sqlite3.connect('storage/database.db')
        self.cur = self.con.cursor()

        # Creating tables
        self.cur.execute(self.__accounts_table)
        self.cur.execute(self.__approvals_table)

        # Applying changes
        self.con.commit()

        # Closing cursor
        self.cur.close()

    def manager(self):
        return DatabaseManager(self.con)


class DatabaseManager:
    def __init__(self, connection: sqlite3.Connection):
        self.con = connection
        self.cur = self.con.cursor()
        self.cur.row_factory = sqlite3.Row

    def set_user_access(self, user_id: int, access: int):
        self.cur.execute(
            """
            UPDATE  accounts
            SET     access = %s
            WHERE   id = %s
            """ % (access, user_id)
        )
        self.con.commit()

    def get_user(self, user_id) -> dict:
        self.cur.execute(
            """
            SELECT *
            FROM accounts
            WHERE id = %s
            """ % (user_id,)
        )
        user = self.cur.fetchone()

        if user:
            return dict(user)

    def new_user(self, user_id, name):
        self.cur.execute(
            """
            INSERT INTO accounts (id, name)
            VALUES (%s, '%s')
            """ % (user_id, name)
        )
        self.con.commit()

    def filter_users(self, access):
        self.cur.execute(
            """
            SELECT id
            FROM accounts
            WHERE access > %s
            """ % access
        )
        return self.cur.fetchall()

    def request_approval(self, message_id, approver_id, requester_id):
        self.cur.execute(
            """
            INSERT INTO approvals
            VALUES (%s, %s, %s)
            """ % (message_id, approver_id, requester_id)
        )
        self.con.commit()

    def response_approval(self, is_approved: bool, message_id):

        approval = self.get_approval(message_id)

        if not approval:
            raise KeyError('Approval with that ID not found.')
        # Finding the id of requester
        requester_id = approval.get('requester_id')

        # Changing the access of the requester accordingly
        self.set_user_access(requester_id, 1 if is_approved else -1)

        # Deleting approvals made by the same requester
        self.cur.execute(
            """
            DELETE FROM approvals
            WHERE requester_id = %s
            """ % requester_id
        )
        self.con.commit()

    def get_approval(self, message_id):

        self.cur.execute(
            """
            SELECT *
            FROM approvals
            WHERE message_id = %s
            """ % message_id
        )

        data = self.cur.fetchone()

        return dict(data) if data else None

