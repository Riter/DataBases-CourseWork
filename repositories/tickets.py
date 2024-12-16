from pandas import DataFrame
import psycopg2
import psycopg2.extras
from settings import DB_CONFIG

def get_purchased_tickets() -> DataFrame:
    query = """
        SELECT 
            t.ticket_id,
            r.start_point || ' - ' || r.end_point AS route_name,
            t.price,
            t.purchase_date,
            t.passenger_name
        FROM 
            tickets t
        LEFT JOIN 
            routes r ON t.route_id = r.route_id
        ORDER BY 
            t.purchase_date DESC;
    """

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query)
            return DataFrame(cur.fetchall())
        
def route_exists(route_id: int) -> bool:
    """
    Check if a route exists in the database.

    Args:
        route_id (int): The ID of the route to check.

    Returns:
        bool: True if the route exists, False otherwise.
    """
    query = "SELECT 1 FROM routes WHERE route_id = %(route_id)s"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, {"route_id": route_id})
            return cur.fetchone() is not None

def add_purchased_ticket(route_id: int, price: float, purchase_date: str, passenger_name: str) -> None:
    if not route_exists(route_id):
        raise ValueError(f"Маршрут с route_id={route_id} не существует.")

    query = """
        INSERT INTO tickets (route_id, price, purchase_date, passenger_name)
        VALUES (%(route_id)s, %(price)s, %(purchase_date)s, %(passenger_name)s)
    """

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, {
                "route_id": route_id,
                "price": price,
                "purchase_date": purchase_date,
                "passenger_name": passenger_name,
            })
            conn.commit()