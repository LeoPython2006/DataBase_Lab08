CREATE OR REPLACE FUNCTION bookings.get_airport_coordinates_in_range(
    p_min double precision DEFAULT 35,
    p_max double precision DEFAULT 50,
    p_limit integer DEFAULT 100
)
RETURNS TABLE (
    airport_code character(3),
    address_x double precision,
    address_y double precision
)
LANGUAGE sql
AS $$
    SELECT
        a.airport_code,
        x(a.coordinates) AS address_x,
        y(a.coordinates) AS address_y
    FROM bookings.airports_data AS a
    WHERE x(a.coordinates) BETWEEN p_min AND p_max
      AND y(a.coordinates) BETWEEN p_min AND p_max
    ORDER BY a.airport_code
    LIMIT p_limit;
$$;
