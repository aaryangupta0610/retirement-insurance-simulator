import streamlit as st

st.markdown("## 🛡 Insurance Simulator")
st.caption("Check whether your insurance coverage is adequate.")

left, right = st.columns([1, 2], gap="large")

with left:
    st.markdown("### 🧾 Inputs")

    income = st.number_input("Annual Income (₹)", 10000)
    life_cover = st.number_input("Existing Life Cover (₹)", 0)

    check = st.button("▶ Check Coverage", use_container_width=True)

with right:
    if check:
        required = income * 10

        st.markdown("### ❤️ Life Insurance")

        c1, c2 = st.columns(2)
        c1.metric("Required Cover", f"₹{required:,.0f}")
        c2.metric("Your Cover", f"₹{life_cover:,.0f}")

        if life_cover < required:
            st.error("Coverage Gap Detected")
            st.write("💡 Consider increasing term insurance cover.")
        else:
            st.success("Coverage Adequate")
    else:
        st.markdown("""
        <div class="card">
        👈 Enter details and click <b>Check Coverage</b>.
        </div>
        """, unsafe_allow_html=True)
