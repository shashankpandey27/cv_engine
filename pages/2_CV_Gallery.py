import streamlit as st
from supabase_client import supabase
from Login import get_authenticator


if st.session_state.get("authentication_status") != True:
    st.warning("Please login to access this page.")
    st.stop()
 
# Set wide layout
st.set_page_config(layout="wide")
st.title("🎓 Candidate CV Gallery")



# --- Role Progress HTML Generator ---
def get_role_progress_html(role_matches):
    html = ""
    for match in role_matches:
        role = match["role"]
        score = match["score"]
        color = "#4CAF50" if score >= 80 else "#FFC107" if score >= 60 else "#F44336"
        html += f"""
<div style="margin-bottom: 8px; text-align: left;">
<strong style="font-size: 13px;">{role}</strong>
<div style="background-color: #e0e0e0; border-radius: 8px; overflow: hidden;">
<div style="width: {score}%; background-color: {color}; padding: 4px 0;
                                text-align: center; color: white; font-size: 12px;">
                        {score}%
</div>
</div>
</div>
        """
    return html

# Fetch data
data = supabase.table("cvs_table").select("*").execute().data
 
# Extract unique roles
all_roles = sorted({role for row in data for role in row["role_scores"]})
selected_role = st.selectbox("🎯 Filter by Role", ["All"] + all_roles)

# --- Sidebar filters ---
search_query = st.text_input("🔍 Search Candidate by Name").strip().lower()
 

# Role score filter UI
with st.sidebar:
    st.markdown("### 🔎 Filter by Role Score")
    selected_role_filter = st.selectbox("Role", ["Any"] + all_roles)
    min_score = st.slider("Minimum Score", 0, 100, 0)

    authenticator = get_authenticator()
    authenticator.logout() # logout button in sidebar 

    st.markdown(
    """
    <marquee behavior="scroll" direction="left" style="color:#0070AD; font-size:13px">
    Disclaimer™: An I&D Middle East tool.
    </marquee>
    """,
    unsafe_allow_html=True)

# Filter candidates
filtered = []
for row in data:
    if selected_role == "All" or selected_role in row["role_scores"]:
        filtered.append(row)
 
if not filtered:
    st.warning("No matching candidates.")
else:
    rows = [filtered[i:i + 5] for i in range(0, len(filtered), 5)]
    for row in rows:
        cols = st.columns(len(row))
        for col, person in zip(cols, row):
            col.markdown(f"""
<div style="padding: 10px; border-radius: 8px; background-color: #f9f9f9; 
                            box-shadow: 0 1px 4px rgba(0,0,0,0.1); min-height: 200px;">
<strong>{person['name']}</strong><br><br>
            """, unsafe_allow_html=True)
            for role, score in person["role_scores"].items():
                color = "#4CAF50" if score >= 80 else "#FFC107" if score >= 60 else "#F44336"
                col.markdown(f"""
<div style="margin-bottom: 4px;">
<small><strong>{role}</strong></small>
<div style="background-color:#e0e0e0; border-radius:6px;">
<div style="width:{score}%; background:{color}; color:white; padding:3px 0; font-size:11px; text-align:center;">
                                {score}%
</div>
</div>
</div>
                """, unsafe_allow_html=True)
            col.markdown(f"""<br><a href="{person['download_url']}" target="_blank">📄 Download CV</a></div>""", unsafe_allow_html=True)
            st.markdown("### &nbsp;")  # Space between rows
