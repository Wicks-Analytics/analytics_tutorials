"""
Database connection and data loading utilities.
"""

import os
from pathlib import Path
from typing import Dict

import polars as pl
from sqlalchemy import create_engine


def get_sqlite_connection(db_path: str = None) -> str:
    """
    Get SQLite connection string.

    Args:
        db_path: Path to SQLite database file. If None, uses default location.

    Returns:
        SQLAlchemy connection string
    """
    if db_path is None:
        # Default to data/insurance.db in the project root
        project_root = Path(__file__).parent.parent
        db_path = project_root / "data" / "insurance.db"

    return f"sqlite:///{db_path}"


def get_postgres_connection(
    host: str = "localhost",
    port: int = 5432,
    database: str = "insurance",
    user: str = None,
    password: str = None,
) -> str:
    """
    Get PostgreSQL connection string.

    Args:
        host: Database host
        port: Database port
        database: Database name
        user: Username (reads from env if not provided)
        password: Password (reads from env if not provided)

    Returns:
        SQLAlchemy connection string
    """
    user = user or os.getenv("POSTGRES_USER", "postgres")
    password = password or os.getenv("POSTGRES_PASSWORD", "")

    return f"postgresql://{user}:{password}@{host}:{port}/{database}"


def get_snowflake_connection(
    account: str = None,
    user: str = None,
    password: str = None,
    warehouse: str = None,
    database: str = None,
    schema: str = None,
    role: str = None,
) -> Dict[str, str]:
    """
    Get Snowflake connection parameters.

    Args:
        account: Snowflake account identifier
        user: Username
        password: Password
        warehouse: Warehouse name
        database: Database name
        schema: Schema name
        role: Role name

    Returns:
        Dictionary of connection parameters
    """
    return {
        "account": account or os.getenv("SNOWFLAKE_ACCOUNT"),
        "user": user or os.getenv("SNOWFLAKE_USER"),
        "password": password or os.getenv("SNOWFLAKE_PASSWORD"),
        "warehouse": warehouse or os.getenv("SNOWFLAKE_WAREHOUSE"),
        "database": database or os.getenv("SNOWFLAKE_DATABASE"),
        "schema": schema or os.getenv("SNOWFLAKE_SCHEMA", "PUBLIC"),
        "role": role or os.getenv("SNOWFLAKE_ROLE"),
    }


def load_from_sql(
    query: str, connection_string: str, connection_type: str = "sqlalchemy"
) -> pl.DataFrame:
    """
    Load data from SQL database using Polars.

    Args:
        query: SQL query to execute
        connection_string: Database connection string
        connection_type: Type of connection ('sqlalchemy' or 'connectorx')

    Returns:
        Polars DataFrame with query results

    Examples:
        >>> # Load from SQLite
        >>> conn = get_sqlite_connection()
        >>> df = load_from_sql("SELECT * FROM policies", conn)

        >>> # Load from PostgreSQL with ConnectorX (faster)
        >>> conn = get_postgres_connection()
        >>> df = load_from_sql("SELECT * FROM claims", conn, "connectorx")
    """
    if connection_type == "connectorx":
        # Use ConnectorX for faster loading (recommended for large datasets)
        try:
            import connectorx as cx

            df = pl.read_database(query, connection_string)
        except ImportError:
            print("ConnectorX not installed. Falling back to SQLAlchemy.")
            print("Install with: pip install connectorx")
            connection_type = "sqlalchemy"

    if connection_type == "sqlalchemy":
        # Use SQLAlchemy (more compatible but slower)
        from sqlalchemy import create_engine

        engine = create_engine(connection_string)

        with engine.connect() as conn:
            df = pl.read_database(query, conn)

    return df


def load_from_snowflake(query: str, connection_params: Dict[str, str] = None) -> pl.DataFrame:
    """
    Load data from Snowflake using Polars.

    Args:
        query: SQL query to execute
        connection_params: Snowflake connection parameters

    Returns:
        Polars DataFrame with query results

    Example:
        >>> params = get_snowflake_connection()
        >>> df = load_from_snowflake("SELECT * FROM insurance.public.policies", params)
    """
    try:
        import snowflake.connector
    except ImportError:
        raise ImportError(
            "Snowflake connector not installed. "
            "Install with: pip install snowflake-connector-python"
        )

    if connection_params is None:
        connection_params = get_snowflake_connection()

    # Remove None values
    connection_params = {k: v for k, v in connection_params.items() if v is not None}

    # Create connection
    conn = snowflake.connector.connect(**connection_params)

    try:
        # Execute query and fetch results
        cursor = conn.cursor()
        cursor.execute(query)

        # Get column names
        columns = [desc[0] for desc in cursor.description]

        # Fetch all rows
        rows = cursor.fetchall()

        # Create Polars DataFrame
        df = pl.DataFrame(rows, schema=columns, orient="row")

        return df

    finally:
        conn.close()


def create_sqlite_tables(db_path: str = None):
    """
    Create SQLite tables and populate with sample data.

    Args:
        db_path: Path to SQLite database file
    """
    from .data_generators import (
        generate_fraud_predictions,
        generate_insurance_claims,
        generate_insurance_policies,
        generate_premium_predictions,
    )

    connection_string = get_sqlite_connection(db_path)
    engine = create_engine(connection_string)

    print("Generating sample data...")

    # Generate datasets
    policies = generate_insurance_policies(10000)
    claims = generate_insurance_claims(5000, policies)
    fraud_preds = generate_fraud_predictions(5000)
    premium_preds = generate_premium_predictions(5000)

    print("Creating database tables...")

    # Write to database
    with engine.connect() as conn:
        # Policies table
        policies.write_database(table_name="policies", connection=conn, if_table_exists="replace")
        print("✓ Created 'policies' table")

        # Claims table
        claims.write_database(table_name="claims", connection=conn, if_table_exists="replace")
        print("✓ Created 'claims' table")

        # Fraud predictions table
        fraud_preds.write_database(
            table_name="fraud_predictions", connection=conn, if_table_exists="replace"
        )
        print("✓ Created 'fraud_predictions' table")

        # Premium predictions table
        premium_preds.write_database(
            table_name="premium_predictions", connection=conn, if_table_exists="replace"
        )
        print("✓ Created 'premium_predictions' table")

    print(f"\n✅ Database created successfully at: {db_path or 'data/insurance.db'}")


if __name__ == "__main__":
    """Create SQLite database with sample data."""
    create_sqlite_tables()
