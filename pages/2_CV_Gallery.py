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
    
     # Caching the fetch
@st.cache_data(show_spinner="Fetching candidate data...")
def fetch_candidates():
    return supabase.table("cvs_table").select("*").execute().data
 
# Refresh button
if st.button("🔄 Refresh Data"):
    st.rerun()
 
# Sidebar filters
with st.sidebar:
    st.markdown("### 🔎 Filter by Role Score")
    authenticator = get_authenticator()
    authenticator.logout()
    selected_role_filter = st.selectbox("Role", ["Any"])
    min_score = st.slider("Minimum Score", 0, 100, 0)
    st.markdown(
        """
<marquee behavior="scroll" direction="left" style="color:#0070AD; font-size:13px">
        Disclaimer™: An I&D Middle East tool.
</marquee>
        """,
        unsafe_allow_html=True
    )
 
# Load data once
data = fetch_candidates()
 
# Extract roles
all_roles = sorted({role for row in data for role in row.get("role_scores", {}).keys() if role})
selected_role = st.selectbox("🎯 Filter by Role", ["All"] + all_roles)
search_query = st.text_input("🔍 Search Candidate by Name").strip().lower()
 
# Filter
filtered = []
for row in data:
    name_match = search_query in row["name"].lower()
    role_match = selected_role == "All" or selected_role in row["role_scores"]
    sidebar_role = selected_role_filter == "Any" or selected_role_filter in row["role_scores"]
    sidebar_score = True
    if selected_role_filter != "Any":
        sidebar_score = row["role_scores"].get(selected_role_filter, 0) >= min_score
    if name_match and role_match and sidebar_role and sidebar_score:
        filtered.append(row)
 
if not filtered:
    st.warning("No matching candidates.")
else:
    rows = [filtered[i:i + 3] for i in range(0, len(filtered), 3)]
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
                )[:3]
                 
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
    
    
