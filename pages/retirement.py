import streamlit as st
import pandas as pd
import altair as alt

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Retirement Simulator",
    layout="wide"
)

# ============================================================
# GLOBAL THEME — MATCHES MAIN APP
# ============================================================
st.markdown("""
<style>
/* ===== GLOBAL TEXT SCALE ===== */
html, body, [class*="css"] {
    font-size: 17px;   /* default is ~14px */
}

/* =============================
   GLOBAL ACCENT COLOR (KEY FIX)
   ============================= */
:root {
    accent-color: #10b981;
}

/* =============================
   BASE APP
   ============================= */
.stApp {
    background-color: #0f172a;
    color: #e5e7eb;
}

/* =============================
   HEADINGS
   ============================= */
h1, h2, h3 {
    color: #f8fafc;
}

/* =============================
   CONTAINERS (CARDS)
   ============================= */
div[data-testid="stContainer"] {
    background-color: #111827;
    border-radius: 18px;
    border: 1px solid #1f2937;
    padding: 26px;
}
div[data-testid="stContainer"]:hover {
    box-shadow: 0 0 0 1px #10b981;
}

/* NUMBER INPUT WRAPPER FIX */
/* NUMBER INPUT WRAPPER FIX */
div[data-testid="stNumberInput"] {
    overflow: visible;
    border-radius: 14px;
}

div[data-testid="stNumberInput"] > div {
    border-radius: 14px;
    overflow: hidden;
}
/* NUMBER INPUT WRAPPER FIX */
div[data-testid="stNumberInput"] {
    overflow: visible;
    border-radius: 14px;
}

div[data-testid="stNumberInput"] > div {
    border-radius: 14px;
    overflow: hidden;
}

/* INPUT FIELD */
input[type="number"],
input[type="text"] {
    background-color: #020617 !important;
    color: #e5e7eb !important;

    border: 1px solid #1f2937 !important;
    border-right: none !important;

    border-radius: 14px 0 0 14px !important;
}

/* FOCUS */
input[type="number"]:focus,
input[type="text"]:focus {
    border-color: #10b981 !important;
    outline: none !important;
    box-shadow: none !important;
}
/* INPUT FIELD */
/* FOCUS */
input[type="number"]:focus,
input[type="text"]:focus {
    border-color: #10b981 !important;
    outline: none !important;
    box-shadow: none !important;
}

/* Kill BaseWeb wrapper borders */
div[data-baseweb="base-input"],
div[data-baseweb="input"] {
    border: none !important;
    box-shadow: none !important;
}

div[data-baseweb="base-input"]:hover,
div[data-baseweb="base-input"]:focus,
div[data-baseweb="base-input"]:focus-within,
div[data-baseweb="input"]:hover,
div[data-baseweb="input"]:focus,
div[data-baseweb="input"]:focus-within {
    border: none !important;
    box-shadow: none !important;
}

/* MINUS BUTTON */
button[data-testid="stNumberInputStepDown"] {
    background-color: #020617 !important;
    color: #ffffff !important;

    border-top: 1px solid #1f2937 !important;
    border-bottom: 1px solid #1f2937 !important;
    border-left: 1px solid #1f2937 !important;
    border-right: none !important;

    margin-left: -1px !important;   /* 🔥 KEY FIX */
    border-radius: 0 !important;
}

/* PLUS BUTTON */
button[data-testid="stNumberInputStepUp"] {
    background-color: #020617 !important;
    color: #ffffff !important;

    border: 1px solid #1f2937 !important;
    border-left: none !important;

    margin-left: -1px !important;   /* 🔥 KEY FIX */
    border-radius: 0 14px 14px 0 !important;
}

/* PLUS BUTTON FOCUS STATE - Match input border color */
input[type="number"]:focus ~ div button[data-testid="stNumberInputStepUp"],
input[type="text"]:focus ~ div button[data-testid="stNumberInputStepUp"] {
    border-color: #10b981 !important;
}

/* MINUS BUTTON FOCUS STATE - Match input border color */
input[type="number"]:focus ~ div button[data-testid="stNumberInputStepDown"],
input[type="text"]:focus ~ div button[data-testid="stNumberInputStepDown"] {
    border-color: #10b981 !important;
}

/* HOVER */
button[data-testid="stNumberInputStepUp"]:hover,
button[data-testid="stNumberInputStepDown"]:hover {
    background-color: #10b981 !important;
    color: #020617 !important;
}

/* FOCUS */
input[type="number"]:focus,
input[type="text"]:focus {
    border-color: #10b981 !important;
    outline: none !important;
    box-shadow: none !important;
}



/* =============================
   PRIMARY BUTTON
   ============================= */
.stButton > button {
    background-color: #10b981;
    color: #022c22;
    border-radius: 12px;
    font-weight: 700;
    border: none;
    padding: 0.8rem 1.6rem;
}
.stButton > button:hover {
    background-color: #059669;
}

/* =============================
   METRICS
   ============================= */
[data-testid="stMetricValue"] {
    color: #5eead4;
    font-weight: 800;
}



/* =============================
   SCROLLBAR
   ============================= */
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-thumb {
    background: #10b981;
    border-radius: 10px;
}
            
            /* ===== NUMBER INPUT + / − BUTTON BORDER ===== */
button[data-testid="stNumberInputStepUp"],
button[data-testid="stNumberInputStepDown"] {
    background-color: #020617 !important;    /* dark background */
    color: #ffffff !important;
    padding: 0.25rem 0.25rem !important;
}



/* =============================
   PROGRESS BAR — HARD RESET
   ============================= */

/* Kill Streamlit default wrapper */
div[data-testid="stProgress"] {
    background: transparent !important;
    padding: 0 !important;
}

/* Kill BaseWeb progress visuals */
div[data-testid="stProgress"] div[role="progressbar"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

/* Track */
div[data-testid="stProgress"] > div {
    background-color: #020617 !important;
    height: 12px !important;
    border-radius: 999px !important;
    overflow: hidden !important;
}

/* Fill */
div[data-testid="stProgress"] > div > div {
    background-color: #10b981 !important;
    height: 100% !important;
    border-radius: 999px !important;
}

/* Nuclear option — remove ALL outlines */
div[data-testid="stProgress"],
div[data-testid="stProgress"] *,
div[data-testid="stProgress"] *::before,
div[data-testid="stProgress"] *::after {
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
}

</style>
""", unsafe_allow_html=True)



