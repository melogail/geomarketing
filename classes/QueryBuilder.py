import re
import datetime
from models.QueriesDone import QueriesDone


class QueryBuilder(object):
    # save_query_log
    # check_query
    def __init__(self):
        self.__query = None

    def save_query_log(self, success):
        """
        Saving query in database

        :param success:
        :return:
        """
        try:
            QueriesDone.insert([[self.__query, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), success]])
        except Exception as e:
            print("Error occurred while saving query! " + str(e))
            exit()

    def check_query(self, query):
        """
        Check whether the query is already present inside the database
        or not

        :param query:
        :return:
        """
        q = QueriesDone.where({'query': query}).first()

        if q is None:
            return False
        else:
            return q

    def set_query(self, query):
        """
        Set query

        :param query:
        :return:
        """
        # TODO:: Create code to check if the query is list or not then filter the query using "re.sub(' +', ' ', query)"
        self.__query = query

    def get_query(self):
        """
        get query

        :return:
        """
        return self.__query
