import streamlit as st

# =============================
# PAGE CONFIG
# =============================
st.set_page_config(
    page_title="Retirement & Insurance Simulator",
    layout="wide"
)

# =============================
# GLOBAL THEME (DARK + EMERALD)
# =============================
st.markdown("""
<style>

/* Background */
.stApp {
    background-color: #0f172a;
    color: #e5e7eb;
}

/* Headings */
h1, h2, h3 {
    color: #f8fafc;
}

/* Hero */
.hero-title {
    font-size: 44px;
    font-weight: 800;
    margin-bottom: 6px;
}
.hero-subtitle {
    font-size: 18px;
    color: #9ca3af;
    margin-bottom: 32px;
}

/* DARK CARDS (Streamlit-native) */
div[data-testid="stContainer"] {
    background-color: #111827;
    border-radius: 18px;
    border: 1px solid #1f2937;
    padding: 26px;
}

/* Card hover (subtle) */
div[data-testid="stContainer"]:hover {
    box-shadow: 0 0 0 1px #10b981;
    transition: 0.2s ease;
}

/* Metrics */
[data-testid="stMetricValue"] {
    font-size: 30px;
    font-weight: 700;
    color: #10b981;
}

/* Buttons */
.stButton > button {
    background-color: #10b981;
    color: white;
    border-radius: 10px;
    font-weight: 600;
    border: none;
    padding: 0.6rem 1.2rem;
}
.stButton > button:hover {
    background-color: #059669;
}

/* Captions / muted */
.small-text {
    color: #94a3b8;
    font-size: 14px;
}
            
/* Accent text */
.accent {
    color: #5eead4;
    font-weight: 600;
}


</style>
""", unsafe_allow_html=True)

# =============================
# HOME PAGE CONTENT (POLISHED)
# =============================

# HERO
st.markdown("""
<div class="hero-title">
Retirement & Insurance Simulator
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-subtitle">
A simple simulator to understand your
<span class="accent">future savings</span> and
<span class="accent">insurance readiness</span> — in minutes.
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='margin-top: -10px;'></div>", unsafe_allow_html=True)



st.markdown("""
- Estimate the corpus you need by the start of your retirement
- Check if your insurance coverage is actually sufficient  
- Identify gaps before they become financial stress  
""")

st.divider()

# =============================
# CORE MODULES
# =============================
st.markdown("""
<h2 style="text-align: center; margin-bottom: 24px;">
Explore our Simulators
</h2>
""", unsafe_allow_html=True)


col1, col2 = st.columns(2, gap="large")

with col1:
    with st.container(border=True):
        st.markdown("###  Retirement Simulator")
        st.markdown("""
        Understand how today’s decisions affect your life after retirement.
        
        • Project your retirement corpus  
        • Compare required vs actual savings  
        • Detect surplus or shortfall clearly  
        """)
        if st.button("▶ Start Retirement Planning", use_container_width=True):
            st.switch_page("pages/retirement.py")

        st.caption("Long-term planning made visual and intuitive.")

with col2:
    with st.container(border=True):
        st.markdown("###  Insurance Checker")
        st.markdown("""
        See whether your family is truly financially protected.
        
        • Evaluate life & health cover needs  
        • Identify coverage gaps  
        • Understand what needs improvement  
        """)
        if st.button("▶ Check Insurance Coverage", use_container_width=True):
             st.switch_page("pages/insurance.py")

        st.caption("Focuses on protection, not products.")

st.divider()

# =============================
# TRUST & DISCLAIMER
# =============================
st.markdown(
    "<div class='small-text'>"
    "This is an educational simulator designed to improve financial awareness. "
    "It does not provide financial advice, product recommendations, or guarantees."
    "</div>",
    unsafe_allow_html=True
)

