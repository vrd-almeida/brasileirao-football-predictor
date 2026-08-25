import os
from supabase import create_client, Client


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if SUPABASE_URL is None or SUPABASE_KEY is None:
    raise ValueError(
        "❌ SUPABASE_URL and SUPABASE_KEY must be defined as environment variables."
    )

try:
    supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    response = supabase_client.table("matches").select("*").limit(1).execute()

    print("✅ Connected to Supabase")

except Exception as e:
    print("❌ Connection failed:")
    print(e)
