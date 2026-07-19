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

# Kills Ctrl+C cache interrupts AND violently strips away the hover link symbols (#)
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
/* Hides the structural link anchors globally */
a.element-hover-anchor {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. THEME SELECTION & HIGH-CONTRAST ENGINE
# ==========================================
with st.sidebar:
    st.markdown('<h2 style="font-family: monospace;">⚙️ THEME MATRIX</h2>', unsafe_allow_html=True)
    ui_theme = st.selectbox(
        "Workspace Visual Theme", 
        ["Dark Matte Studio", "Drafting Light Mode"]
    )

if ui_theme == "Dark Matte Studio":
    st.markdown("""
        <style>
        .stApp {
            background-color: #0D0F12 !important;
            background-image: linear-gradient(rgba(255, 255, 255, 0.012) 1px, transparent 0),
                              linear-gradient(90deg, rgba(255, 255, 255, 0.012) 1px, transparent 0);
            background-size: 32px 32px;
        }
        label, p, span, h1, h2, h3, div, h4 { color: #E2E8F0 !important; }
        .stTextInput input, .stSelectbox div { background-color: #151922 !important; border: 1px solid #222936 !important; color: #E2E8F0 !important; }
        .stContentBlock { background-color: #11141B !important; border: 1px solid #222936 !important; }
        /* High contrast colors for text inside badges on Dark Mode */
        .badge-txt { color: #FFFFFF !important; }
        </style>
        """, unsafe_allow_html=True)
    autocad_badge = "rgba(239, 68, 68, 0.25)"
    solidworks_badge = "rgba(59, 130, 246, 0.25)"
else:
    st.markdown("""
        <style>
        .stApp {
            background-color: #F8FAFC !important;
            background-image: linear-gradient(rgba(15, 23, 42, 0.03) 1px, transparent 0),
                              linear-gradient(90deg, rgba(15, 23, 42, 0.03) 1px, transparent 0);
            background-size: 24px 24px;
        }
        /* Forces deep, razor-sharp dark text on light mode to prevent fading out */
        label, p, span, h1, h2, h3, div, h4, .stMarkdown p { color: #0F172A !important; font-weight: 500; }
        h1, h2, h3 { color: #020617 !important; font-weight: 700 !important; }
        .stTextInput input, .stSelectbox div { background-color: #FFFFFF !important; border: 1px solid #94A3B8 !important; color: #0F172A !important; }
        .stContentBlock { background-color: #FFFFFF !important; border: 1px solid #CBD5E1 !important; }
        /* Dark text for badges inside Light Mode for visibility */
        .badge-txt { color: #0F172A !important; }
        </style>
        """, unsafe_allow_html=True)
    autocad_badge = "rgba(239, 68, 68, 0.15)"
    solidworks_badge = "rgba(59, 130, 246, 0.15)"

# ==========================================
# 3. DATABASE CONFIGURATION
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
# 4. MAIN PAGE INTERFACE & ROW SELECTORS
# ==========================================
st.markdown('<h1 style="font-family: monospace; text-align: center; margin-bottom: 5px;">📐 CADD CORE ENGINE</h1>', unsafe_allow_html=True)
st.markdown('<p style="color: #64748B; text-align: center; margin-top: 0px;">Instant Engine Autocomplete Reference</p>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# CAD Systems are now placed on the main page layout!
software_choice = st.segmented_control(
    "Select Subsystem Workspace Mode:",
    ["All Systems", "AutoCAD Engine", "SolidWorks Engine"],
    default="All Systems"
)
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
# 5. HIGH-CONTRAST CARD RENDERING
# ==========================================
if search_query:
    if suggestions:
        options_labels = [item[0] for item in suggestions]
        selected_label = st.selectbox(f"Select from {len(suggestions)} matches:", options_labels)
        
        selected_cmd = next(item[1] for item in suggestions if item[0] == selected_label)
        st.markdown("---")
        
        if selected_cmd["software"] == "AutoCAD":
            brand_color = "#DC2626"  # True Red
            bg_badge = autocad_badge
            border_line = "rgba(220, 38, 38, 0.4)"
        else:
            brand_color = "#2563EB"  # True Blue
            bg_badge = solidworks_badge
            border_line = "rgba(37, 99, 235, 0.4)"

        icon_initials = "".join([word[0] for word in selected_cmd["name"].split()[:2]]).upper()

        # Custom container using dynamic classes ensuring high contrast styles
        st.markdown(f"""
        <div class="stContentBlock" style="
            padding: 24px; 
            border-radius: 12px; 
            border-left: 6px solid {brand_color};
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            margin-top: 10px;">
            <table style="width:100%; border-collapse:collapse; border:none;">
                <tr style="border:none; background:none;">
                    <td style="width:65px; vertical-align:middle; border:none; padding:0;">
                        <div style="
                            display: flex; 
                            align-items: center; 
                            justify-content: center; 
                            width: 50px; 
                            height: 50px; 
                            background-color: {brand_color}; 
                            border-radius: 8px;">
                            <span style="
                                color: #FFFFFF !important; 
                                font-family: monospace; 
                                font-size: 1.3rem; 
                                font-weight: 800;">
                                {icon_initials}
                            </span>
                        </div>
                    </td>
                    <td style="vertical-align:middle; border:none; padding:0;">
                        <h3 style="margin:0; padding:0; line-height:1.2;">{selected_cmd['name']}</h3>
                        <div style="margin-top: 6px;">
                            <span class="badge-txt" style="
                                font-size: 0.75rem; 
                                background: {bg_badge}; 
                                padding: 4px 10px; 
                                border-radius: 6px; 
                                font-weight: 700;
                                border: 1px solid {brand_color};">
                                {selected_cmd['software']} Environment
                            </span>
                        </div>
                    </td>
                    <td style="text-align:right; vertical-align:middle; border:none; padding:0;">
                        {f'<div><span style="font-size:0.75rem; color:#64748B; font-weight:700; text-transform:uppercase; display:block; margin-bottom:2px;">Key Map</span><span style="font-family:monospace; font-size:1.5rem; font-weight:800; color:{brand_color} !important;">{selected_cmd["shortcut"]}</span></div>' if selected_cmd["shortcut"] else ''}
                    </td>
                </tr>
            </table>
            <hr style="border:none; border-top: 1px solid {border_line}; margin: 20px 0;">
            <div style="font-size: 1.05rem; line-height: 1.6; font-weight: 500;">
                {selected_cmd['description']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("No matching commands indexed. Adjust entry query tokens.")
else:
    st.markdown("""
    <div style="text-align: center; color: #64748B; padding: 50px 0; font-style: italic; font-family: monospace; font-size: 0.9rem;">
        // Engine standby. Awaiting subsystem selection token inputs...
    </div>
    """, unsafe_allow_html=True)
