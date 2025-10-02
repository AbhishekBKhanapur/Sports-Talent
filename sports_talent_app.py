import streamlit as st
from situp_module import situp_live
from vertical_jump_module import jump_live
from shuttle_run_module import shuttle_live

st.set_page_config(page_title="Sports Talent Assessment", page_icon="🏆", layout="centered")

st.title("🏅 AI-Powered Sports Talent Assessment")
# User Info Section
st.subheader("👤 Enter Your Details")
name = st.text_input("Name")
age = st.number_input("Age", min_value=10, max_value=60, value=18)
gender = st.selectbox("Gender", ["male", "female"])

st.write("Select a test below to start:")

choice = st.radio("📌 Choose a Fitness Test:", ["Sit-ups", "Vertical Jump", "Shuttle Run"])

if choice == "Sit-ups":
    if st.button("▶ Start Sit-up Test"):
        count = situp_live()
        st.success(f"✅ Total Sit-ups: {count}")

elif choice == "Vertical Jump":
    if st.button("▶ Start Vertical Jump Test"):
        max_jump = jump_live()
        st.success(f"✅ Max Jump Height: {max_jump:.2f}")

elif choice == "Shuttle Run":
    if st.button("▶ Start Shuttle Run Test"):
        laps, elapsed = shuttle_live()
        st.success(f"✅ Laps: {laps} | Time: {elapsed:.1f} sec")
