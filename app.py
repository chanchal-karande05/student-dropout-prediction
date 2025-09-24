import streamlit as st
import pandas as pd
import pickle

st.title("Student Dropout Prediction")

model = pickle.load(open("model.pkl", "rb"))

resources = {
    'academic': ['https://swayam.gov.in/', 'https://nptel.ac.in/'],
    'financial': ['https://scholarships.gov.in/', 'https://buddy4study.com/']
}

def recommend_resources(features, prediction):
    recs = []
    if prediction == 1:
        if features.loc[0, 'Tuition fees up to date'] == 0:
            recs.append(f"Financial Aid: {resources['financial'][0]}")

        if features.loc[0, 'Curricular units 1st sem (grade)'] < 50 or \
           features.loc[0, 'Curricular units 2nd sem (grade)'] < 50:
            recs.append(f"Academic Support: {resources['academic'][0]}")

    return recs

tuition_paid = st.selectbox("Is tuition fees up to date?", ["Yes", "No"])
first_sem_approved = st.selectbox("Curricular units 1st sem (approved)?", ["Yes", "No"])
first_sem_grade = st.number_input("Curricular units 1st sem (grade)", min_value=0.0, max_value=100.0, step=0.1)

if first_sem_approved == "No":
    st.warning("First semester not approved, so second semester approval is set to 'No'.")
    second_sem_approved = "No"
    st.write("Curricular units 2nd sem (approved)? No")
else:
    second_sem_approved = st.selectbox("Curricular units 2nd sem (approved)?", ["Yes", "No"])

second_sem_grade = st.number_input("Curricular units 2nd sem (grade)", min_value=0.0, max_value=100.0, step=0.1)

tuition_val = 1 if tuition_paid == "Yes" else 0
first_sem_approved_val = 1 if first_sem_approved == "Yes" else 0
second_sem_approved_val = 1 if second_sem_approved == "Yes" else 0

input_data = pd.DataFrame([[
    tuition_val,
    first_sem_approved_val,
    first_sem_grade,
    second_sem_approved_val,
    second_sem_grade
]], columns=[
    'Tuition fees up to date',
    'Curricular units 1st sem (approved)',
    'Curricular units 1st sem (grade)',
    'Curricular units 2nd sem (approved)',
    'Curricular units 2nd sem (grade)'
])

if st.button("Predict Dropout"):
    prediction = model.predict(input_data)[0]
    if prediction == 0:
        st.success("Student is unlikely to drop out.")
    else:
        st.error("Student is likely to drop out.")

    recs = recommend_resources(input_data, prediction)
    if recs:
        st.write("Personalized Recommended Resources:")
        for rec in recs:
            st.markdown(f"- {rec}")
