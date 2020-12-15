#
# Database configurations
#
db_config = {
    'host': 'localhost',  # Database host
    'user': 'root',  # Database user
    'password': '',  # Database password
    'name': 'geomarketing_automation',  # Database name
    'port': 3306,  # Database port
    'charset': 'utf8',  # Database charset
    'use_unicode': True  # Database apply using unicode
}

#
# Web browser configurations
# TODO:: Still not used
#
web_driver_config = {
    'chrome': {
        'path': '..\drivers\chromedriver.exe'
    }
}
