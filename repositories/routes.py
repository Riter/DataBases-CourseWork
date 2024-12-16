from pandas import DataFrame
import psycopg2
import psycopg2.extras
from settings import DB_CONFIG

def get_schedule_with_drivers() -> DataFrame:
    query = """
        SELECT 
            s.schedule_id,
            r.start_point || ' - ' || r.end_point AS route_name,
            s.departure_time,
            s.arrival_time,
            COALESCE(d.name, 'Водитель не назначен') AS driver_name
        FROM 
            schedules s
        LEFT JOIN 
            routes r ON s.route_id = r.route_id
        LEFT JOIN 
            shifts sh ON s.route_id = sh.route_id
        LEFT JOIN 
            drivers d ON sh.driver_id = d.driver_id
        ORDER BY 
            s.departure_time;
    """

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query)
            return DataFrame(cur.fetchall())
