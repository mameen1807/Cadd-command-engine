import streamlit as st
import json
import re

# 1. Canvas Setup
st.set_page_config(page_title="CADD Command Engine", layout="centered")

# 2. Premium Dark Studio Styling & White-Label Logic via CSS Injection
st.markdown("""
    <style>
    /* 1. Complete White-Label Injection: Evaporate all hosting banners, profile menus, and footers */
    #MainMenu, footer, header {visibility: hidden; display: none !important;}
    div[data-testid="stHeader"] {background: transparent !important; background-color: transparent !important; display: none !important;}
    div[data-testid="stToolbar"] {visibility: hidden; display: none !important;}
    div[data-testid="stDecoration"] {display: none !important;}
    div[data-testid="stStatusWidget"] {visibility: hidden; display: none !important;}
    footer {visibility: hidden; display: none !important;}
    .viewerBadge_container__1QS1h {display: none !important;}
    
    /* 2. Matte Charcoal Dark Studio Canvas with Technical Grid */
    .stApp {
        background-color: #0D0F12 !important;
        background-image: linear-gradient(rgba(255, 255, 255, 0.012) 1px, transparent 0),
                          linear-gradient(90deg, rgba(255, 255, 255, 0.012) 1px, transparent 0);
        background-size: 32px 32px;
    }
    
    /* Sleek Typography Rules */
    label, p, .stSelectbox, .stTextInput input {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        letter-spacing: -0.01em;
    }
    
    /* Industrial Input Fields */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: #151922 !important;
        border: 1px solid #222936 !important;
        border-radius: 4px !important;
        color: #E2E8F0 !important;
    }
    
    /* Target Output Container Wrapper for Scan Line */
    div[data-testid="stVerticalBlock"] > div:has(.studio-panel-marker) {
        position: relative;
        padding: 20px 0;
        margin-top: 20px;
        overflow: hidden;
    }
    
    /* Smooth Laser Scanner Drafting Animation */
    div[data-testid="stVerticalBlock"] > div:has(.studio-panel-marker)::after {
        content: '';
        position: absolute;
        top: -100%;
        left: 0;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, transparent, #2563EB, #00D2FF, transparent);
        animation: cadScan 1.6s cubic-bezier(0.25, 1, 0.5, 1) forwards;
    }
    
    @keyframes cadScan {
        0% { top: 0%; opacity: 0; }
        15% { opacity: 1; }
        85% { opacity: 1; }
        100% { top: 100%; opacity: 0; }
    }
    </style>

    <script>
    /* Absolute global hotkey interception to completely squash the Streamlit cache menu */
    window.addEventListener('keydown', function(e) {
        if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'c') {
            e.stopPropagation();
        }
    }, true);
    </script>
    """, unsafe_allow_html=True)

# 3. Clean Studio Branding Header
st.markdown("<h1 style='font-size: 2rem; font-weight: 800; letter-spacing: -0.04em; color: #F8FAFC; margin-bottom:0px;'>CADD COMMAND ENGINE</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 0.95rem; color: #475569; margin-top: 2px;'>A clean creative reference for architectural and solid modelers.</p>", unsafe_allow_html=True)
st.write("---")

# 4. Fresh File Loading
def load_commands_fresh():
    with open("commands.json", "r") as f:
        return json.load(f)

try:
    commands_db = load_commands_fresh()
except Exception as e:
    st.error(f"Error loading commands.json: {e}")
    commands_db = []

# 5. Interface Layout Elements
software_choice = st.selectbox("ENVIRONMENT SETTING", options=["All Softwares", "AutoCAD", "SolidWorks"])

if software_choice != "All Softwares":
    filtered_db = [cmd for cmd in commands_db if cmd["software"] == software_choice]
else:
    filtered_db = commands_db

user_query = st.text_input("QUERY ENTRY", placeholder="Type what you want to achieve...").strip()

# 6. Strict Token-Isolated Search Engine
best_match = None

if user_query:
    query_clean = user_query.strip().lower()
    
    def clean_str(text):
        return re.sub(r'[^a-z0-9\s]', '', text.lower()).strip()
    
    query_alphanumeric = clean_str(query_clean)
    query_words = query_alphanumeric.split()

    exact_match = None
    whole_word_match = None

    # --- PASS 1: Isolated Word Token Matching (No Substring Hijacking) ---
    for cmd in filtered_db:
        cmd_name_clean = clean_str(cmd["name"])
        cmd_name_words = cmd_name_clean.split()
        
        if query_alphanumeric == cmd_name_clean:
            exact_match = cmd
            break
        elif query_alphanumeric in cmd_name_words:
            if not whole_word_match:
                whole_word_match = cmd
        elif query_alphanumeric in cmd_name_clean and (" " in query_alphanumeric):
            if not whole_word_match:
                whole_word_match = cmd

    if exact_match:
        best_match = exact_match
    elif whole_word_match:
        best_match = whole_word_match

    # --- PASS 2: Description Fallback (Whole Word Only) ---
    if not best_match and query_words:
        highest_keyword_count = 0
        for cmd in filtered_db:
            use_lower = f" {clean_str(cmd['use'])} "
            match_count = sum(1 for word in query_words if len(word) > 2 and f" {word} " in use_lower)
            
            if match_count > highest_keyword_count:
                highest_keyword_count = match_count
                best_match = cmd

    # 7. Native Premium Output Display
    if best_match:
        with st.container():
            # Invisible marker element to drop the dynamic laser scan animation line
            st.markdown('<div class="studio-panel-marker"></div>', unsafe_allow_html=True)
            
            st.markdown("<p style='font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.15em; color: #475569; margin-bottom: 0px;'>Platform</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size: 1rem; font-weight: 500; color: #94A3B8; margin-top: 0px;'>{best_match['software'].upper()}</p>", unsafe_allow_html=True)
            
            st.markdown("<p style='font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.15em; color: #475569; margin-bottom: 0px;'>Command</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size: 2.2rem; font-weight: 700; letter-spacing: -0.03em; color: #F8FAFC; margin-top: 0px; margin-bottom: 10px;'>{best_match['name']}</p>", unsafe_allow_html=True)
            
            st.markdown("<div style='width: 100%; height: 1px; background: #222936; margin: 20px 0;'></div>", unsafe_allow_html=True)
            
            st.markdown("<p style='font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.15em; color: #475569; margin-bottom: 0px;'>Application Description</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size: 1.15rem; line-height: 1.7; color: #CBD5E1; font-weight: 400; margin-top: 0px;'>{best_match['use']}</p>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='color: #475569; font-size: 0.9rem; margin-top: 15px;'>No matching command key found. Try another design keyword.</p>", unsafe_allow_html=True)
