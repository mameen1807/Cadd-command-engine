import streamlit as st
import json

# ==========================================
# 1. CORE WEBAPP PAGE SETUP
# ==========================================
st.set_page_config(
    page_title="CADD Core | Reference Engine",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. SIDEBAR CONTROL & PREFERENCES PANEL
# ==========================================
with st.sidebar:
    st.markdown('<h2 style="color: #38BDF8; font-family: monospace; margin-bottom: 5px;">⚙️ STUDIO CONTROL</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color: #64748B; font-size: 0.85rem; margin-top: 0px;">Configure your terminal workspace layout</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    ui_theme = st.selectbox(
        "Workspace Visual Theme", 
        ["Dark Matte Studio", "Drafting Light Mode"]
    )
    
    view_mode = st.selectbox(
        "Default Search View",
        ["Comprehensive Layout", "Compact Command Table"]
    )
    
    st.markdown("---")
    
    st.markdown('<h3 style="color: #E2E8F0; font-size: 1rem; font-family: monospace;">🖥️ SOFTWARE ENGINE</h3>', unsafe_allow_html=True)
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
        label, p, span, h1, h2, h3 { color: #E2E8F0 !important; }
        table, th, td { color: #E2E8F0 !important; background-color: #151922 !important; }
        .stTextInput input { background-color: #151922 !important; border: 1px solid #222936 !important; color: #E2E8F0 !important; }
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
        label, p, span, h1, h2, h3 { color: #0F172A !important; }
        table, th, td { color: #0F172A !important; background-color: #FFFFFF !important; }
        .stTextInput input { background-color: #FFFFFF !important; border: 1px solid #CBD5E1 !important; color: #0F172A !important; }
        </style>
        """, unsafe_allow_html=True)

# ==========================================
# 4. DATABASE LOADING
# ==========================================
try:
    with open("commands.json", "r") as f:
        commands_db = json.load(f)
except Exception as e:
    st.error(f"Error loading commands.json: {e}")
    commands_db = []

# ==========================================
# 5. CORE LAYOUT & INTERFACE RENDERING
# ==========================================
st.markdown('<h1 style="font-family: monospace; letter-spacing: -0.03em; font-weight: 700; margin-bottom: 5px;">📐 CADD CORE ENGINE</h1>', unsafe_allow_html=True)
st.markdown('<p style="color: #64748B; margin-top: 0px;">Instant production search matrix for engineering subsystems</p>', unsafe_allow_html=True)

search_query = st.text_input("🔍 Input token query (e.g., line, extrude):", "").strip().lower()

# ==========================================
# 6. INTELLIGENT KEY MAPPING LOGIC
# ==========================================
# This loops through your actual JSON entries and safely extracts data even if keys are uppercase or named differently
processed_commands = []
for entry in commands_db:
    if not isinstance(entry, dict):
        continue
        
    # Helper to scan items regardless of casing (e.g., Command vs command)
    def get_flexible_field(d, options, default=""):
        for opt in options:
            if opt in d: return str(d[opt])
            if opt.lower() in d: return str(d[opt.lower()])
            if opt.capitalize() in d: return str(d[opt.capitalize()])
            if opt.upper() in d: return str(d[opt.upper()])
        return default

    cmd_name = get_flexible_field(entry, ["command", "name", "tool", "key"])
    cmd_soft = get_flexible_field(entry, ["software", "system", "app", "platform"], default="AutoCAD")
    cmd_short = get_flexible_field(entry, ["shortcut", "key", "hotkey", "alias"])
    cmd_desc = get_flexible_field(entry, ["description", "info", "action", "function"])

    # Evaluate Subsystem Filter Constraints
    if software_choice == "AutoCAD Engine" and "autocad" not in cmd_soft.lower():
        continue
    if software_choice == "SolidWorks Engine" and "solidworks" not in cmd_soft.lower():
        continue
        
    # Process Search Text
    if search_query:
        match_found = (
            search_query in cmd_name.lower() or 
            search_query in cmd_short.lower() or 
            search_query in cmd_desc.lower()
        )
        if not match_found:
            continue
            
    processed_commands.append({
        "name": cmd_name,
        "software": "AutoCAD" if "autocad" in cmd_soft.lower() else "SolidWorks",
        "shortcut": cmd_short,
        "description": cmd_desc
    })

# ==========================================
# 7. DYNAMIC DATA OUTPUT MATRIX
# ==========================================
st.markdown("---")

if processed_commands:
    if view_mode == "Comprehensive Layout":
        for cmd in processed_commands:
            accent_color = "#38BDF8" if cmd["software"] == "AutoCAD" else "#A855F7"
            st.markdown(f"""
            <div class="studio-panel-marker" style="padding: 16px; border-left: 4px solid {accent_color}; background-color: rgba(255,255,255,0.02); border-radius: 0 6px 6px 0; margin-bottom: 12px;">
                <span style="font-family: monospace; font-size: 1.15rem; font-weight: bold;">{cmd['name']}</span> 
                <span style="font-size: 0.8rem; background: rgba(255,255,255,0.08); padding: 2px 6px; border-radius: 4px; margin-left: 8px;">{cmd['software']}</span>
                <span style="float: right; font-family: monospace; color: #10B981; font-weight: bold;">{cmd['shortcut']}</span>
                <p style="margin: 8px 0 0 0; font-size: 0.95rem; opacity: 0.85;">{cmd['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            
    elif view_mode == "Compact Command Table":
        table_data = []
        for cmd in processed_commands:
            table_data.append({
                "System Platform": "📐 CAD" if cmd['software'] == "AutoCAD" else "💎 SW",
                "Key Command": cmd['name'],
                "Hot Shortcut": cmd['shortcut'],
                "Function Scope": cmd['description']
            })
        st.table(table_data)
else:
    # If the database itself is empty or completely unreadable, print the key structure as a hint
    if commands_db and len(commands_db) > 0:
        st.warning("Data loaded, but fields couldn't be auto-mapped.")
        st.write("Diagnostic - Your JSON keys look like this:", list(commands_db[0].keys()))
    else:
        st.info("No matching structural tool definitions found.")
