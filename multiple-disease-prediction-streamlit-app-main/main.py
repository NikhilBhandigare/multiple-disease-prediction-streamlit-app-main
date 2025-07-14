import os
import sqlite3
import hashlib
import pickle
import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai
import re
from fpdf import FPDF
from io import BytesIO
# ---------------------- CONFIG & SETUP ---------------------- #
st.set_page_config("Health Assistant", layout="wide", page_icon="📈")

# Show logo or banner
# Disease Prediction App Header
st.markdown("<h1 style='text-align:center;'>🔬 Disease Prediction System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Predict Diabetes, Heart Disease, and Parkinson's using ML and recommended medicines,exercise, diet using ai</p>", unsafe_allow_html=True)


# ---------------------- GEMINI SETUP ---------------------- #
genai.configure(api_key=os.getenv("GOOGLE_API_KEY") or "AIzaSyAMbLh4EqrMAR6Yo6i-wnNVdVh3cJjEYqM")
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

# ---------------------- DATABASE SETUP ---------------------- #
def create_connection(db_file):
    try:
        return sqlite3.connect(db_file, check_same_thread=False)
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
        return None

def create_patient_table(conn):
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        gender TEXT,
        phone TEXT,
        password TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY,
        email TEXT,
        disease TEXT,
        result TEXT)''')
    conn.commit()

# ---------------------- UTILS ---------------------- #
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)

def add_patient(conn, name, email, gender, phone, password):
    try:
        conn.cursor().execute("INSERT INTO patients (name, email, gender, phone, password) VALUES (?, ?, ?, ?, ?)",
            (name, email, gender, phone, hash_password(password)))
        conn.commit()
        st.success("✅ Patient added successfully.")

        return True
    except sqlite3.IntegrityError:
        st.error("❌ Email already exists.")
        return False

def get_all_patients(conn):
    return pd.read_sql("SELECT id, name, email, gender, phone FROM patients", conn)

def get_disease_distribution(conn):
    return pd.read_sql("SELECT disease, COUNT(*) as count FROM predictions GROUP BY disease", conn)

def verify_user(conn, email, password):
    if email == "admin@gmail.com" and password == "admin":
        return "admin"
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE email=? AND password=?",
        (email, hash_password(password)))
    return "user" if cursor.fetchone() else None

def save_prediction(conn, email, disease, result):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO predictions (email, disease, result) VALUES (?, ?, ?)",
                   (email, disease, result))
    conn.commit()

def delete_patient(conn, patient_id):
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM patients WHERE id=?", (patient_id,))
    row = cursor.fetchone()
    if row:
        email = row[0]
        cursor.execute("DELETE FROM predictions WHERE email=?", (email,))
        cursor.execute("DELETE FROM patients WHERE id=?", (patient_id,))
        conn.commit()

def update_patient(conn, patient_id, name, email, gender, phone):
    cursor = conn.cursor()
    cursor.execute("UPDATE patients SET name=?, email=?, gender=?, phone=? WHERE id=?",
                   (name, email, gender, phone, patient_id))
    conn.commit()

def clear_all_data(conn):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM predictions")
    cursor.execute("DELETE FROM patients")
    conn.commit()

# ---------------------- LOAD MODELS ---------------------- #
working_dir = os.path.dirname(os.path.abspath(__file__))
diabetes_model = pickle.load(open(f"{working_dir}/saved_models/diabetes_model.sav", 'rb'))
heart_model = pickle.load(open(f"{working_dir}/saved_models/heart_disease_model.sav", 'rb'))
parkinsons_model = pickle.load(open(f"{working_dir}/saved_models/parkinsons_model.sav", 'rb'))

# ---------------------- GEMINI FUNCTION ---------------------- #
def ai_recommendation(email, disease, result, inputs):
    prompt = f"""
Patient Email: {email}
Disease: {disease}
Prediction Result: {result}
Parameters: {inputs}

Give short, real, and actionable recommendations with no disclaimers:
1. List 2-3 example generic medicines often prescribed for {disease}
2. Give a short, 2-line exercise suggestion tailored for this condition
3. Give a short Indian diet tip specific to {disease}
"""
    try:
        response = gemini_model.generate_content(prompt)
        return f"""
**🎒 Recommended Medicines:**
{response.text.split('2.')[0].strip().replace('1.', '').strip()}

**🏋️ Exercise Suggestion:**
{response.text.split('2.')[1].split('3.')[0].strip()}

**🍜 Indian Diet Tip:**
{response.text.split('3.')[1].strip()}
"""
    except Exception as e:
        return f"Gemini Error: {e}"

def remove_emojis(text):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags
        u"\U00002500-\U00002BEF"  # Chinese characters
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub('', text)

def generate_pdf(email, disease, inputs, result, recommendations):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.set_title("Disease Prediction Report")
    pdf.cell(200, 10, txt="Disease Prediction Report", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Patient Email: {email}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", 'B', size=12)
    pdf.cell(200, 10, txt="Entered Parameters:", ln=True)
    pdf.set_font("Arial", size=12)
    for key, val in inputs.items():
        pdf.cell(200, 8, txt=f"{key}: {val}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", 'B', size=12)
    pdf.cell(200, 10, txt=f"Prediction Result: {result}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", 'B', size=12)
    pdf.cell(200, 10, txt="Recommendations:", ln=True)
    pdf.set_font("Arial", size=12)

    clean_text = remove_emojis(recommendations)
    for line in clean_text.split('\n'):
        pdf.multi_cell(0, 8, txt=line)

    pdf_output = pdf.output(dest='S').encode('latin1')
    return BytesIO(pdf_output)
# ---------------------- UI FUNCTIONS ---------------------- #
def add_patient_ui(conn):
    st.header("➕ Add New Patient")
    name = st.text_input("Name")
    email = st.text_input("Email")
    gender = st.selectbox("Gender", ["Select", "Male", "Female", "Other"])
    phone = st.text_input("Mobile")
    password = st.text_input("Password", type="password")

    if st.button("➕ Add Patient"):
        if not name.strip():
            st.error("Name is required.")
        elif not email.strip():
            st.error("Email is required.")
        elif not is_valid_email(email):
            st.error("Invalid email format.")
        elif gender == "Select":
            st.error("Please select a valid gender.")
        elif not phone.strip():
            st.error("Mobile number is required.")
        elif not password:
            st.error("Password is required.")
        else:
            add_patient(conn, name, email, gender, phone, password)

def view_patients_ui(conn):
    st.header("👥 All Patients")
    df = get_all_patients(conn)
    if df.empty:
        st.info("No patients found.")
        return
    for idx, row in df.iterrows():
        with st.expander(f"{row['name']} ({row['email']})"):
            new_name = st.text_input("Name", value=row["name"], key=f"name_{row['id']}_{idx}")
            new_email = st.text_input("Email", value=row["email"], key=f"email_{row['id']}_{idx}")
            new_gender = st.selectbox("Gender", ["Male", "Female", "Other"],
                                      index=["Male", "Female", "Other"].index(row["gender"]),
                                      key=f"gender_{row['id']}_{idx}")
            new_phone = st.text_input("Phone", value=row["phone"], key=f"phone_{row['id']}_{idx}")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Update", key=f"update_{row['id']}_{idx}"):
                    update_patient(conn, row["id"], new_name, new_email, new_gender, new_phone)
                    st.success("Updated successfully.")
                    st.rerun()
            with col2:
                if st.button("🗑️ Delete", key=f"delete_{row['id']}_{idx}"):
                    delete_patient(conn, row["id"])
                    st.warning("Deleted successfully.")
                    st.rerun()

def predict_disease(conn):
    st.header("🔬 Disease Prediction")
    st.image("prediction_banner.png", use_column_width=True)
    email = st.session_state.get("user_email", "admin@gmail.com")
    disease = st.selectbox("Select Disease", ["Diabetes", "Heart Disease", "Parkinson's"])
    result = None
    inputs = {}

def predict_disease(conn):
    st.header("Disease Prediction")
    email = st.session_state.get("user_email", "admin@gmail.com")
    disease = st.selectbox("Select Disease", ["Diabetes", "Heart Disease", "Parkinson's"])
    result = None
    inputs = {}

    if disease == "Diabetes":
        st.subheader("Enter Diabetes Parameters")
        cols = st.columns(3)
        inputs = {
            'Pregnancies': cols[0].number_input('Pregnancies', min_value=0),
            'Glucose': cols[1].number_input('Glucose', min_value=0),
            'BloodPressure': cols[2].number_input('Blood Pressure', min_value=0),
            'SkinThickness': cols[0].number_input('Skin Thickness', min_value=0),
            'Insulin': cols[1].number_input('Insulin', min_value=0),
            'BMI': cols[2].number_input('BMI', min_value=0.0)
        }
        if st.button("Predict"):
            val = list(inputs.values())
            pred = diabetes_model.predict([val])[0]
            result = "Diabetic" if pred == 1 else "Non-Diabetic"
            st.success(f"Prediction: {result}")

            
    elif disease == "Heart Disease":
        st.subheader("Enter Heart Parameters")
        cols = st.columns(3)
        inputs = {
            'Sex': cols[0].selectbox("Sex", [0, 1]),
            'Chest Pain': cols[1].selectbox("Chest Pain Type", [0, 1, 2, 3]),
            'RestBP': cols[2].number_input("Resting BP"),
            'Chol': cols[0].number_input("Cholesterol"),
            'FBS': cols[1].selectbox("Fasting Sugar > 120?", [0, 1]),
            'ECG': cols[2].selectbox("ECG", [0, 1, 2]),
            'MaxHR': cols[0].number_input("Max Heart Rate"),
            'Angina': cols[1].selectbox("Exercise Angina", [0, 1]),
            'Oldpeak': cols[2].number_input("Oldpeak"),
            'Slope': cols[0].selectbox("Slope", [0, 1, 2]),
            'CA': cols[1].selectbox("CA", [0, 1, 2, 3, 4]),
            'Thal': cols[2].selectbox("Thal", [0, 1, 2, 3])
        }
        if st.button("Predict"):
            val = list(inputs.values())
            pred = heart_model.predict([val])[0]
            result = "Heart Disease" if pred == 1 else "No Heart Disease"
            st.success(f"Prediction: {result}")

    elif disease == "Parkinson's":
        st.subheader("Enter Parkinson's Parameters")
        labels = ["Fo", "Fhi", "Flo", "Jitter %", "Jitter Abs", "RAP", "PPQ", "DDP",
                  "Shimmer", "Shimmer dB", "APQ3", "APQ5", "APQ", "DDA", "NHR", "HNR",
                  "RPDE", "DFA", "Spread1", "Spread2", "D2", "PPE"]
        cols = st.columns(3)
        for i, label in enumerate(labels):
            inputs[label] = cols[i % 3].number_input(label)
        if st.button("Predict"):
            val = list(inputs.values())
            pred = parkinsons_model.predict([val])[0]
            result = "Parkinson's" if pred == 1 else "No Parkinson's"
            st.success(f"Prediction: {result}")

    if result and "No" not in result:
        save_prediction(conn, email, disease, result)
        st.subheader("AI-Powered Recommendations")
    
        with st.spinner("Generating personalized recommendations..."):
            recommendations = ai_recommendation(email, disease, result, inputs)

        st.markdown(recommendations)

        pdf_buffer = generate_pdf(email, disease, inputs, result, recommendations)
        st.download_button("📄 Download Report", data=pdf_buffer, file_name="prediction_report.pdf", mime="application/pdf")

def show_disease_distribution(conn):
    st.header("Disease Distribution")
    df = get_disease_distribution(conn)
    if not df.empty:
        fig = px.pie(df, names='disease', values='count', title='Prediction Count by Disease')
        st.plotly_chart(fig)
    else:
        st.info("No prediction data available.")

# ---------------------- MAIN FLOW ---------------------- #
conn = create_connection("patients.db")
create_patient_table(conn)

if 'user_role' not in st.session_state:
    st.session_state.user_role = None

if st.session_state.user_role is None:
    st.subheader("🔐 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if not email.strip():
            st.error("Email is required.")
        elif not is_valid_email(email):
            st.error("Please enter a valid email address.")
        elif not password:
            st.error("Password is required.")
        else:
            role = verify_user(conn, email, password)
            if role == "admin":
                st.session_state.user_role = "admin"
                st.toast("Admin logged in successfully!", icon="✅")
                st.rerun()
            elif role == "user":
                st.session_state.user_role = "user"
                st.session_state.user_email = email
                st.toast("User logged in successfully!", icon="✅")
                st.rerun()
            else:
                st.error("Invalid email or password.")

elif st.session_state.user_role == "admin":
    option = st.sidebar.selectbox("🛠️ Admin Options", [
        "➕ Add Patient", "👥 View Patients", "🔬 Predict Disease", "📊 Visualize Data", "🗑️ Clear All Data"])
    with st.sidebar.expander("🚪 Logout", expanded=False):
        if st.checkbox("Are you sure you want to logout?"):
            if st.button("✅ Confirm Logout"):
                st.session_state.user_role = None
                st.session_state.user_email = None
                st.toast("Logged out successfully.", icon="👋")
                st.rerun()

    if option == "➕ Add Patient":
        add_patient_ui(conn)
    elif option == "👥 View Patients":
        view_patients_ui(conn)
    elif option == "🔬 Predict Disease":
        predict_disease(conn)
    elif option == "📊 Visualize Data":
        show_disease_distribution(conn)
    elif option == "🗑️ Clear All Data":
        with st.expander("⚠️ Confirm Clear All Data", expanded=False):
            confirm_clear = st.checkbox("Yes, I want to clear all patient and prediction data.")
            if confirm_clear and st.button("🧹 Clear Now"):
                clear_all_data(conn)
                st.success("All data cleared.")
                st.rerun()


elif st.session_state.user_role == "user":
    with st.sidebar.expander("🚪 Logout", expanded=False):
        if st.checkbox("Are you sure you want to logout?"):
            if st.button("✅ Confirm Logout"):
                st.session_state.user_role = None
                st.session_state.user_email = None
                st.toast("Logged out successfully.", icon="👋")
                st.rerun()

    predict_disease(conn)

# if st.sidebar.button("🚪 Logout"):
#     st.session_state.user_role = None
#     st.session_state.user_email = None
#     st.toast("Logged out successfully.", icon="👋")
#     st.rerun()
