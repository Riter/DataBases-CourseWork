import repositories.users
import repositories.registr
import pandas as pd

class Registration():
    def registr(self, user : pd.DataFrame):
        return repositories.registr.registration(user)
        