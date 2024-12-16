import psycopg2
import psycopg2.extras
from settings import DB_CONFIG
from pandas import DataFrame
import repositories.users

def get_user(email) -> DataFrame:

    user = repositories.users.get_user_by_email(email)
    result = DataFrame(user)

    return result

