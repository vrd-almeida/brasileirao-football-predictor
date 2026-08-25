import pandas as pd
from db_config import supabase_client


def get_data_from_database() -> pd.DataFrame:
    """Loads all data from Supabase 'matches' table with pagination."""

    all_data = []
    step = 1000
    offset = 0

    while True:
        response = (
            supabase_client.table("matches")
            .select("*")
            .range(offset, offset + step - 1)
            .execute()
        )

        chunk = response.data
        all_data.extend(chunk)

        if len(chunk) < step:
            break

        offset += step

    if len(all_data) == 0:
        df = pd.DataFrame(
            columns=list(expected_columns), index=pd.Index([], name="id", dtype=str)
        )
    else:
        df = pd.DataFrame(all_data)
        df["Date"] = pd.to_datetime(df["Date"]).dt.date
        df.set_index("id", inplace=True)
        df.sort_index(inplace=True)

    validate_dataframe(df)

    return df


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

    if df.index.name != "id":
        raise ValueError("Index must be name 'id'.")

    return
