import streamlit as st
import json
import re

# ==========================================
# 1. CORE WEBAPP PAGE SETUP & SAFETY HOOKS
# ==========================================
st.set_page_config(
    page_title="CADD Core | Reference Engine",
    page_icon="📐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Complete global styling overrides to crush bugs
st.markdown("""
<script>
window.addEventListener('keydown', function(e) {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'c') {
        e.stopImmediatePropagation();
        e.preventDefault();
    }
}, true);
</script>
<style>
/* Total, absolute elimination of the hover link symbols (#) */
.element-hover-anchor, 
a.element-hover-anchor, 
[data-testid="stHeaderActionElements"] a,
h1 a, h2 a, h3 a, h4 a, h5 a, h6 a,
svg.element-hover-anchor,
.st-emotion-cache-bho8b9 e1nzilva5 {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    width: 0 !important;
    height: 0 !important;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. SIDEBAR WORKSPACE OPTIMIZATION
# ==========================================
with st.sidebar:
    st.markdown('### ⚙️ SYSTEM SETTINGS')
    ui_theme = st.selectbox(
        "Workspace Visual Theme", 
        ["Dark Matte Studio", "Drafting Light Mode"]
    )

# ==========================================
# 3. HIGH-CONTRAST CANVAS CONFIGURATION
# ==========================================
if ui_theme == "Dark Matte Studio":
    st.markdown("""
        <style>
        .stApp {
            background-color: #0D0F12 !important;
            background-image: linear-gradient(rgba(255, 255, 255, 0.012) 1px, transparent 0),
                              linear-gradient(90deg, rgba(255, 255, 255, 0.012) 1px, transparent 0) !important;
            background-size: 32px 32px !important;
        }
        section[data-testid="stSidebar"] { background-color: #11141B !important; }
        h1, h2, h3, h4, h5, h6, p, label, span, div { color: #E2E8F0 !important; }
        input { background-color: #151922 !important; color: #E2E8F0 !important; border: 1px solid #222936 !important; }
        </style>
        """, unsafe_allow_html=True)
    brand_autocad = "#EF4444"
    brand_solidworks = "#3B82F6"
else:
    st.markdown("""
        <style>
        .stApp {
            background-color: #F8FAFC !important;
            background-image: linear-gradient(rgba(15, 23, 42, 0.03) 1px, transparent 0),
                              linear-gradient(90deg, rgba(15, 23, 42, 0.03) 1px, transparent 0) !important;
            background-size: 24px 24px !important;
        }
        section[data-testid="stSidebar"] { background-color: #FFFFFF !important; border-right: 1px solid #E2E8F0 !important; }
        h1, h2, h3, h4, h5, h6, p, label, span, div, .stMarkdown p { color: #0F172A !important; }
        input { background-color: #FFFFFF !important; color: #0F172A !important; border: 1px solid #94A3B8 !important; }
        div[data-testid="stTextInput"] div[data-baseweb="input"] { background-color: #FFFFFF !important; }
        div[role="listbox"], div[data-testid="stSelectbox"] div { background-color: #FFFFFF !important; color: #0F172A !important; }
        </style>
        """, unsafe_allow_html=True)
    brand_autocad = "#DC2626"
    brand_solidworks = "#2563EB"

# ==========================================
# 4. DATABASE CONFIGURATION
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
        
        match = re.search(r"^(.*?)\s*\((.*?)\)$", raw_name)
        if match:
            clean_name = match.group(1).strip()
            shortcut = match.group(2).strip()
        else:
            clean_name = raw_name.strip()
            shortcut = None
            
        clean_db.append({
            "name": clean_name,
            "software": software,
            "shortcut": shortcut,
            "description": definition
        })

# ==========================================
# 5. MAIN PAGE INTERFACE & WORKSPACE TABS
# ==========================================
st.title("📐 CADD CORE ENGINE")
st.caption("Instant Engine Autocomplete Reference")
st.markdown("<br>", unsafe_allow_html=True)

# Replacing the buggy segmented control bar with high-contrast native layout columns!
st.markdown("##### 🖥️ Filter CAD Subsystem")
c1, c2, c3 = st.columns(3)
with c1:
    btn_all = st.button("🌐 All Systems", use_container_width=True, type="secondary" if st.session_state.get("subsystem", "All Systems") != "All Systems" else "primary")
    if btn_all: st.session_state["subsystem"] = "All Systems"
with c2:
    btn_cad = st.button("❤️ AutoCAD Engine", use_container_width=True, type="primary" if st.session_state.get("subsystem", "All Systems") == "AutoCAD Engine" else "secondary")
    if btn_cad: st.session_state["subsystem"] = "AutoCAD Engine"
with c3:
    btn_sw = st.button("💙 SolidWorks Engine", use_container_width=True, type="primary" if st.session_state.get("subsystem", "All Systems") == "SolidWorks Engine" else "secondary")
    if btn_sw: st.session_state["subsystem"] = "SolidWorks Engine"

software_choice = st.session_state.get("subsystem", "All Systems")
st.markdown("<br>", unsafe_allow_html=True)

search_query = st.text_input("🔍 Search Command Registry:", "").strip().lower()

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
                label = f"{cmd['name']} [{cmd['shortcut']}] — ({cmd['software']})"
            else:
                label = f"{cmd['name']} — ({cmd['software']})"
            suggestions.append((label, cmd))

# ==========================================
# 6. FIXED CONTAINER VIEW
# ==========================================
if search_query:
    if suggestions:
        options_labels = [item[0] for item in suggestions]
        selected_label = st.selectbox(f"Select from {len(suggestions)} matches:", options_labels)
        
        selected_cmd = next(item[1] for item in suggestions if item[0] == selected_label)
        st.markdown("---")
        
        active_color = brand_autocad if selected_cmd["software"] == "AutoCAD" else brand_solidworks
        icon_initials = "".join([word[0] for word in selected_cmd["name"].split()[:2]]).upper()

        with st.container(border=True):
            col_icon, col_meta, col_key = st.columns([1, 4, 2])
            
            with col_icon:
                st.markdown(f"""
                <div style="display:flex; align-items:center; justify-content:center; 
                            width:50px; height:50px; background-color:{active_color}; border-radius:8px;">
                    <span style="color:#FFFFFF !important; font-family:monospace; font-size:1.3rem; font-weight:800;">
                        {icon_initials}
                    </span>
                </div>
                """, unsafe_allow_html=True)
                
            with col_meta:
                st.subheader(selected_cmd['name'])
                st.markdown(f"<span style='font-size:0.85rem; font-weight:700; color:{active_color};'>{selected_cmd['software']} Workspace Tool</span>", unsafe_allow_html=True)
                
            with col_key:
                if selected_cmd["shortcut"]:
                    st.metric(label="Key Shortcut", value=selected_cmd["shortcut"])
            
            st.markdown("---")
            st.write(selected_cmd["description"])
            
    else:
        st.info("No matching commands indexed. Adjust entry query tokens.")
else:
    st.markdown("""
    <div style="text-align: center; color: #64748B; padding: 50px 0; font-style: italic; font-family: monospace; font-size: 0.9rem;">
        // Engine standby. Awaiting subsystem selection token inputs...
    </div>
    """, unsafe_allow_html=True)
