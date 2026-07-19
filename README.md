<div align="center">

# Database Lab 08

### Resolving geographic coordinates into addresses with PostgreSQL and Python

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Functions_and_Triggers-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![Python](https://img.shields.io/badge/Python-Geocoding-3776AB?style=flat-square&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/status-coursework_specification-6B7280?style=flat-square)

</div>

## Objective

Design a small data pipeline that reads eligible coordinates from **airports_data**, resolves them to human-readable addresses with GeoPy, and persists the results in PostgreSQL.

## Target workflow

~~~mermaid
flowchart LR
    A[airports_data] --> B[PostgreSQL function]
    B --> C[Python client]
    C --> D[GeoPy geocoder]
    D --> E[Address table]
~~~

## Requirements

1. Create a PostgreSQL function that returns coordinate pairs within the requested range.
2. Call the function from Python.
3. Resolve coordinates to addresses through GeoPy.
4. Create and populate an **Address** table with:
   - **address_id**
   - **address_text**
   - **address_x**
   - **address_y**
5. Apply a conservative request limit to respect geocoding service policies.

## Engineering considerations

- Parameterize SQL instead of interpolating values.
- Add a unique constraint to avoid duplicate address rows.
- Handle timeouts, missing geocoder results, and retryable errors.
- Keep database credentials in environment variables.
- Cache resolved coordinates to reduce external API calls.

## Repository status

The default branch currently contains the coursework specification. A completed implementation has not yet been committed here.
