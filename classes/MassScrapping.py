from classes.Scrap import Scrap
from classes.QueryBuilder import QueryBuilder


class MassScrapping(Scrap):
    def __init__(self, queries_list):
        super().__init__()
        self.qb = QueryBuilder()
        # queries must be of list type
        if type(queries_list) != list:
            print('Error Mass Scrapping queries must be of type list,', type(queries_list) , 'is given!')
            exit()
        # set query
        self.qb.set_query(queries_list)
        self.queries = self.qb.get_query()

    def start(self, ask_for_rerun=False):
        for query in self.queries:
            # query check
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


test = MassScrapping(['ATM in قسم ثان القاهرة الجديدة, محافظة القاهرة'])
test.start(True)
