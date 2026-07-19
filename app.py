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
# 2. SIDEBAR CONTROL & PREFERENCES PANEL (Cleaned Up)
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
        .description-text { color: #94A3B8 !important; }
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
        .description-text { color: #475569 !important; }
        </style>
        """, unsafe_allow_html=True)

# ==========================================
# 4. DATABASE LOADING & STRUCTURAL RE-MAPPING
# ==========================================
try:
    with open("commands.json", "r") as f:
        commands_db = json.load(f)
except Exception as e:
    st.error(f"Error loading database: {e}")
    commands_db = []

# Safe dictionary key scanner to capture both variations (lower vs capitalized)
def get_field(d, options):
    for opt in options:
        if opt in d: return d[opt]
        if opt.lower() in d: return d[opt.lower()]
        if opt.capitalize() in d: return d[opt.capitalize()]
    return ""

clean_db = []
for entry in commands_db:
    if isinstance(entry, dict):
        clean_db.append({
            "name": get_field(entry, ["command", "name"]),
            "software": get_field(entry, ["software", "system"]),
            "shortcut": get_field(entry, ["shortcut", "key"]),
            "description": get_field(entry, ["description", "info", "definition"])
        })

# ==========================================
# 5. CORE SEARCH INTERFACE
# ==========================================
st.markdown('<h1 style="font-family: monospace; text-align: center; margin-bottom: 5px;">📐 CADD CORE ENGINE</h1>', unsafe_allow_html=True)
st.markdown('<p style="color: #64748B; text-align: center; margin-top: 0px;">Type a shortcut token to query data structures</p>', unsafe_allow_html=True)
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
# 6. INSTANT DEFINITION CARD DISPLAY
# ==========================================
if search_query:
    if suggestions:
        options_labels = [item[0] for item in suggestions]
        selected_label = st.selectbox(f"Select from {len(suggestions)} suggestions:", options_labels)
        
        # Extract matching command row item
        selected_cmd = next(item[1] for item in suggestions if item[0] == selected_label)
        
        st.markdown("---")
        accent_color = "#38BDF8" if selected_cmd["software"] == "AutoCAD" else "#A855F7"
        
        # Unified template styling block bringing back the crystal clear descriptions!
        st.markdown(f"""
        <div style="padding: 24px; border-left: 5px solid {accent_color}; background-color: rgba(255,255,255,0.015); border-radius: 0 8px 8px 0; margin-top: 15px; border-top: 1px solid rgba(255,255,255,0.02); border-right: 1px solid rgba(255,255,255,0.02); border-bottom: 1px solid rgba(255,255,255,0.02);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <div>
                    <span style="font-family: monospace; font-size: 1.5rem; font-weight: 700;">{selected_cmd['name']}</span>
                    <span style="font-size: 0.8rem; background: rgba(255,255,255,0.08); padding: 3px 8px; border-radius: 4px; margin-left: 10px; font-weight: 600;">{selected_cmd['software']}</span>
                </div>
                <span style="font-family: monospace; color: #10B981; font-size: 1.6rem; font-weight: 800;">{selected_cmd['shortcut']}</span>
            </div>
            <div class="description-text" style="font-size: 1.1rem; line-height: 1.6; font-weight: 400; padding-top: 5px;">
                {selected_cmd['description']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("No matching commands indexed. Refine token search query input.")
else:
    st.markdown("""
    <div style="text-align: center; color: #64748B; padding: 50px 0; font-style: italic; font-family: monospace; font-size: 0.9rem;">
        // Engine ready. Enter key token to begin autocomplete mapping sequence.
    </div>
    """, unsafe_allow_html=True)
