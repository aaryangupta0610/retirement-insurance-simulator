import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# ============================================================
# GLOBAL UI: FONT SCALE (RETIREMENT PAGE ONLY)
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
    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# PAGE HEADER
# ============================================================
st.markdown("## Retirement Simulator")
st.markdown(
    "Understand how much money you’ll need for retirement — "
    "and how much you should invest every month to get there."
)

st.divider()

# ============================================================
# INPUT SECTION
# ============================================================
col_inputs, col_info = st.columns([1, 1])

with col_inputs:
    with st.container(border=True):
        st.markdown("###  Your Details")

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
            "Monthly expense today",
            min_value=0,
            value=30000,
            step=1000,
            help="Your current monthly lifestyle cost"
        )

        post_retirement_expense = st.number_input(
            "Expected monthly expense after retirement",
            min_value=0,
            value=int(monthly_expense * 0.8),
            step=1000,
            help="Inflation will be handled internally"
        )

        # BACKEND: total retirement savings accumulated so far
        current_retirement_savings = st.number_input(
            "Retirement savings accumulated so far",
            min_value=0,
            value=500000,
            step=50000,
            help="Total amount already invested towards retirement (EPF, MF, NPS, etc.)"
        )

        st.caption(
            "Exclude emergency funds or money meant for short-term goals."
        )   


        st.markdown("---")

        risk_factor = st.slider(
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

        st.caption(f"Your risk profile: **{risk_labels[risk_factor]}**")

        st.markdown("---")

        calculate_clicked = st.button(
            "Calculate my retirement plan",
            use_container_width=True,
            type="primary"
        )

# ============================================================
# NOT CALCULATED STATE
# ============================================================
if not calculate_clicked:
    st.info(
        "Enter your details and click **Calculate my retirement plan** "
        "to see your retirement estimate."
    )

# ============================================================
# CALCULATED STATE
# ============================================================
if calculate_clicked:

    # ----------------------------
    # ASSUMPTIONS + PROGRESS
    # ----------------------------
    with col_info:
        with st.container(border=True):
            st.markdown("###  Our Assumptions")

            st.markdown(
                """
                - Inflation: 6% per annum  
                - Equity returns: 11% per annum  
                - Debt returns: 6% per annum  
                - Gold returns: 5% per annum  
                - Savings returns: 3% per annum  
                - Life expectancy assumed: 90 years  

                You don’t need to guess returns — we handle the assumptions.
                """
            )

        with st.container(border=True):
            st.markdown("###  Your retirement journey so far")

            total_corpus_required = 26_000_000
            total_saved_so_far = 1_000_000

            progress_ratio = min(
                total_saved_so_far / total_corpus_required,
                1.0
            )

            st.markdown(
                f"""
                <p style="margin-bottom:6px; color:#a7f3d0;">
                    You’ve saved <b>₹{total_saved_so_far:,}</b> out of
                    <b>₹{total_corpus_required/1e7:.2f} Cr</b> so far
                </p>
                """,
                unsafe_allow_html=True
            )

            st.progress(progress_ratio)

            st.caption(
                "This shows how far you are from your long-term retirement goal."
            )

    st.divider()

    # ============================================================
    # CORE RESULTS
    # ============================================================
    with st.container(border=True):
        st.markdown("###  Your Retirement Requirement")

        required_corpus = 26_000_000
        monthly_investment = 18_000

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("####  Money needed at retirement")
            st.markdown(
                f"<h1 style='color:#34d399;'>₹{required_corpus/1e7:.2f} Cr</h1>",
                unsafe_allow_html=True
            )
            st.caption(
                "Total amount required to maintain your lifestyle after retirement"
            )

        with col2:
            st.markdown("####  Monthly investment needed")
            st.markdown(
                f"<h1 style='color:#34d399;'>₹{monthly_investment:,}</h1>",
                unsafe_allow_html=True
            )
            st.caption(
                "Amount you should invest every month to reach the goal"
            )

    # ============================================================
    # INVESTMENT ALLOCATION
    # ============================================================
    with st.container(border=True):
        st.markdown("###  Where your monthly investment goes")

        allocation = {
            "Equity": 50,
            "Debt": 25,
            "Gold": 15,
            "Savings": 10
        }

        alloc_df = pd.DataFrame({
            "Asset Class": allocation.keys(),
            "Monthly Amount (₹)": [
                monthly_investment * v / 100 for v in allocation.values()
            ]
        })

        col1, col2 = st.columns([1, 1])

        with col1:
            pie = alt.Chart(alloc_df).mark_arc(innerRadius=50).encode(
                theta="Monthly Amount (₹):Q",
                color="Asset Class:N",
                tooltip=["Asset Class", "Monthly Amount (₹)"]
            ).properties(height=300)

            st.altair_chart(pie, use_container_width=True)

        with col2:
            st.markdown(
                """
                **What this means in simple terms:**

                - Equity helps long-term growth  
                - Debt and savings reduce risk  
                - Gold protects against uncertainty  

                This balance keeps your plan stable and realistic.
                """
            )

            st.dataframe(
                alloc_df,
                hide_index=True,
                use_container_width=True
            )

    # ============================================================
    # GROWTH GRAPH
    # ============================================================
    with st.container(border=True):
        st.markdown("###  Your journey to retirement")

        ages = list(range(current_age, retirement_age + 1))
        savings = np.linspace(0, required_corpus, len(ages))

        df = pd.DataFrame({
            "Age": ages,
            "Projected Savings": savings
        })

        st.line_chart(df.set_index("Age"), use_container_width=True)

    st.divider()

    # ============================================================
    # FINAL TAKEAWAY
    # ============================================================
    with st.container(border=True):
        st.markdown("###  Simple takeaway")

        st.markdown(
            f"""
            - Your current lifestyle costs **₹{monthly_expense:,}/month**  
            - You may need around **₹{required_corpus/1e7:.2f} Cr** at retirement  
            - Investing **₹{monthly_investment:,}/month** consistently can help reach this goal  

            Starting early matters more than timing the market.
            """
        )
