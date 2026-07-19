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

# ==========================================
# 3. DYNAMIC WORKSPACE STYLING INJECTION (Safe UI)
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
        </style>
        """, unsafe_allow_html=True)

# ==========================================
# 4. DATABASE LOADING & ULTRA-SAFE KEY EXTRACTOR
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
        # We search every possible text variable style to guarantee we extract the description text
        cmd_name = entry.get("command") or entry.get("name") or entry.get("Command") or entry.get("Name") or "Unknown"
        software = entry.get("software") or entry.get("system") or entry.get("Software") or entry.get("System") or "Universal"
        shortcut = entry.get("shortcut") or entry.get("key") or entry.get("Shortcut") or entry.get("Key") or "N/A"
        
        # Scrape every possible variant of description / definition / info keys
        description = (
            entry.get("description") or 
            entry.get("definition") or 
            entry.get("info") or 
            entry.get("Description") or 
            entry.get("Definition") or 
            entry.get("Info") or 
            "No description text found in database row structure."
        )
        
        clean_db.append({
            "name": str(cmd_name),
            "software": str(software),
            "shortcut": str(shortcut),
            "description": str(description)
        })

# ==========================================
# 5. CORE SEARCH INTERFACE
# ==========================================
st.title("📐 CADD CORE ENGINE")
st.caption("Type a shortcut token to query data structures")
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
            
        if search_query in cmd["name"].lower() or search_query in cmd["shortcut"].lower():
            label = f"{cmd['shortcut']} — {cmd['name']} ({cmd['software']})"
            suggestions.append((label, cmd))

# ==========================================
# 6. INSTANT DEFINITION CARD DISPLAY (Native Streamlit)
# ==========================================
if search_query:
    if suggestions:
        options_labels = [item[0] for item in suggestions]
        selected_label = st.selectbox(f"Select from {len(suggestions)} suggestions:", options_labels)
        
        # Extract matching command row item
        selected_cmd = next(item[1] for item in suggestions if item[0] == selected_label)
        
        st.markdown("---")
        
        # Using Native Streamlit containers completely shields text visibility layout issues!
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(selected_cmd["name"])
                st.caption(f"System: {selected_cmd['software']}")
            with col2:
                st.metric(label="Shortcut", value=selected_cmd["shortcut"])
            
            st.markdown("---")
            st.markdown("**Command Definition:**")
            st.write(selected_cmd["description"])
            
    else:
        st.info("No matching commands indexed. Refine token search query input.")
else:
    st.markdown("""
    <div style="text-align: center; color: #64748B; padding: 50px 0; font-style: italic; font-family: monospace; font-size: 0.9rem;">
        // Engine ready. Enter key token to begin autocomplete mapping sequence.
    </div>
    """, unsafe_allow_html=True)
