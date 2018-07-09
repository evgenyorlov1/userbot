import easy_env
from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv())

API_ID = easy_env.get_int('API_ID')
API_HASH = easy_env.get('API_HASH')
USER_PHONE = easy_env.get('USER_PHONE')
USER_PASSWORD = easy_env.get('USER_PASSWORD')
NOU_LIST = easy_env.get_list('NOU_LIST', ['baka'], separator='|')