import pandas as pd
from repositories.routes import get_schedule_with_drivers

class RoutesService:
    
    def __init__(self) -> None:
        pass

    def get_schedule(self) -> pd.DataFrame:
        """
        Get schedule with drivers information.
        
        Returns:
            pd.DataFrame: DataFrame containing schedule information with driver assignments
        """
        return get_schedule_with_drivers()
