import streamlit as st
import pandas as pd
import pickle

st.title("Student Dropout Prediction")

model = pickle.load(open("model.pkl", "rb"))

tuition_paid = st.selectbox("Is tuition fees up to date?", ["Yes", "No"])
first_sem_approved = st.selectbox("Curricular units 1st sem (approved)?", ["Yes", "No"])
first_sem_grade = st.number_input("Curricular units 1st sem (grade)", min_value=0.0, max_value=20.0, step=0.1)
second_sem_approved = st.selectbox("Curricular units 2nd sem (approved)?", ["Yes", "No"])
second_sem_grade = st.number_input("Curricular units 2nd sem (grade)", min_value=0.0, max_value=20.0, step=0.1)

# Convert categorical to numeric
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

    # Show recommendations
    recs = recommend_resources(input_data, prediction)
    if recs:
        st.write("Personalized Recommended Resources:")
        for rec in recs:
            st.markdown(f"- {rec}")


