from classes.Scrap import Scrap
from classes.QueryBuilder import QueryBuilder


class MassScraping(Scrap):
    def __init__(self, queries_list):
        super().__init__()
        self.qb = QueryBuilder()
        # queries must be of list type
        if type(queries_list) != list and type(queries_list) != dict:
            print('Error Mass Scraping queries must be of type list, or dictionary', type(queries_list) , 'is given!')
            exit()
        # set query
        self.qb.set_query(queries_list)
        self.queries = self.qb.get_query()

    def start(self, ask_for_rerun=False):
        """
        Start running mass scraping, you can prompt every saved
        query and ask for rerun the query again by setting the
        "ask_for_rerun" option to True <default: False>

        :param ask_for_rerun:
        :return:
        """
        for query in self.queries:
            # query check
            if type(query) == dict:
                result = self.qb.check_query(query['query'])
            else:
                result = self.qb.check_query(query)

            if result:
                print(f'"{query}" query already performed on: {result[2]}')

                # Prompt the user for rerun the query
                if ask_for_rerun:
                    rerun = input("Do you like to perform this query again?[Yes|No] ").lower()

                    while rerun != 'yes' and rerun != 'no':
                        rerun = input("Do you like to perform this query again?[Yes|No] ").lower()

                    if rerun == 'yes':
                        self.run(query)
                    else:
                        continue
            else:
                self.run(query)