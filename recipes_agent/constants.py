import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
IMAGES_URL = f"{SUPABASE_URL}/storage/v1/object/public/images"
