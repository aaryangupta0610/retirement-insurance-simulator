import streamlit as st
import pandas as pd
import altair as alt
from insurance_inputs import InsuranceInputs
from life_insurance import calculate_required_life_cover
from health_insurance import calculate_required_health_cover
from premium_estimator import estimate_life_premium, estimate_health_premium


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
        st.markdown("### Assumptions Used")

        # Layer 1: Short, user-friendly summary
        st.caption(
            "Estimates are based on income, age, family size, and city-level healthcare costs. "
            "Premiums shown are indicative yearly ranges."
        )

        # Layer 2: Simple explanation
        with st.expander("How did we calculate this?"):
            st.markdown("""
- Life insurance is estimated using income replacement and dependents.
- Health insurance is adjusted for age, family size, and city healthcare costs.
- Existing insurance is fully considered before identifying gaps.
- Lifestyle inputs, if provided, add optional safety buffers.
- Premiums are approximate and meant for affordability awareness.
""")

        # Layer 3: Technical assumptions
        with st.expander("Technical Assumptions (Detailed)"):
            st.text("""
LIFE INSURANCE ASSUMPTIONS
• Life insurance need is calculated using an income replacement approach.
• Recommended cover is based on annual income and number of dependents.
• Income multipliers used:
  – 0 dependents: 10× annual income
  – 1–2 dependents: 12× annual income
  – 3 or more dependents: 15× annual income
• Existing life insurance is fully deducted before calculating any gap.

HEALTH INSURANCE ASSUMPTIONS
• Health insurance need increases with age due to rising medical risk.
• Base health cover by age:
  – Below 30 years: ₹5,00,000
  – 30–45 years: ₹10,00,000
  – Above 45 years: ₹15,00,000
• Additional family buffer of ₹2,50,000 is added per dependent.
• City-level healthcare cost adjustment:
  – Tier-1 (Metro): +₹5,00,000
  – Tier-2: +₹2,50,000
  – Tier-3 / Rural: +₹0

LIFESTYLE RISK ASSUMPTIONS (OPTIONAL)
• Lifestyle inputs are optional and self-declared.
• Only high-level risk indicators are used.
• Risk buffers applied:
  – Smoking: +₹5,00,000
  – Sedentary lifestyle: +₹2,50,000
  – High stress: +₹2,50,000
• No medical diagnosis or health profiling is performed.

INSURANCE GAP LOGIC
• Insurance gap = Required cover − Existing cover.
• If gap ≤ 0, coverage is marked as Adequate.
• If gap > 0, coverage is marked as Underinsured.

PREMIUM ESTIMATION ASSUMPTIONS
• Premiums shown are indicative yearly ranges, not policy quotes.
• Life insurance premium rates (per ₹10L cover per year):
  – Below 30 years: ₹500 – ₹800
  – 30–45 years: ₹800 – ₹1,200
  – Above 45 years: ₹1,500 – ₹2,500
• Health insurance premium rates (per ₹10L cover per year):
  – Below 30 years: ₹6,000 – ₹8,000
  – 30–45 years: ₹8,000 – ₹12,000
  – Above 45 years: ₹15,000 – ₹25,000
• Premiums are calculated only on the uncovered gap.

DISCLAIMER
• This tool is for educational and planning purposes only.
• Actual insurance needs and premiums may vary by insurer and individual profile.
""")


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
    # DUMMY LOGIC (Now integrated to actual logic)
    # ----------------------------
    inputs = InsuranceInputs(
        age=age,
        annual_income=income,
        dependents=dependants,
        existing_life_cover=life_cover,
        existing_health_cover=health_cover,
        city_tier=city.replace(" ", "_"),
        lifestyle_risks=[risk.lower().replace(" ", "_") for risk in lifestyle]
    )

    required_life = calculate_required_life_cover(inputs)
    required_health = calculate_required_health_cover(inputs)

    life_gap = required_life - life_cover
    health_gap = required_health - health_cover

    

    # ============================================================
    # SUMMARY CARDS (RIGHT SIDE)
    # ============================================================
    with col_right:

        with st.container(border=True):
            color = "#34d399" if life_gap <= 0 else "#f87171"
            status = "Adequate" if life_gap <= 0 else "Underinsured"

            st.markdown(
                f"""
                <h4> Life Insurance</h4>
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

    # ============================================================
    # PREMIUM ESTIMATOR (BOTTOM SECTION)
    # ============================================================

    st.divider()

    st.markdown(
        "## Estimated Cost to Improve Your Coverage"
    )

    with st.container(border=True):

        st.caption(
            "These are indicative costs based on your uncovered insurance gaps. "
            "They help you understand affordability — not policy pricing."
        )

        # ----------------------------
        # LIFE INSURANCE PREMIUM
        # ----------------------------
        if life_gap > 0:
            life_low, life_high = estimate_life_premium(life_gap, age)

            col_lp1, col_lp2 = st.columns(2)

            with col_lp1:
                st.markdown("### Life Insurance")
                st.metric(
                    "Estimated yearly cost",
                    f"₹{life_low:,} – ₹{life_high:,}"
                )

            with col_lp2:
                st.markdown("### Monthly equivalent")
                st.metric(
                    "Approx. per month",
                    f"₹{round(life_high / 12):,}"
                )

        else:
            st.success("✅ Your life insurance coverage appears adequate.")

        st.markdown("<br>", unsafe_allow_html=True)

        # ----------------------------
        # HEALTH INSURANCE PREMIUM
        # ----------------------------
        if health_gap > 0:
            health_low, health_high = estimate_health_premium(health_gap, age)

            col_hp1, col_hp2 = st.columns(2)

            with col_hp1:
                st.markdown("### Health Insurance")
                st.metric(
                    "Estimated yearly cost",
                    f"₹{health_low:,} – ₹{health_high:,}"
                )

            with col_hp2:
                st.markdown("### Monthly equivalent")
                st.metric(
                    "Approx. per month",
                    f"₹{round(health_high / 12):,}"
                )

        else:
            st.success("Your health insurance coverage appears adequate.")

        st.markdown("<br>", unsafe_allow_html=True)

        st.caption(
            "Premiums shown are approximate yearly ranges. "
            "Actual premiums depend on insurer, policy features, and underwriting."
        )

    # ============================================================
    # FINAL INSIGHTS (OVERALL SUMMARY)
    # ============================================================

    st.divider()

    st.markdown("## Final Insights")

    with st.container(border=True):

        # CASE 1: Fully protected
        if life_gap <= 0 and health_gap <= 0:
            st.success(
                "You appear to be well protected across both life and health insurance."
            )

            st.markdown("""
- Your current insurance coverage aligns well with your financial responsibilities.
- No immediate action is required.
- Periodically reassess your coverage as income, family size, or lifestyle changes.
""")

        # CASE 2: Life gap only
        elif life_gap > 0 and health_gap <= 0:
            st.warning(
                "Your health insurance is adequate, but your life insurance may be insufficient."
            )

            st.markdown(f"""
- Your family may face income protection risk if something happens to you.
- Estimated uncovered life insurance gap: **₹{life_gap:,}**
- Consider strengthening life cover gradually based on affordability.
""")

        # CASE 3: Health gap only
        elif life_gap <= 0 and health_gap > 0:
            st.warning(
                "Your life insurance is adequate, but your health insurance may need attention."
            )

            st.markdown(f"""
- Medical expenses can be unpredictable and financially stressful.
- Estimated uncovered health insurance gap: **₹{health_gap:,}**
- Increasing health cover can reduce out-of-pocket medical risk.
""")

        # CASE 4: Both gaps exist
        else:
            st.error(
                "You may be underinsured across both life and health coverage."
            )

            st.markdown(f"""
- Life insurance gap: **₹{life_gap:,}**
- Health insurance gap: **₹{health_gap:,}**
- Addressing these gaps early can significantly improve financial resilience.
- Even small, gradual improvements can make a meaningful difference.
""")

        st.markdown("<br>", unsafe_allow_html=True)

        st.caption(
            "This summary is based on the information provided and uses simplified assumptions. "
            "It is meant to guide awareness, not replace professional advice."
        )
