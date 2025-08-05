import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError


# Retrieve required environment variables or raise an error if missing
user = os.getenv("USER")
if user is None:
    raise ValueError("❌ Environment variable 'USER' must be defined.")

password = os.getenv("PASSWORD")
if password is None:
    raise ValueError("❌ Environment variable 'PASSWORD' must be defined.")

host = os.getenv("HOST")
if host is None:
    raise ValueError("❌ Environment variable 'HOST' must be defined.")

port = os.getenv("PORT")
if port is None:
    raise ValueError("❌ Environment variable 'PORT' must be defined.")

database = os.getenv("DB_NAME")
if database is None:
    raise ValueError("❌ Environment variable 'DB_NAME' must be defined.")

# Try to connect
try:
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}")
    # Test the connection
    with engine.connect() as connection:
        print("✅ Successfully connected to the database.")
except SQLAlchemyError as e:
    print("❌ Failed to connect to the database.")
    print("Error:", e)
    print("\n🔧 Make sure:")
    print("- PostgreSQL is installed and running")
    print("- The credentials are correct")
    print("- Required Python packages are installed: `sqlalchemy`, `psycopg2-binary`")


expected_columns = {
    "Season",
    "Date",
    "Home",
    "Away",
    "HG",
    "AG",
    "Res",
    "PSCH",
    "PSCD",
    "PSCA",
    "MaxCH",
    "MaxCD",
    "MaxCA",
    "AvgCH",
    "AvgCD",
    "AvgCA",
}


def validate_dataframe(df: pd.DataFrame) -> None:
    actual_columns = set(df.columns)

    # Check if all expected columns are present
    missing_columns = expected_columns - actual_columns
    extra_columns = actual_columns - expected_columns

    if missing_columns:
        raise ValueError("Missing columns:", missing_columns)

    if extra_columns:
        raise ValueError("Unexpected columns:", extra_columns)

    if not missing_columns and not extra_columns:
        print("✅ DataFrame has exactly the expected columns.")

    return


def get_data_from_database() -> pd.DataFrame:

    # Example: load entire table into a DataFrame
    df = pd.read_sql("SELECT * FROM matches", con=engine, index_col="id")

    validate_dataframe(df)

    return df
