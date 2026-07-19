import streamlit as st
import json

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
    st.title("⚙️ STUDIO CONTROL")
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

if ui_theme == "Dark Matte Studio":
    st.markdown("<style>.stApp { background-color: #0D0F12 !important; }</style>", unsafe_allow_html=True)
else:
    st.markdown("<style>.stApp { background-color: #F8FAFC !important; }</style>", unsafe_allow_html=True)

# ==========================================
# 4. DATABASE LOADING
# ==========================================
try:
    with open("commands.json", "r") as f:
        commands_db = json.load(f)
except Exception as e:
    st.error(f"Error loading database: {e}")
    commands_db = []

# ==========================================
# 5. DIAGNOSTIC DATA INSPECTOR (Temporary)
# ==========================================
# This will show us exactly how your file is structured so we can map it perfectly!
st.title("📐 CADD CORE ENGINE")

st.write("### 🔍 Debug Mode: Raw Database Entry Insight")
if commands_db:
    st.info("Here is exactly how your first data entry looks behind the scenes:")
    st.json(commands_db[0])
else:
    st.error("Your commands.json file appears to be completely empty or failed to parse.")

st.markdown("---")

# ==========================================
# 6. SIMPLE FALLBACK SEARCH
# ==========================================
search_query = st.text_input("🔍 Test Search Box:", "").strip().lower()

if search_query and commands_db:
    st.write("Searching raw entries...")
    # Basic dump of entries containing the query to see what text is available
    for entry in commands_db:
        entry_str = str(entry).lower()
        if search_query in entry_str:
            st.code(json.dumps(entry, indent=2))
