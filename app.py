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
    
    # User Preference Toggles
    ui_theme = st.selectbox(
        "Workspace Visual Theme", 
        ["Dark Matte Studio", "Drafting Light Mode"]
    )
    
    view_mode = st.selectbox(
        "Default Search View",
        ["Comprehensive Layout", "Compact Command Table"],
        help="Choose how the engine results display automatically when you search."
    )
    
    st.markdown("---")
    
    # System Platform Engine Filters (Our original system controls)
    st.markdown('<h3 style="color: #E2E8F0; font-size: 1rem; font-family: monospace;">🖥️ SOFTWARE ENGINE</h3>', unsafe_allow_html=True)
    software_choice = st.radio(
        "Filter CAD Subsystem:",
        ["All Systems", "AutoCAD Engine", "SolidWorks Engine"]
    )

# ==========================================
# 3. DYNAMIC WORKSPACE STYLING INJECTION
# ==========================================
if ui_theme == "Dark Matte Studio":
    # Premium Dark Studio Canvas with a Subtle Structural Grid Layout
    st.markdown("""
        <style>
        .stApp {
            background-color: #0D0F12 !important;
            background-image: linear-gradient(rgba(255, 255, 255, 0.012) 1px, transparent 0),
                              linear-gradient(90deg, rgba(255, 255, 255, 0.012) 1px, transparent 0);
            background-size: 32px 32px;
        }
        label, p, span, h1, h2, h3 { color: #E2E8F0 !important; }
        
        /* Force high contrast table text for dark mode */
        table, th, td { color: #E2E8F0 !important; background-color: #151922 !important; }
        
        .stTextInput input {
            background-color: #151922 !important;
            border: 1px solid #222936 !important;
            color: #E2E8F0 !important;
        }
        /* Smooth Laser Scanner Drafting Animation for Dark Mode */
        div[data-testid="stVerticalBlock"] > div:has(.studio-panel-marker)::after {
            content: ''; position: absolute; top: -100%; left: 0; width: 100%; height: 2px;
            background: linear-gradient(90deg, transparent, #2563EB, #00D2FF, transparent);
            animation: cadScan 1.6s ease-in-out forwards;
        }
        @keyframes cadScan { 0% { top: 0%; opacity: 0; } 50% { opacity: 1; } 100% { top: 100%; opacity: 0; } }
        </style>
        """, unsafe_allow_html=True)
else:
    # High-Visibility Drafting Light Mode (Mimics blueprint printing paper layouts)
    st.markdown("""
        <style>
        .stApp {
            background-color: #F8FAFC !important;
            background-image: linear-gradient(rgba(15, 23, 42, 0.03) 1px, transparent 0),
                              linear-gradient(90deg, rgba(15, 23, 42, 0.03) 1px, transparent 0);
            background-size: 24px 24px;
        }
        label, p, span, h1, h2, h3 { color: #0F172A !important; }
        
        /* Force high contrast table text for light mode */
        table, th, td { color: #0F172A !important; background-color: #FFFFFF !important; }
        
        .stTextInput input {
            background-color: #FFFFFF !important;
            border: 1px solid #CBD5E1 !important;
            color: #0F172A !important;
        }
        /* Orange Construction Drafting Line Animation for Light Mode */
        div[data-testid="stVerticalBlock"] > div:has(.studio-panel-marker)::after {
            content: ''; position: absolute; top: -100%; left: 0; width: 100%; height: 2px;
            background: linear-gradient(90deg, transparent, #EA580C, #F97316, transparent);
            animation: cadScan 1.6s ease-in-out forwards;
        }
        @keyframes cadScan { 0% { top: 0%; opacity: 0; } 50% { opacity: 1; } 100% { top: 100%; opacity: 0; } }
        </style>
        """, unsafe_allow_html=True)

# ==========================================
# 4. DATABASE LOADING
# ==========================================
try:
    with open("commands.json", "r") as f:
        commands_db = json.load(f)
except Exception as e:
    st.error(f"Error loading commands.json database tracking assets: {e}")
    commands_db = []

# ==========================================
# 5. CORE LAYOUT & INTERFACE RENDERING
# ==========================================
st.markdown('<h1 style="font-family: monospace; letter-spacing: -0.03em; font-weight: 700; margin-bottom: 5px;">📐 CADD CORE ENGINE</h1>', unsafe_allow_html=True)
st.markdown('<p style="color: #64748B; margin-top: 0px;">Instant production search matrix for engineering subsystems</p>', unsafe_allow_html=True)

# Central Terminal Search Target
search_query = st.text_input("🔍 Input token query (e.g., line, extrude, circle):", "").strip().lower()

# Token Processing & Filtration Engine Logic
filtered_commands = []
for cmd in commands_db:
    # Evaluate Subsystem Filter Constraints First
    if software_choice == "AutoCAD Engine" and cmd["software"] != "AutoCAD":
        continue
    if software_choice == "SolidWorks Engine" and cmd["software"] != "SolidWorks":
        continue
        
    # Process Search Query String Tokens
    if search_query:
        match_found = (
            search_query in cmd["command"].lower() or 
            search_query in cmd["shortcut"].lower() or 
            search_query in cmd["description"].lower()
        )
        if not match_found:
            continue
            
    filtered_commands.append(cmd)

# ==========================================
# 6. DYNAMIC DATA OUTPUT MATRIX
# ==========================================
st.markdown("---")

if filtered_commands:
    if view_mode == "Comprehensive Layout":
        # Classic high-fidelity tracking cards
        for cmd in filtered_commands:
            accent_color = "#38BDF8" if cmd["software"] == "AutoCAD" else "#A855F7"
            st.markdown(f"""
            <div class="studio-panel-marker" style="padding: 16px; border-left: 4px solid {accent_color}; background-color: rgba(255,255,255,0.02); border-radius: 0 6px 6px 0; margin-bottom: 12px;">
                <span style="font-family: monospace; font-size: 1.15rem; font-weight: bold;">{cmd['command']}</span> 
                <span style="font-size: 0.8rem; background: rgba(255,255,255,0.08); padding: 2px 6px; border-radius: 4px; margin-left: 8px;">{cmd['software']}</span>
                <span style="float: right; font-family: monospace; color: #10B981; font-weight: bold;">{cmd['shortcut']}</span>
                <p style="margin: 8px 0 0 0; font-size: 0.95rem; opacity: 0.85;">{cmd['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            
    elif view_mode == "Compact Command Table":
        # CRITICAL FIX: The keys here must match the raw lowercase JSON dictionary entries precisely!
        table_data = []
        for cmd in filtered_commands:
            table_data.append({
                "System Platform": "📐 CAD" if cmd['software'] == "AutoCAD" else "💎 SW",
                "Key Command": cmd['command'],
                "Hot Shortcut": cmd['shortcut'],
                "Function Scope": cmd['description']
            })
        st.table(table_data)
else:
    st.info("No matching structural tool definitions mapped to query tokens.")