# ============================================================
# CONSTANTS (UNCHANGED)
# ============================================================
INFLATION = 0.06
POST_RET_RETURN = 0.05
MAX_SIP_GROWTH = 0.15

ASSET_RETURNS = {
    "Equity": 0.12,
    "Debt": 0.07,
    "Gold": 0.06,
    "Savings": 0.04
}

RISK_ALLOC = {
    1: {"Equity": 0.25, "Debt": 0.45, "Gold": 0.10, "Savings": 0.20},
    2: {"Equity": 0.35, "Debt": 0.40, "Gold": 0.10, "Savings": 0.15},
    3: {"Equity": 0.50, "Debt": 0.30, "Gold": 0.10, "Savings": 0.10},
    4: {"Equity": 0.65, "Debt": 0.20, "Gold": 0.10, "Savings": 0.05},
    5: {"Equity": 0.75, "Debt": 0.10, "Gold": 0.10, "Savings": 0.05},
}

# ============================================================
# ALTAR DARK THEME (GLOBAL)
# ============================================================
alt.themes.register(
    "dark_emerald",
    lambda: {
        "config": {
            "background": "transparent",
            "axis": {
                "labelColor": "#9ca3af",
                "titleColor": "#e5e7eb",
                "gridColor": "#1f2937",
                "tickColor": "#374151",
            },
            "legend": {
                "labelColor": "#e5e7eb",
                "titleColor": "#e5e7eb"
            },
            "range": {
                "category": ["#10b981", "#5eead4", "#34d399", "#059669"]
            }
        }
    }
)
alt.themes.enable("dark_emerald")

# ============================================================
# HEADER
# ============================================================
st.markdown("## Retirement Simulator")
st.markdown("Understand how much money you’ll need for retirement — and how to realistically get there.")
st.divider()

