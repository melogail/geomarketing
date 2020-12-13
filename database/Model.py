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

    fillable = []

    # data as dictionary
    data = dict()

    @classmethod
    def all(cls):
        q = f'SELECT * FROM {cls.table}'
        cls.model.execute(q)

        result = []
        fetch =  cls.model.fetchall()
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
