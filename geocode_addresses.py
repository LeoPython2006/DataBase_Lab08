import os
from time import sleep

from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim
import psycopg


def get_connection():
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        return psycopg.connect(db_url)

    return psycopg.connect(
        dbname=os.getenv("PGDATABASE", "demo-mediuk"),
        user=os.getenv("PGUSER", "postgres"),
        password=os.getenv("PGPASSWORD", "postgres"),
        host=os.getenv("PGHOST", "localhost"),
        port=os.getenv("PGPORT", "5432"),
    )


def ensure_address_table(cur):
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS bookings."Address" (
            address_id bigserial PRIMARY KEY,
            address_text text NOT NULL,
            address_x double precision NOT NULL,
            address_y double precision NOT NULL,
            UNIQUE (address_x, address_y)
        )
        """
    )


def fetch_coordinates(cur, min_v, max_v, row_limit):
    cur.execute(
        "SELECT airport_code, address_x, address_y FROM bookings.get_airport_coordinates_in_range(%s, %s, %s)",
        (min_v, max_v, row_limit),
    )
    return cur.fetchall()


def reverse_geocode(locator, x_coord, y_coord):
    location = locator(f"{y_coord}, {x_coord}")
    if location and location.address:
        return location.address
    return f"Unknown address ({x_coord}, {y_coord})"


def insert_address(cur, address_text, x_coord, y_coord):
    cur.execute(
        """
        INSERT INTO bookings."Address" (address_text, address_x, address_y)
        VALUES (%s, %s, %s)
        ON CONFLICT (address_x, address_y)
        DO UPDATE SET address_text = EXCLUDED.address_text
        """,
        (address_text, x_coord, y_coord),
    )


def main():
    min_v = float(os.getenv("COORD_MIN", "35"))
    max_v = float(os.getenv("COORD_MAX", "50"))
    row_limit = int(os.getenv("ROW_LIMIT", "50"))
    pause_seconds = float(os.getenv("GEOCODE_SLEEP", "1.1"))

    geolocator = Nominatim(user_agent=os.getenv("GEOPY_USER_AGENT", "lab08-address-resolver"))
    reverse = RateLimiter(geolocator.reverse, min_delay_seconds=pause_seconds)

    with get_connection() as conn:
        with conn.cursor() as cur:
            ensure_address_table(cur)
            rows = fetch_coordinates(cur, min_v, max_v, row_limit)
            for _, x_coord, y_coord in rows:
                address_text = reverse_geocode(reverse, x_coord, y_coord)
                insert_address(cur, address_text, x_coord, y_coord)
                sleep(0.05)
        conn.commit()


if __name__ == "__main__":
    main()
