import os
import sqlite3
import streamlit as st
import subprocess
import re
import pandas as pd
import plotly.express as px

# Function to create a database connection
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        st.error(f"Error: {e}")
    return conn

# Function to create patient table
def create_patient_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                address TEXT,
                disease TEXT
            )
        ''')
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"Error: {e}")

# Function to add a new patient
def add_patient(conn, name, email, phone, address, disease):
    if not any(char.isalpha() for char in name):
        st.error("Please enter a name with at least one alphabet character.")
        return False
    # Check if any of the input fields are empty
    if not name or not email or not phone or not address or not disease:
        st.error("All fields are required. Please fill in all the information.")
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO patients (name, email, phone, address, disease) VALUES (?, ?, ?, ?, ?)
        ''', (name, email, phone, address, disease))
        conn.commit()
        st.success("Patient added successfully.")
        
        # Redirect to another page after successful addition
        return True
    except sqlite3.Error as e:
        st.error(f"Error: {e}")
        return False


# Function to retrieve all patients
def get_patients(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM patients
        ''')
        rows = cursor.fetchall()
        return rows
    except sqlite3.Error as e:
        st.error(f"Error: {e}")
        return []

# Function to clear all data in the database
def clear_database(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM patients
        ''')
        conn.commit()
        st.session_state.is_database_cleared = True  # Set the flag
        st.success("Database cleared successfully.")
    except sqlite3.Error as e:
        st.error(f"Error: {e}")

# Function to display the Admin Page with clear database option and disease-wise patient pie chart
def admin_page(conn):
    st.title("Admin Page")

    # Clear Database option
    if st.button("Clear Database"):
        clear_database(conn)

    # Display disease-wise patient pie chart
    st.subheader("Disease-wise Patient Distribution")
    patients = get_patients(conn)
    df = pd.DataFrame(patients, columns=['ID', 'Name', 'Email', 'Phone', 'Address', 'Disease'])
    if not df.empty:
        disease_counts = df['Disease'].value_counts()
        fig = px.pie(names=disease_counts.index, values=disease_counts.values, title="Disease-wise Patient Distribution")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No patient data available to display.")

# Function to display the View patients Page with search functionality
def view_patients(conn):
    st.title("View patients")

    # Check if the database is cleared
    if st.session_state.is_database_cleared:
        st.info("Database is cleared. No patients to display.")
        return

    # Search bar for filtering patients by name
    search_query = st.text_input("Search by name:", "").strip().lower()

    # Retrieve all patients from the database
    patients = get_patients(conn)

    # Filter patients based on the search query
    filtered_patients = [patient for patient in patients if search_query.lower() in patient[1].lower()]

    # Display filtered patients in a table
    if filtered_patients:
        st.write("Patients Information:")
        # Create a DataFrame from the filtered patients
        df = pd.DataFrame(filtered_patients, columns=['ID', 'Name', 'Email', 'Phone', 'Address', 'Disease'])
        # Display the DataFrame as a table
        st.table(df)
    else:
        st.warning("No patients found matching the search criteria.")

# Admin login function
def admin_login():
    st.title("Admin Login")
    if not st.session_state.is_admin_logged_in:
        email_placeholder = st.empty()
        password_placeholder = st.empty()
        email = email_placeholder.text_input("Email", key="admin_email")
        password = password_placeholder.text_input("Password", type="password", key="admin_password")
        login_button = st.button("Login")
        if login_button:
            if email == "admin@gmail.com" and password == "admin":
                st.session_state.is_admin_logged_in = True
                st.success("Login successful.")
                email_placeholder.empty()
                password_placeholder.empty()
                st.session_state.show_login_button = False  # Hide the login button
                st.session_state.show_login_message = False  # Hide the login successful message
            else:
                st.error("Invalid email or password. Please try again.")
    else:
        st.success("Logged in as admin.")
    
    # Place the logout button at the top right corner
    logout_placeholder = st.empty()
    logout_placeholder.write("")  # Create space for the button
    if st.session_state.is_admin_logged_in:
        logout_button = logout_placeholder.button("Logout", key="logout_button_admin_login")
        if logout_button:
            st.session_state.is_admin_logged_in = False
            st.success("Logged out successfully.")

# Function to display the "Add patient" page for both admin and user
def add_patient_page(conn):
    st.title("Add patient")
    name = st.text_input("Name", key="add_name")
    email = st.text_input("Email", key="add_email")
    phone = st.text_input("Phone", key="add_phone")
    address = st.text_input("Address", key="add_address")
    disease = st.text_input("Disease", key="add_disease")
    if st.button("Add patient"):
        if add_patient(conn, name, email, phone, address, disease):
            st.markdown("[Next Page](http://localhost:8501)")

# Main function
def main():
    # Initialize session state
    if 'is_database_cleared' not in st.session_state:
        st.session_state.is_database_cleared = False
    if 'is_admin_logged_in' not in st.session_state:
        st.session_state.is_admin_logged_in = False
    if 'chart_update_trigger' not in st.session_state:
        st.session_state.chart_update_trigger = 0

    # Set page configuration
    st.set_page_config(page_title="Health Assistant", layout="wide", page_icon="🧑‍⚕️")
    
    # Sidebar for navigation
    with st.sidebar:
        st.title("Navigation")
        selected = st.radio("Go to:", ["Admin"])

    # Database setup
    database = "patient_history.db"
    conn = create_connection(database)
    if conn is not None:
        create_patient_table(conn)
        
        # Admin page
        if selected == "Admin":
            admin_login()
            if st.session_state.is_admin_logged_in:
                admin_page(conn)
                st.title("Navigation")
                selected_page = st.radio("Go to:", ["Add patient", "View patients"])
                if selected_page == "Add patient":
                    add_patient_page(conn)
                elif selected_page == "View patients":
                    view_patients(conn)

if __name__ == "__main__":
    main()