# ============================================================
# RETIREMENT CORPUS ENGINES (ONLY THIS LOGIC CHANGED)
# ============================================================

def portfolio_return(risk):
    return sum(RISK_ALLOC[risk][a] * ASSET_RETURNS[a] for a in ASSET_RETURNS)


def required_corpus_portfolio(monthly_expense_today, years_to_ret, retirement_years, risk):
    annual = monthly_expense_today * 12 * ((1 + INFLATION) ** years_to_ret)
    r = portfolio_return(risk)

    def survives(C):
        E = annual
        for _ in range(retirement_years):
            C = C * (1 + r) - E
            if C < 0:
                return False
            E *= (1 + INFLATION)
        return True

    lo, hi = 0, 1e11
    for _ in range(100):
        mid = (lo + hi) / 2
        hi = mid if survives(mid) else hi
        lo = lo if survives(mid) else mid
    return hi


def required_corpus_fd_lockin(monthly_expense_today, years_to_ret, retirement_years):
    annual = monthly_expense_today * 12 * ((1 + INFLATION) ** years_to_ret)

    def survives(C):
        E = annual
        for _ in range(retirement_years):
            C = C * (1 + POST_RET_RETURN) - E
            if C < 0:
                return False
            E *= (1 + INFLATION)
        return True

    lo, hi = 0, 1e11
    for _ in range(100):
        mid = (lo + hi) / 2
        hi = mid if survives(mid) else hi
        lo = lo if survives(mid) else mid
    return hi


# ============================================================
# SIP + SUPPORTING ENGINES (UNCHANGED)
# ============================================================

def required_monthly_sip(required_corpus, current_savings, years, annual_return):
    lo, hi = 0, 300_000
    for _ in range(100):
        mid = (lo + hi) / 2
        C = current_savings
        for _ in range(years):
            C = C * (1 + annual_return) + 12 * mid
        hi = mid if C >= required_corpus else hi
        lo = lo if C >= required_corpus else mid
    return int(hi)


def min_start_sip_for_overshoot(required_sip, years, stepup, overshoot_factor=1.10):
    lo, hi = 0, required_sip
    for _ in range(60):
        mid = (lo + hi) / 2
        sip = mid
        for _ in range(years):
            sip = min(sip * (1 + stepup), required_sip * overshoot_factor)
        hi = mid if sip >= required_sip * overshoot_factor else hi
        lo = lo if sip >= required_sip * overshoot_factor else mid
    return int(hi)


def system_risk_level(current_age, retirement_age, is_behind):
    years = retirement_age - current_age
    base = 4 if years > 25 else 3 if years > 15 else 2
    return min(5, base + 1) if is_behind else base


def blended_risk(user_risk, system_risk):
    return max(1, min(5, round(0.6 * user_risk + 0.4 * system_risk)))


# ============================================================
# INPUTS
# ============================================================
col_inputs, col_info = st.columns([1, 1])

with col_inputs:
    with st.container(border=True):
        current_age = st.number_input(
            "Current age",
            min_value=18,
            max_value=65,
            value=22,
            help="Your age today"
        )
        retirement_age = st.number_input(
            "Planned retirement age",
            min_value=current_age + 1,
            max_value=75,
            value=60,
            help="Age at which you plan to retire"
        )

        monthly_expense = st.number_input(
            "Desired monthly expense after retirement (today’s value)",
            step=1000,
            value=100000,
            help = "Inflated till retirement automatically."
        )

        retirement_style = st.radio(
            "Post-retirement investment strategy",
            [
                "Portfolio Withdrawal (Systematic)",
                "FD Lock-In (Conservative)"
            ],
            help="Determines how your retirement corpus is handled after retirement."
)

        if retirement_style.startswith("Portfolio"):
            st.caption(" Corpus stays invested; withdrawals rise with inflation.")
        else:
            st.caption(" Corpus locked into FD; safer but depletes faster.")




        current_monthly_investment = st.number_input("Current monthly investment", step=1000, value=50000)
        current_savings = st.number_input("Retirement savings accumulated so far", step=50000, value=0)
        st.markdown("---")


        user_risk = st.slider(
            "Risk tolerance",
            min_value=1,
            max_value=5,
            value=3,
            help="Higher risk may mean higher returns, but more volatility"
        )

        risk_labels = {
            1: "Very Conservative",
            2: "Conservative",
            3: "Balanced",
            4: "Growth Oriented",
            5: "Aggressive"
        }

        st.caption(f"Your risk profile: **{risk_labels[user_risk]}**")

        st.markdown("---")

        calculate = st.button("Calculate my retirement plan", use_container_width=True)

