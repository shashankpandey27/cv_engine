from supabase import create_client, Client
import streamlit as st

# --- Supabase Config ---
# Access secrets securely
SUPABASE_URL = st.secrets["supabase_engine"]["url"]
SUPABASE_KEY = st.secrets["supabase_engine"]["key"]
SUPABASE_SERVICE_KEY = st.secrets["supabase_engine"]["service_key"]
BUCKET_NAME = st.secrets["supabase_engine"]["bucket"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
