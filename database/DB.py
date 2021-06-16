import pymysql


class DB(object):
    """
    database connection and operations class
    """

    def __init__(self, db_config):
        """
        Instantiate database connection with the database configurations

        :param db_config:
        """
        self.db_connect = pymysql.connect(host=db_config['host'], user=db_config['user'],
                                          password=db_config['password'],
                                          database=db_config['name'], port=db_config['port'],
                                          charset=db_config['charset'], use_unicode=db_config['use_unicode'])
