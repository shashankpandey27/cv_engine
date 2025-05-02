from supabase import create_client, Client
import streamlit as st

# --- Supabase Config ---
# Access secrets securely
SUPABASE_URL = st.secrets["supabase"]["url"]
SUPABASE_KEY = st.secrets["supabase"]["key"]
SUPABASE_SERVICE_KEY = st.secrets["supabase"]["service_key"]
BUCKET_NAME = st.secrets["supabase"]["bucket"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
