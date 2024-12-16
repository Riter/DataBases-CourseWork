import pandas as pd
from repositories.tickets import get_purchased_tickets, add_purchased_ticket

class TicketsService:

    def __init__(self) -> None:
        self.tickets : pd.DataFrame
        self.tickets = get_purchased_tickets()

    def get_tickets(self) -> pd.DataFrame:
        """
        Get schedule with drivers information.
        
        Returns:
            pd.DataFrame: DataFrame containing schedule information with driver assignments
        """
        return self.tickets

    def add_ticket(self, route_id: int, price: float, purchase_date: str, passenger_name: str) -> None:
        """
        Add a purchased ticket to the database.

        Args:
            route_id (int): The ID of the route.
            price (float): Ticket price.
            purchase_date (str): Date of ticket purchase.
            passenger_name (str): Name of the passenger.

        Raises:
            Exception: If there is an error during the database operation.
        """
        add_purchased_ticket(route_id, price, purchase_date, passenger_name)
        self.tickets = get_purchased_tickets()  # Обновление локального кэша
