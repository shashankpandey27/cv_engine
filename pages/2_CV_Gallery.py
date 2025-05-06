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
    st.markdown(
        """
<marquee behavior="scroll" direction="left" style="color:#0070AD; font-size:13px">
        Disclaimer™: An I&D Middle East tool.
</marquee>
        """,
        unsafe_allow_html=True
    )
 
 
# Extract all unique role types
all_roles = sorted({role for row in data for role in row.get("role_scores", {}).keys() if role})

col1 , col2 , col3, col4 = st.columns([1,2,2,2])

with col1:
    # Main role filter dropdown
    selected_role = st.selectbox("🎯 Filter by Role Type", ["All"] + all_roles)
with col2: 
    # Search by candidate name
    search_query = st.text_input("🔍 Search Candidate by Name").strip().lower()
with col3: 
    # Search by technical skill
    skill_query = st.text_input("🛠️ Search by Technical Skill").strip().lower()
with col4: 
    # Search by Language
    lang_query = st.text_input("🗣️ Search by Language").strip().lower()
 
# Filtering logic

filtered = []
for row in data:
    role_scores = row.get("role_scores", {})
    if not role_scores:
        continue
 
    # Get top 3 roles by score
    top_roles = sorted(role_scores.items(), key=lambda x: x[1], reverse=True)[:3]
    top_role_names = [role for role, _ in top_roles]
 
    # Filter by selected role (must be in top 3)
    if selected_role != "All" and selected_role not in top_role_names:
        continue
 
    # Filter by search query on name
    if search_query and search_query not in row["name"].lower():
        continue

    # Filter by skill search
    skills = row.get("technical_skills", [])
    skill_text = ", ".join(skills).lower() if isinstance(skills, list) else str(skills).lower()
    if skill_query and skill_query not in skill_text:
        continue

    # Filter by Language search
    languages = row.get("languages", [])
    lang_text = ", ".join(languages).lower() if isinstance(languages, list) else str(languages).lower()
    if lang_query and lang_query not in lang_text:
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
                candidate_id = person.get("file_name", person["name"])  # Ensure unique key
                tile_key = f"flip_{candidate_id}"
                if tile_key not in st.session_state:
                    st.session_state[tile_key] = False
         
                def flip_card(key=tile_key):
                    st.session_state[key] = not st.session_state[key]
         
                # Flip button (small)
                if st.button("🔄", key=f"{tile_key}_btn", help="Flip card", on_click=flip_card):
                    pass
         
                # FRONT SIDE: Role Scores
                if not st.session_state[tile_key]:
                    html = f"""
        <div style="padding: 12px; border-radius: 10px; background-color: #f9f9f9;
                        box-shadow: 0 2px 6px rgba(0,0,0,0.1); min-height: 240px;
                        transition: transform 0.3s;">
        <strong style="font-size: 14px;">{person['name']}</strong><br><br>
                    """
                    top_roles = sorted(
                        [(r, s) for r, s in person["role_scores"].items()],
                        key=lambda x: x[1], reverse=True
                    )[:5]
                    for role, score in top_roles:
                        color = "#ADC178" if score >= 80 else "#FCBF49" if score >= 60 else "#BC4749"
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
         
                # BACK SIDE: Technical Skills
                else:
                    skills = person.get("technical_skills", [])
                    skill_str = ", ".join(skills) if isinstance(skills, list) else str(skills)
                    experience = person.get("experience","N/A")
                    gender = person.get("gender","Unknown").strip().capitalize()
                    bg_color = "#e6f0ff" if gender == "Male" else "#ffe6f0" if gender == "Female" else "#f9f9f9"
                    languages = person.get("languages","Unknown")
                    langs_str = ", ".join(languages) if isinstance(languages, list) else str(languages)
                    show_arabic_flag = any("arabic" in lang.lower() for lang in languages)

                    flag_html = """
                    <div style="position: absolute; top: 10px; right: 10px; font-size: 20px;">🇸🇦</div>
                    """ if show_arabic_flag else ""
                     
                    tile_html = f"""
                    <div style="position: relative; padding: 12px; border-radius: 10px; background-color: {bg_color};
                        box-shadow: 0 2px 6px rgba(0,0,0,0.1); min-height: 240px;
                        transition: transform 0.3s;">
                        {flag_html}
                    <strong style="font-size: 14px;">{person['name']}</strong><br><br>
                    <strong>🧑Gender: </strong> {gender}<br>
                    <strong>🛠Technical Skills: </strong><br>
                    <div style="font-size: 13px; margin-top: 5px;">{skill_str}</div><br>
                    <strong>🌍Languages: </strong> {langs_str}<br>
                    <strong>💼Experience: </strong> {experience} years
                    </div>
                    """
                     
                    st.markdown(tile_html, unsafe_allow_html=True)
