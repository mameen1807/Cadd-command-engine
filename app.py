import streamlit as st
import json
import re

# ==========================================
# 1. CORE WEBAPP PAGE SETUP
# ==========================================
st.set_page_config(
    page_title="CADD Core | Reference Engine",
    page_icon="📐",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. SIDEBAR CONTROL & PREFERENCES PANEL
# ==========================================
with st.sidebar:
    st.markdown('<h2 style="color: #38BDF8; font-family: monospace; margin-bottom: 5px;">⚙️ STUDIO CONTROL</h2>', unsafe_allow_html=True)
    st.markdown("---")
    
    ui_theme = st.selectbox(
        "Workspace Visual Theme", 
        ["Dark Matte Studio", "Drafting Light Mode"]
    )
    
    st.markdown("---")
    software_choice = st.radio(
        "Filter CAD Subsystem:",
        ["All Systems", "AutoCAD Engine", "SolidWorks Engine"]
    )

# ==========================================
# 3. DYNAMIC WORKSPACE STYLING INJECTION
# ==========================================
if ui_theme == "Dark Matte Studio":
    st.markdown("""
        <style>
        .stApp {
            background-color: #0D0F12 !important;
            background-image: linear-gradient(rgba(255, 255, 255, 0.012) 1px, transparent 0),
                              linear-gradient(90deg, rgba(255, 255, 255, 0.012) 1px, transparent 0);
            background-size: 32px 32px;
        }
        label, p, span, h1, h2, h3, div { color: #E2E8F0 !important; }
        .stTextInput input, .stSelectbox div { background-color: #151922 !important; border: 1px solid #222936 !important; color: #E2E8F0 !important; }
        </style>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        .stApp {
            background-color: #F8FAFC !important;
            background-image: linear-gradient(rgba(15, 23, 42, 0.03) 1px, transparent 0),
                              linear-gradient(90deg, rgba(15, 23, 42, 0.03) 1px, transparent 0);
            background-size: 24px 24px;
        }
        label, p, span, h1, h2, h3, div { color: #0F172A !important; }
        .stTextInput input, .stSelectbox div { background-color: #FFFFFF !important; border: 1px solid #CBD5E1 !important; color: #0F172A !important; }
        </style>
        """, unsafe_allow_html=True)

# ==========================================
# 4. DATABASE LOADING & CLEAN PARSING
# ==========================================
try:
    with open("commands.json", "r") as f:
        commands_db = json.load(f)
except Exception as e:
    st.error(f"Error loading database: {e}")
    commands_db = []

clean_db = []
for entry in commands_db:
    if isinstance(entry, dict):
        raw_name = entry.get("name", "Unknown Tool")
        software = entry.get("software", "Universal")
        definition = entry.get("use", "No description provided.")
        
        # Regex extraction: If name looks like "LINE (L)", pull out "LINE" and "L"
        match = re.search(r"^(.*?)\s*\((.*?)\)$", raw_name)
        if match:
            clean_name = match.group(1).strip()
            shortcut = match.group(2).strip()
        else:
            clean_name = raw_name.strip()
            shortcut = "Menu/Icon"  # Fallback for tools without explicit shortcut strings
            
        clean_db.append({
            "name": clean_name,
            "software": software,
            "shortcut": shortcut,
            "description": definition
        })

# ==========================================
# 5. CORE SEARCH INTERFACE
# ==========================================
st.markdown('<h1 style="font-family: monospace; text-align: center; margin-bottom: 5px;">📐 CADD CORE ENGINE</h1>', unsafe_allow_html=True)
st.markdown('<p style="color: #64748B; text-align: center; margin-top: 0px;">Type a tool name or character key to begin suggestion query</p>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

search_query = st.text_input("🔍 Search box:", "").strip().lower()

# Build matched lists based on keystroke query
suggestions = []
if search_query:
    for cmd in clean_db:
        if software_choice == "AutoCAD Engine" and cmd["software"] != "AutoCAD":
            continue
        if software_choice == "SolidWorks Engine" and cmd["software"] != "SolidWorks":
            continue
            
        # Match against name or shortcut
        if search_query in cmd["name"].lower() or search_query in cmd["shortcut"].lower():
            label = f"{cmd['name']} [{cmd['shortcut']}] — ({cmd['software']})"
            suggestions.append((label, cmd))

# ==========================================
# 6. DISPLAY SELECTION & RICH CARD VIEW
# ==========================================
if search_query:
    if suggestions:
        options_labels = [item[0] for item in suggestions]
        selected_label = st.selectbox(f"Select from {len(suggestions)} matching features:", options_labels)
        
        # Extract the chosen command row entry
        selected_cmd = next(item[1] for item in suggestions if item[0] == selected_label)
        
        st.markdown("---")
        accent_color = "#38BDF8" if selected_cmd["software"] == "AutoCAD" else "#A855F7"
        
        # Native safe UI structure with absolute mapping to description string values
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(selected_cmd["name"])
                st.caption(f"Subsystem Environment: {selected_cmd['software']}")
            with col2:
                st.metric(label="System Key", value=selected_cmd["shortcut"])
            
            st.markdown("---")
            st.write(selected_cmd["description"])
    else:
        st.info("No matching commands indexed. Adjust entry query tokens.")
else:
    st.markdown("""
    <div style="text-align: center; color: #64748B; padding: 50px 0; font-style: italic; font-family: monospace; font-size: 0.9rem;">
        // Engine ready. Enter terminal character to query database arrays.
    </div>
    """, unsafe_allow_html=True)
