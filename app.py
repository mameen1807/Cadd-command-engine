import streamlit as st
import json
import re

# ==========================================
# 1. CORE WEBAPP PAGE SETUP & BRUTE SHORTCUT INTERCEPT
# ==========================================
st.set_page_config(
    page_title="CADD Core | Reference Engine",
    page_icon="📐",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
<script>
window.addEventListener('keydown', function(e) {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'c') {
        e.stopImmediatePropagation();
        e.preventDefault();
    }
}, true);
</script>
""", unsafe_allow_html=True)

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

# Automated Dictionary fallback icons map to handle search menu visually
EMOJI_ICONS = {
    "line": "✏️", "rectangle": "⬜", "fillet": "↪️", "chamfer": "📐", 
    "extend": "➡️", "offset": "♊", "mirror": "🪞", "explode": "💥", 
    "join": "🔗", "extruded boss/base": "📦", "revolved boss/base": "🔄", 
    "revolved cut": "🛞", "swept boss/base": "〰️", "linear pattern": "░", 
    "circular pattern": "🔘", "rib": "🧱", "straight slot": "💊"
}

clean_db = []
for entry in commands_db:
    if isinstance(entry, dict):
        raw_name = entry.get("name", "Unknown Tool")
        software = entry.get("software", "Universal")
        definition = entry.get("use", "No description provided.")
        
        match = re.search(r"^(.*?)\s*\((.*?)\)$", raw_name)
        if match:
            clean_name = match.group(1).strip()
            shortcut = match.group(2).strip()
        else:
            clean_name = raw_name.strip()
            shortcut = None
            
        fallback_icon = EMOJI_ICONS.get(clean_name.lower(), "🛠️")
            
        clean_db.append({
            "name": clean_name,
            "software": software,
            "shortcut": shortcut,
            "description": definition,
            "emoji": fallback_icon
        })

# ==========================================
# 5. CORE SEARCH INTERFACE
# ==========================================
st.markdown('<h1 style="font-family: monospace; text-align: center; margin-bottom: 5px;">📐 CADD CORE ENGINE</h1>', unsafe_allow_html=True)
st.markdown('<p style="color: #64748B; text-align: center; margin-top: 0px;">Type a tool name or shortcut to search</p>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

search_query = st.text_input("🔍 Search box:", "").strip().lower()

suggestions = []
if search_query:
    for cmd in clean_db:
        if software_choice == "AutoCAD Engine" and cmd["software"] != "AutoCAD":
            continue
        if software_choice == "SolidWorks Engine" and cmd["software"] != "SolidWorks":
            continue
            
        matches_name = search_query in cmd["name"].lower()
        matches_shortcut = cmd["shortcut"] and search_query in cmd["shortcut"].lower()
        
        if matches_name or matches_shortcut:
            if cmd["shortcut"]:
                label = f"{cmd['emoji']} {cmd['name']} [{cmd['shortcut']}] — ({cmd['software']})"
            else:
                label = f"{cmd['emoji']} {cmd['name']} — ({cmd['software']})"
            suggestions.append((label, cmd))

# ==========================================
# 6. DISPLAY SELECTION & RICH CARD VIEW WITH VECTOR ENGINE
# ==========================================
if search_query:
    if suggestions:
        options_labels = [item[0] for item in suggestions]
        selected_label = st.selectbox(f"Select from {len(suggestions)} matching features:", options_labels)
        
        selected_cmd = next(item[1] for item in suggestions if item[0] == selected_label)
        st.markdown("---")
        
        # Color profile logic mapping matching system platform design palettes
        if selected_cmd["software"] == "AutoCAD":
            brand_color = "#E53E3E"  # Autodesk Red
            accent_color = "#38BDF8"
            bg_badge = "rgba(229, 62, 62, 0.15)"
        else:
            brand_color = "#1E40AF"  # Dassault Blue
            accent_color = "#A855F7"
            bg_badge = "rgba(30, 64, 175, 0.2)"

        # Automatically generates the first letter or abbreviation to create a clean UI block
        icon_initials = "".join([word[0] for word in selected_cmd["name"].split()[:2]]).upper()

        with st.container(border=True):
            col_icon, col_title, col_metric = st.columns([1, 4, 2])
            
            with col_icon:
                # DYNAMIC EMBEDDED VECTOR ICON GENERATOR
                st.markdown(f"""
                <div style="
                    display: flex; 
                    align-items: center; 
                    justify-content: center; 
                    width: 52px; 
                    height: 52px; 
                    background-color: {brand_color}; 
                    border-radius: 8px; 
                    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.2);
                    border: 1px solid rgba(255,255,255,0.1);
                    margin-top: 5px;">
                    <span style="
                        color: white !important; 
                        font-family: 'Courier New', monospace; 
                        font-size: 1.35rem; 
                        font-weight: 900; 
                        letter-spacing: -1px;">
                        {icon_initials}
                    </span>
                </div>
                """, unsafe_allow_html=True)
            
            with col_title:
                st.subheader(selected_cmd["name"])
                st.markdown(f"""
                    <span style="
                        font-size: 0.75rem; 
                        background: {bg_badge}; 
                        color: white !important;
                        padding: 3px 8px; 
                        border-radius: 4px; 
                        font-weight: 600;
                        border: 1px solid {brand_color}40;">
                        {selected_cmd['software']} Ecosystem
                    </span>
                """, unsafe_allow_html=True)
                
            with col_metric:
                if selected_cmd["shortcut"]:
                    st.metric(label="System Key", value=selected_cmd["shortcut"])
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.write(selected_cmd["description"])
    else:
        st.info("No matching commands indexed. Adjust entry query tokens.")
else:
    st.markdown("""
    <div style="text-align: center; color: #64748B; padding: 50px 0; font-style: italic; font-family: monospace; font-size: 0.9rem;">
        // Engine ready. Enter key token to begin query sequence.
    </div>
    """, unsafe_allow_html=True)
