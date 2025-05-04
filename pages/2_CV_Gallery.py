import streamlit as st
from supabase_client import supabase, BUCKET_NAME
from Login import get_authenticator


if st.session_state.get("authentication_status") != True:
    st.warning("Please login to access this page.")
    st.stop()
 
# Set wide layout
st.set_page_config(layout="wide")
with st.spinner("Loading data ..."):
     st.title("🎓 Candidate CV Gallery")
    
#      # Caching the fetch
# @st.cache_data(show_spinner="Fetching candidate data...")
# def fetch_candidates():
#     return supabase.table("cvs_table").select("*").execute().data
 
# --- Caching Supabase data ---
@st.cache_data(ttl=600)
def load_data():
    return supabase.table("cvs_table").select("*").execute().data
 
# --- Refresh control ---
if "refresh" not in st.session_state:
    st.session_state.refresh = False
 
# Refresh button
if st.button("🔄 Refresh Candidates"):
        st.session_state.refresh = True 
data = load_data() if not st.session_state.refresh else supabase.table("cvs_table").select("*").execute().data
st.session_state.refresh = False  # Reset flag
 
# Sidebar filters
with st.sidebar:
    #st.markdown("### 🔎 Filter by Role Score")

    authenticator = get_authenticator()
    authenticator.logout()
    #selected_role_filter = st.selectbox("Role", ["Any"])
    #min_score = st.slider("Minimum Score", 0, 100, 0)
    # Score slider for filtering
    #min_score = st.slider("🔘 Filter by Minimum Score", 0, 100, 0)
    st.markdown(
        """
<marquee behavior="scroll" direction="left" style="color:#0070AD; font-size:13px">
        Disclaimer™: An I&D Middle East tool.
</marquee>
        """,
        unsafe_allow_html=True
    )
 
# Load data once
#data = fetch_candidates()
 
# Extract all unique role types
all_roles = sorted({role for row in data for role in row.get("role_scores", {}).keys() if role})

col1 , col2 = st.columns([1,2])

with col1:
    # Main role filter dropdown
    selected_role = st.selectbox("🎯 Filter by Role Type", ["All"] + all_roles)
with col2: 
    # Search by candidate name
    search_query = st.text_input("🔍 Search Candidate by Name").strip().lower()
 
# Filtering logic
filtered = []
for row in data:
    role_scores = row.get("role_scores", {})
    if not role_scores:
        continue
 
    # Identify main (top scoring) skill
    main_role, main_score = max(role_scores.items(), key=lambda x: x[1])
 
    # Apply role filter only to main role
    if selected_role != "All" and selected_role != main_role:
        continue
    if main_score < min_score:
        continue
 
    # Also apply name search filter
    if selected_role != "All" and selected_role not in role_scores:
        continue
    if search_query and search_query not in row["name"].lower():
        continue
 
    filtered.append(row)
 
# Display warning if no results
if not filtered:
    st.warning("No matching candidates.")
else:
    # Arrange tiles: 5 per row
    rows = [filtered[i:i + 5] for i in range(0, len(filtered), 5)]
 
    for row in rows:
        cols = st.columns(len(row))
        for col, person in zip(cols, row):
            with col:
                html = f"""
<div style="padding: 12px; border-radius: 10px; background-color: #f9f9f9;
                             box-shadow: 0 2px 6px rgba(0,0,0,0.1); min-height: 240px;
                             transition: transform 0.3s; cursor: pointer;"
                             onmouseover="this.style.transform='scale(1.02)'"
                             onmouseout="this.style.transform='scale(1)'">
<strong style="font-size: 14px;">{person['name']}</strong><br><br>
                """
 
                top_roles = sorted(
                    [(r, s) for r, s in person["role_scores"].items()],
                    key=lambda x: x[1], reverse=True
                )[:5]
 
                for role, score in top_roles:
                    color = "#4CAF50" if score >= 80 else "#FFC107" if score >= 60 else "#F44336"
                    html += f"""
<div style="margin-bottom: 4px;">
<small><strong>{role}</strong></small>
<div style="background-color:#e0e0e0; border-radius:6px;">
<div style="width:{score}%; background:{color}; color:white;
                                     padding:3px 0; font-size:11px; text-align:center;">
                                    {score}%
</div>
</div>
</div>
                    """
 
                if person.get("download_url"):
                    html += f"""
<a href="{person['download_url']}" target="_blank"
                           style="text-decoration:none; font-size:13px;">📄 Download CV</a>
                    """
                else:
                    html += "<div style='color:red; font-size:12px;'>⚠️ No download link</div>"
                html += "</div>"
                st.markdown(html, unsafe_allow_html=True)
