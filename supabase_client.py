from supabase import create_client
import os
 

# --- Supabase Config ---
SUPABASE_URL = "https://bidvgtspaijadkddvbxv.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJpZHZndHNwYWlqYWRrZGR2Ynh2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDU5OTA0MjMsImV4cCI6MjA2MTU2NjQyM30.1C4UCQe_1uSXvv0Y1ALJVzkQvejoy__xpHygc2NmeCY"
BUCKET_NAME = "cv-uploads"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)