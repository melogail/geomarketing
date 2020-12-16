from classes.MassScraping import MassScraping
from classes.DetailsScraping import DetailsScraping


def mass_scrapping(query_list, ask_for_rerun=False):
    """
    Generate mass scrapping for Google Maps landmarks, and save
    data to the database.
    This function must accept a list of queries to run.

    :return:
    """
    scrap = MassScraping(query_list)
    scrap.start(ask_for_rerun)


def scrap_for_single_query():
    """
    Prompt the user for scrapping single query using query choices
    :return:
    """
    pass


def scrap_custom_query(query):
    """
    Promp the user to type in custom query to scrap data
    :param query:
    :return:
    """
    pass

def details_scraping(query):
    """
    Scrap single CID for details
    :param query:
    :return:
    """
    scrap = DetailsScraping(query)
    scrap.start()