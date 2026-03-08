import streamlit as st
import pickle
import numpy as np

with open("resume.pkl", "rb") as f:
    model = pickle.load(f)
with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)


st.set_page_config(page_title="Resume Shortlisting App")
st.title("📄 Resume Shortlisting System")
st.write("This system predicts whether a resume will be shortlisted or not.")

education_dict = {
    "High School": 0,
    "Bachelors": 1,
    "Masters": 2,
    "PhD": 3
}

education_label = st.selectbox(
    "Education Level",
    options=list(education_dict.keys())
)

education_level = education_dict[education_label] 

years_experience = st.number_input("years_experience")
skills_match_score = st.number_input("skills_match_score")
project_count = st.number_input("project_count")
resume_length = st.number_input("resume_length")
github_activity = st.number_input("github_activity")

if st.button("Predict Default Risk"):
    input_data = np.array([[years_experience,skills_match_score,education_level,project_count,resume_length,github_activity]])

    # Scale input
    input_scaled = scaler.transform(input_data)

    # Prediction
    prediction = model.predict(input_scaled)[0]

    st.subheader("Prediction Result")

    if prediction == 1:
        st.success("✅ Resume Shortlisted")
    else:
        st.error("❌ Resume Not Shortlisted")