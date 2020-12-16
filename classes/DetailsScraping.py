from classes.Scrap import Scrap
from classes.QueryBuilder import QueryBuilder


class DetailsScraping(Scrap):
    def __init__(self, query):
        super().__init__()
        self.db = QueryBuilder()
        # query must be type of string
        if type(query) != str:
            print('Error Details Scraping query must be of type string,', type(query), 'given!')
            exit()
        # set query
        self.db.set_query(query)
        self.query = self.db.get_query()

    def start(self, display=False):

        self.run(self.query)