# ============================================================
# CALCULATION
# ============================================================
if calculate:
    years_to_ret = retirement_age - current_age
    retirement_years = 90 - retirement_age

    required = (
        required_corpus_portfolio(monthly_expense, years_to_ret, retirement_years, user_risk)
        if retirement_style.startswith("Portfolio")
        else required_corpus_fd_lockin(monthly_expense, years_to_ret, retirement_years)
    )

    progress = max(0.0, min(current_savings / required, 1.0)) if required > 0 else 0.0

    r_user = portfolio_return(user_risk)
    required_sip = required_monthly_sip(required, current_savings, years_to_ret, r_user)

    is_behind = current_monthly_investment < required_sip
    min_start_sip = min_start_sip_for_overshoot(required_sip, years_to_ret, MAX_SIP_GROWTH)
    can_recover = current_monthly_investment >= min_start_sip

    system_risk = system_risk_level(current_age, retirement_age, is_behind)
    final_risk = blended_risk(user_risk, system_risk)

    # ============================================================
    # ASSUMPTIONS + PROGRESS (RESTORED)
    # ============================================================
    with col_info:
        with st.container(border=True):
            st.markdown("### Our Assumptions")
            st.markdown("""
        **Inflation** - 6% per year
                        
        **Post-retirement returns** - Portfolio-based or FD-based (depending on strategy)
                        
        **Life expectancy** - 90 years
                        
        **Asset return assumptions (annual)**
        - Equity: **12%**
        - Debt: **7%**
        - Gold: **6%**
        - Savings / Liquid: **4%**
        """)


        with st.container(border=True):
            st.markdown("### Your retirement journey so far")
            st.markdown(
        f"""
            <div style="
                width: 100%;
                background: #020617;
                border-radius: 999px;
                height: 12px;
                overflow: hidden;
                margin-top: 8px;
            ">
            <div style="
                width: {progress*100:.2f}%;
                background: #10b981;
                height: 100%;
                border-radius: 999px;
                transition: width 0.6s ease;
            "></div>
        </div>
        """,
        unsafe_allow_html=True
    )

            st.caption(f"{progress*100:.1f}% complete")
            st.caption(f"You've saved ₹{current_savings:,} out of ₹{required/1e7:.2f} Cr")

        with st.container(border=True):
            st.markdown("### Your Retirement Requirement")

            st.markdown(
        f"""
        <div style="margin-top: px;">
            <p style="
                margin-bottom: 0px;
                font-size: 0.95rem;
                color: #cbd5e1;
            ">
                Required retirement corpus (Adjusted to inflation)
            </p>
            <h1 style="
                margin: 0;
                font-weight: 800;
                color: #f8fafc;
            ">
                ₹{required/1e7:.2f} Cr
            </h1>
        </div>

        <div style="margin-top: 6px;">
            <p style="
                margin-bottom: 0px;
                font-size: 0.95rem;
                color: #cbd5e1;
            ">
                Required monthly investment
            </p>
            <h2 style="
                margin: 0;
                font-weight: 700;
                color: #f8fafc;
            ">
                ₹{required_sip:,} / month
            </h2>
        </div>
        """,
        unsafe_allow_html=True
    )



            if is_behind:
                if not can_recover:
                    st.error(f"To recover, SIP must start at ₹{min_start_sip:,}/month and grow yearly.")
                else:
                    st.info("Temporary SIP overshoot is required to compensate for lost compounding.")
            else:
                st.success("At your current investment rate, you are on track.")

        # ============================================================
    # SIP PATH (WITH VISIBLE POINTS)
    # ============================================================
        # ============================================================
    # SIP PATH (FIXED: INSIDE EXPANDER + SMALLER POINTS)
    # ============================================================
    years = list(range(1, years_to_ret + 1))
    sip = current_monthly_investment
    cap = 1.10 * required_sip
    catchup = []

    for _ in years:
        catchup.append(int(sip))
        sip = min(sip * (1 + MAX_SIP_GROWTH), cap)

    df = pd.DataFrame({
        "Years till retirement": years,
        "Current SIP": [current_monthly_investment] * years_to_ret,
        "Required SIP": [required_sip] * years_to_ret,
        "Catch-up Path": catchup
    })

    if is_behind and can_recover:
        with st.expander(" How to close the gap (overshoot path)"):

            line_df = df.melt(
                "Years till retirement",
                var_name="Type",
                value_name="Monthly SIP"
            )

            # ---- Lines for ALL paths ----
            lines = alt.Chart(line_df).mark_line(
                strokeWidth=3
            ).encode(
                x="Years till retirement:Q",
                y="Monthly SIP:Q",
                color=alt.Color(
                    "Type:N",
                    scale=alt.Scale(
                        domain=["Catch-up Path", "Current SIP", "Required SIP"],
                        range=["#22c55e", "#38bdf8", "#facc15"]
                    )
                )
            )

            # ---- Points ONLY for Catch-up Path (smaller & clean) ----
            points = alt.Chart(
                line_df[line_df["Type"] == "Catch-up Path"]
            ).mark_circle(
                size=42,                 # ✅ FIXED (was too big)
                filled=True,
                stroke="#020617",
                strokeWidth=1.5
            ).encode(
                x="Years till retirement:Q",
                y="Monthly SIP:Q",
                color=alt.value("#22c55e")
            )

            st.altair_chart(
                (lines + points).properties(height=320),
                use_container_width=True
            )




    # ============================================================
    # INVESTMENT ALLOCATION (UNCHANGED)
    # ==    ==========================================================
        with st.container(border=True):
            st.markdown("### Where your monthly investment goes")
            st.markdown(
            f"""
            **Your risk choice:** {user_risk}  
            **System suggested risk:** {system_risk}  
            **Blended risk used:** {final_risk}
            """
        )

        alloc = RISK_ALLOC[final_risk]
        alloc_df = pd.DataFrame({
            "Asset Class": alloc.keys(),
            "Monthly Amount (₹)": [required_sip * v for v in alloc.values()]
        })

        c1, c2 = st.columns(2)
        with c1:
            pie = alt.Chart(alloc_df).mark_arc(innerRadius=55).encode(
    theta=alt.Theta("Monthly Amount (₹):Q", stack=True),
    color=alt.Color(
        "Asset Class:N",
        scale=alt.Scale(
            range=[
    "#22c55e",  # soft green
    "#3b82f6",  # soft blue
    "#eab308",  # soft amber
    "#94a3b8"   # muted gray
]

        ),
        legend=alt.Legend(title="Asset Class")
    )
)

            st.altair_chart(pie, use_container_width=True)

        with c2:
            st.dataframe(alloc_df, hide_index=True, use_container_width=True)

    with st.container(border=False):
        with st.expander("How your retirement money is used"):
            st.markdown("""
        • **Short-term:** Fixed deposits / liquid funds  
        • **Medium-term:** Debt instruments  
        • **Long-term:** Growth assets  
        """)

with st.container(border=False):
    with st.expander("How to interpret the two retirement models"):
        st.markdown("""
        **Portfolio Withdrawal (Systematic)**  
        • Corpus stays invested across assets  
        • Withdrawals increase every year with inflation  
        • Slower corpus depletion  
        • Reflects modern retirement planning  

        **FD Lock-In (Conservative)**  
        • Entire corpus moved to fixed deposits at retirement  
        • Withdrawals increase with inflation  
        • Faster corpus depletion due to lower returns  
        • Reflects extreme risk aversion  

        Both models ensure the corpus lasts till age 90.
        """)

