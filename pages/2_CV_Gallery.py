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
@st.cache_data(ttl=600)
def load_cv_data():
    return supabase.table("cvs_table").select("*").execute().data

data = load_cv_data()

col1, col2 = st.columns([1, 2])
 
# with col1:
#     # Extract unique roles
#     all_roles = sorted({role for row in data for role in row["role_scores"]})
#     selected_role = st.selectbox("🎯 Filter by Display Role", ["All"] + all_roles)
 
with col2:
    # Search input
    search_query = st.text_input("🔍 Search Candidate by Name").strip().lower()
 
# Sidebar filter for score
with st.sidebar:
    st.markdown("### 🔎 Filter by Role Score")
    all_roles = sorted({role for row in data for role in row["role_scores"]})
    selected_role_filter = st.selectbox("🎯 Filter by Display Role", ["Any"] + all_roles)
    min_score = st.slider("Minimum Score", 0, 100, 0)

    if st.button("🔄 Refresh CV Data"):
        load_cv_data.clear()  # Clear the cache
        st.rerun()  # Force rerun to reload fresh data
   
    
    authenticator = get_authenticator()
    authenticator.logout()
 
    st.markdown(
        """
<marquee behavior="scroll" direction="left" style="color:#0070AD; font-size:13px">
        Disclaimer™: An I&D Middle East tool.
</marquee>
        """,
        unsafe_allow_html=True
    )
 
# Apply filters
filtered = []
for row in data:
    # Filter by selected display role (main page)
    if selected_role_filter != "Any" and selected_role_filter not in row["role_scores"]:
        continue
    # Filter by search query
    if search_query and search_query not in row["name"].lower():
        continue
    # Filter by role score from sidebar
    if selected_role_filter != "Any":
        role_score = row["role_scores"].get(selected_role_filter, 0)
        if role_score < min_score:
            continue
    filtered.append(row)
 
# Display filtered candidates
if not filtered:
    st.warning("No matching candidates.")
else:
    rows = [filtered[i:i + 5] for i in range(0, len(filtered), 5)]
    for row in rows:
        cols = st.columns(len(row))
        for col, person in zip(cols, row):
            # Start tile
            tile_html = f"""
<div style="padding: 16px; border-radius: 12px; background-color: #f9f9f9;
            box-shadow: 0 1px 6px rgba(0,0,0,0.1); min-height: 250px;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            transition: all 0.3s ease;"
     onmouseover="this.style.boxShadow='0 4px 12px rgba(0,0,0,0.2)'; this.style.transform='scale(1.02)';"
     onmouseout="this.style.boxShadow='0 1px 6px rgba(0,0,0,0.1)'; this.style.transform='scale(1)';">
<strong style="font-size: 16px; margin-bottom: 12px;">{person['name']}</strong>
"""
 
        # Top 2-3 role scores
        top_roles = sorted(
            [(r, s) for r, s in person["role_scores"].items() if r.lower() != "name"],
            key=lambda x: x[1], reverse=True
        )[:5] # top N roles 
         
        for role, score in top_roles:
            color = "#4CAF50" if score >= 80 else "#FFC107" if score >= 60 else "#F44336"
            tile_html += f"""
        <div style="width: 100%; max-width: 220px; margin-bottom: 10px;">
        <small><strong>{role}</strong></small>
        <div style="background-color:#e0e0e0; border-radius:8px; overflow: hidden;">
        <div style="width:{score}%; background:{color}; color:white;
                                padding:5px 0; font-size:12px; text-align:center;">
                        {score}%
        </div>
        </div>
        </div>
            """
         
        # Download link
        if person.get("download_url"):
            tile_html += f"""
        <a href="{person['download_url']}" target="_blank"
               style="margin-top: 10px; font-size:13px; text-decoration: none; color: #3366cc;">
               📄 Download CV
        </a>
            """
        else:
            tile_html += "<p style='color:red; font-size:12px;'>No CV link</p>"
         
        tile_html += "</div>"
         
        col.markdown(tile_html, unsafe_allow_html=True)
