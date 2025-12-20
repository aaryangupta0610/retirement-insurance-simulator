import streamlit as st
import pandas as pd
import altair as alt

# ============================================================
# GLOBAL UI: FONT SCALE + BLUE ACCENTS
# ============================================================
st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        font-size: 17px;
    }

    h1 { font-size: 2.4rem; }
    h2 { font-size: 1.9rem; }
    h3 { font-size: 1.5rem; }
    h4 { font-size: 1.2rem; }

    label, .stCaption, .stMarkdown {
        font-size: 1.05rem;
    }

    input, textarea {
        font-size: 1.05rem !important;
    }

    /* BLUE PRIMARY BUTTON */
    div.stButton > button {
        background-color: #3b82f6;
        color: white;
        border-radius: 8px;
        height: 3rem;
        font-size: 1.05rem;
    }

    /* BLUE MULTISELECT TAGS */
    span[data-baseweb="tag"] {
        background-color: #3b82f6 !important;
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# PAGE HEADER
# ============================================================
st.markdown("## Insurance Adequacy Checker")
st.markdown(
    "Check whether your life and health insurance coverage is sufficient "
    "based on your income, responsibilities, and lifestyle."
)

st.divider()

# ============================================================
# INPUTS + ASSUMPTIONS (SIDE BY SIDE)
# ============================================================
col_inputs, col_right = st.columns([1.2, 1])

with col_inputs:
    with st.container(border=True):
        st.markdown("###  Your Details")

        age = st.number_input(
            "Age", 18, 70, 22,
            help="Your current age helps estimate risk duration"
        )

        income = st.number_input(
            "Annual income (₹)", 0, value=600000, step=50000,
            help="Used to estimate life insurance needs"
        )

        dependants = st.number_input(
            "Number of dependants", 0, 10, 2,
            help="People financially dependent on you"
        )

        life_cover = st.number_input(
            "Existing life insurance cover (₹)", 0, value=0, step=100000,
            help="Total life insurance across all policies"
        )

        health_cover = st.number_input(
            "Existing health insurance cover (₹)", 0, value=0, step=50000,
            help="Total health cover for you / family"
        )

        city = st.selectbox(
            "City tier", ["Tier 1", "Tier 2", "Tier 3"],
            help="Healthcare costs vary by city type"
        )

        lifestyle = st.multiselect(
            "Lifestyle habits (optional)",
            ["Smoking", "High stress lifestyle", "Sedentary routine"],
            help="Certain habits increase long-term health risks"
        )

        st.markdown("---")

        check_clicked = st.button(
            "Check my insurance adequacy",
            use_container_width=True,
            type="primary"
        )

with col_right:
    with st.container(border=True):
        st.markdown("###  Assumptions used")
        st.markdown(
            """
            - Life insurance assumed as **10× annual income**  
            - Health insurance varies by **city tier**  
            - Lifestyle risks slightly increase health cover  
            - This tool is for **awareness**, not advice  
            """
        )

# ============================================================
# NOT CALCULATED STATE
# ============================================================
if not check_clicked:
    st.info(
        "Enter your details and click **Check my insurance adequacy** "
        "to see your coverage status."
    )

# ============================================================
# RESULTS
# ============================================================
if check_clicked:

    # ----------------------------
    # DUMMY LOGIC
    # ----------------------------
    required_life = income * 10
    required_health = 1_000_000

    if city == "Tier 1":
        required_health = 1_500_000
    elif city == "Tier 2":
        required_health = 1_200_000

    if len(lifestyle) >= 2:
        required_health += 300_000

    life_gap = required_life - life_cover
    health_gap = required_health - health_cover

    st.divider()

    # ============================================================
    # SUMMARY CARDS (RIGHT SIDE)
    # ============================================================
    with col_right:

        with st.container(border=True):
            color = "#34d399" if life_gap <= 0 else "#f87171"
            status = "Adequate" if life_gap <= 0 else "Underinsured"

            st.markdown(
                f"""
                <h4>🛡️ Life Insurance</h4>
                <p style="color:{color}; font-weight:600; margin:4px 0;">
                    {status}
                </p>
                <h2 style="color:{color}; margin:0;">
                    ₹{max(life_gap, 0):,}
                </h2>
                <p class="stCaption">Insurance gap</p>
                """,
                unsafe_allow_html=True
            )

        with st.container(border=True):
            color = "#34d399" if health_gap <= 0 else "#f87171"
            status = "Adequate" if health_gap <= 0 else "Needs attention"

            st.markdown(
                f"""
                <h4>🏥 Health Insurance</h4>
                <p style="color:{color}; font-weight:600; margin:4px 0;">
                    {status}
                </p>
                <h2 style="color:{color}; margin:0;">
                    ₹{max(health_gap, 0):,}
                </h2>
                <p class="stCaption">Insurance gap</p>
                """,
                unsafe_allow_html=True
            )

    # ============================================================
    # HEALTH INSURANCE DETAILS + CHART
    # ============================================================
    col_h_text, col_h_chart = st.columns([1.3, 1])

    current_health_text = (
        f"₹{health_cover:,}" if health_cover > 0 else "Not declared"
    )

    with col_h_text:
        with st.container(border=True):
            st.markdown("###  Health Insurance Coverage")
            st.markdown(
                f"""
                - Required cover: **₹{required_health:,}**  
                - Your current cover: **{current_health_text}**

                <p class="stCaption">
                Consider increasing your health cover to avoid medical expense shocks.
                </p>
                """,
                unsafe_allow_html=True
            )

    with col_h_chart:
        df = pd.DataFrame({
            "Type": ["Current", "Required"],
            "Amount": [health_cover, required_health]
        })

        st.altair_chart(
            alt.Chart(df).mark_bar().encode(
                x=alt.X("Type", axis=alt.Axis(labelAngle=0)),
                y="Amount",
                color="Type"
            ).properties(title="Health Insurance Cover"),
            use_container_width=True
        )

    # ============================================================
    # LIFE INSURANCE DETAILS + CHART
    # ============================================================
    col_l_text, col_l_chart = st.columns([1.3, 1])

    current_life_text = (
        f"₹{life_cover:,}" if life_cover > 0 else "Not declared"
    )

    with col_l_text:
        with st.container(border=True):
            st.markdown("###  Life Insurance Coverage")
            st.markdown(
                f"""
                - Required cover: **₹{required_life:,}**  
                - Your current cover: **{current_life_text}**

                <p class="stCaption">
                This gap indicates how much income protection your family may lack.
                </p>
                """,
                unsafe_allow_html=True
            )

    with col_l_chart:
        df = pd.DataFrame({
            "Type": ["Current", "Required"],
            "Amount": [life_cover, required_life]
        })

        st.altair_chart(
            alt.Chart(df).mark_bar().encode(
                x=alt.X("Type", axis=alt.Axis(labelAngle=0)),
                y="Amount",
                color="Type"
            ).properties(title="Life Insurance Cover"),
            use_container_width=True
        )
