from database.DB import DB
from config import db_config
from unicodedata import normalize


class Model(object):
    """
    Base Model class where every table will be a class to inherit from Model class
    """
    conn = DB(db_config).db_connect
    model = conn.cursor()

    # Table name
    table = ''

    # Fillable data in table
    fillable = []

    # Query
    query = ''

    # data as dictionary
    data = dict()

    @classmethod
    def all(cls):
        q = f'SELECT * FROM {cls.table}'
        cls.model.execute(q)

        result = []
        fetch = cls.model.fetchall()
        for record in fetch:
            rec_result = []
            for rec in record:
                if type(rec) == str:
                    rec = rec.replace(u'\xa0', ' ')
                rec_result.append(rec)
            result.append(rec_result)

        return result

    @classmethod
    def insert(cls, values):
        """
        Inserting data inside table

        :param values:
        :return:
        """
        fields = ''
        delimiter = ''
        for field in cls.fillable:
            if len(cls.fillable) == 1 or field == cls.fillable[-1]:
                fields += f'{field}'
                if type(field) == str:
                    delimiter += '%s'
                elif type(field) == int:
                    delimiter += '%d'

            else:
                fields += f'{field},'
                if type(field) == str:
                    delimiter += '%s,'
                elif type(field) == int:
                    delimiter += '%d,'

        cls.model.executemany(f'INSERT INTO {cls.table} ({fields}) values ({delimiter})', values)
        cls.conn.commit()
        try:
            print('Data successfully stored!\n')
            return cls.last_row_insert_id(cls)

        except:
            print('Data storing failed!')

    def last_row_insert_id(self):
        """
        Return last row id

        :return:
        """
        return self.model.lastrowid

    @classmethod
    def get(cls):
        """
        Return collection of results from query

        :return:
        """
        query = f'SELECT * FROM {cls.table} {cls.query}'
        cls.model.execute(query)
        return cls.model.fetchall()

    @classmethod
    def first(cls):
        """
        Return the first result of the query.

        :return:
        """
        query = f'SELECT * FROM {cls.table} {cls.query}'
        cls.model.execute(query)
        return cls.model.fetchone()

    @classmethod
    def where(cls, where):
        """
        Add where clause to query, use with get

        :param where:
        :return:
        """
        # Initialize the where clue
        query = 'WHERE '

        try:
            # Loop through where clause dictionary
            if type(where) == dict:
                for index, (key, value) in enumerate(where.items()):
                    if (index + 1) != len(where):
                        query += f'{key} = "{value}" AND '
                    else:
                        query += f'{key} = "{value}"'

                cls.query = query
                return cls
        except Exception as e:
            print("Error! make sure your where clause are in dictionary format", str(e))
            return False


    @classmethod
    def close_connection(cls):
        print('connection closed:', cls.conn)
        cls.conn.close()