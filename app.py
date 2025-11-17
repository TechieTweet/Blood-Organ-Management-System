# app.py
import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd
from datetime import datetime, date

st.set_page_config(page_title="Blood & Organ Donation System", layout="wide")

# ----------------------
# Database connection
# ----------------------
@st.cache_resource
def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="#Swathi@1234",        # change if you have a password
            database="blood_organ_donation",
            autocommit=False
        )
        return conn
    except Error as e:
        st.error(f"MySQL connection error: {e}")
        return None

def run_query(query, params=None, fetch=True, dict_cursor=False):
    conn = get_connection()
    if conn is None:
        return None
    cursor = conn.cursor(dictionary=dict_cursor) if dict_cursor else conn.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        if fetch:
            cols = [c[0] for c in cursor.description] if cursor.description else []
            rows = cursor.fetchall()
            df = pd.DataFrame(rows, columns=cols) if rows else pd.DataFrame(columns=cols)
            return df
        else:
            conn.commit()
            return True
    except Exception as e:
        conn.rollback()
        st.error(f"Query error: {e}")
        return None
    finally:
        cursor.close()

def call_proc(proc_name, args=()):
    conn = get_connection()
    if conn is None:
        return False
    cursor = conn.cursor()
    try:
        cursor.callproc(proc_name, args)
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        st.error(f"Stored procedure error: {e}")
        return False
    finally:
        cursor.close()

# ----------------------
# Layout and Navigation
# ----------------------
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Go to", [
    "Dashboard",
    "Manage Donors",
    "Manage Patients",
    "Manage Donations",
    "View Donations",
    "Blood Stock",
    "Organ Stock",
    "Hospitals"
])

# ----------------------
# Helper small utilities
# ----------------------
def df_to_table(df: pd.DataFrame):
    if df is None:
        st.warning("No data")
        return
    if df.empty:
        st.info("No records found")
        return
    st.dataframe(df)

def safe_date_input(label, value=None):
    if value is None or value == "" or pd.isna(value):
        return st.date_input(label)
    # value may be datetime/date/string
    try:
        if isinstance(value, datetime):
            return st.date_input(label, value.date())
        if isinstance(value, date):
            return st.date_input(label, value)
        # try parse string
        return st.date_input(label, datetime.strptime(str(value), "%Y-%m-%d").date())
    except:
        return st.date_input(label)

# ----------------------
# DASHBOARD
# ----------------------
if page == "Dashboard":
    st.title("Blood & Organ Donation System — Dashboard")
    conn = get_connection()
    if conn is None:
        st.stop()

    c1, c2, c3, c4 = st.columns(4)
    # counts
    donors = run_query("SELECT COUNT(*) AS cnt FROM Donor", fetch=True)
    patients = run_query("SELECT COUNT(*) AS cnt FROM Patient", fetch=True)
    donations = run_query("SELECT COUNT(*) AS cnt FROM Donation", fetch=True)
    blood_units = run_query("SELECT COUNT(*) AS cnt FROM Blood WHERE B_status='Available'", fetch=True)

    c1.metric("Donors", int(donors['cnt'].iloc[0]) if not donors.empty else 0)
    c2.metric("Patients", int(patients['cnt'].iloc[0]) if not patients.empty else 0)
    c3.metric("Donations", int(donations['cnt'].iloc[0]) if not donations.empty else 0)
    c4.metric("Available Blood Units", int(blood_units['cnt'].iloc[0]) if not blood_units.empty else 0)

    st.markdown("---")
    st.subheader("Recent Donations")
    recent = run_query("SELECT Do_id, D_id, H_id, Do_type, Do_DT, success_status FROM Donation ORDER BY Do_DT DESC LIMIT 10", fetch=True)
    df_to_table(recent)

# ----------------------
# MANAGE DONORS (CRUD)
# ----------------------
elif page == "Manage Donors":
    st.title("Manage Donors")
    conn = get_connection()
    if conn is None:
        st.stop()

    tab1, tab2, tab3 = st.tabs(["View Donors", "Add Donor", "Edit / Delete Donor"])

    # View donors
    with tab1:
        st.subheader("All donors")
        donors_df = run_query("SELECT * FROM Donor ORDER BY D_id", fetch=True)
        df_to_table(donors_df)

        if not donors_df.empty:
            st.markdown("**Search**")
            q = st.text_input("Search by name or blood group (partial)")
            if q:
                qparam = f"%{q}%"
                df = run_query("SELECT * FROM Donor WHERE FN LIKE %s OR MN LIKE %s OR LN LIKE %s OR B_grp LIKE %s",
                               params=(qparam, qparam, qparam, qparam))
                df_to_table(df)

    # Add donor
    with tab2:
        st.subheader("Add new donor")
        with st.form("add_donor"):
            fn = st.text_input("First Name", max_chars=50)
            mn = st.text_input("Middle Name", max_chars=50)
            ln = st.text_input("Last Name", max_chars=50)
            dob = st.date_input("DOB")
            gender = st.selectbox("Gender", ["M", "F"])
            bgrp = st.text_input("Blood Group (ex: A+)", max_chars=5)
            d_type = st.selectbox("Donation Type", ["Blood", "Organ"])
            d_date = st.date_input("Donation Date", value=date.today())
            d_time = st.time_input("Donation Time", value=datetime.now().time())
            d_datetime = datetime.combine(d_date, d_time)
            submitted = st.form_submit_button("Add Donor")
        if submitted:
            try:
                q = """INSERT INTO Donor (FN, MN, LN, DOB, Gender, B_grp, D_type, D_dateTime, Eligibility_status)
                       VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                params = (fn, mn, ln, dob, gender, bgrp, d_type, d_datetime, True)
                conn = get_connection()
                cur = conn.cursor()
                cur.execute(q, params)
                conn.commit()
                new_id = cur.lastrowid
                cur.close()
                st.success(f"Donor added with D_id = {new_id}")
            except Exception as e:
                st.error(f"Error adding donor: {e}")

    # Edit / Delete
    with tab3:
        st.subheader("Edit or Delete a donor")
        st.info("Enter an existing Donor ID to load details.")
        did = st.number_input("Donor ID", min_value=1, step=1)
        if st.button("Load Donor"):
            df = run_query("SELECT * FROM Donor WHERE D_id=%s", params=(did,))
            if df is None or df.empty:
                st.warning("Donor not found")
            else:
                donor = df.iloc[0].to_dict()
                with st.form("edit_donor_form"):
                    fn = st.text_input("First Name", value=donor.get("FN",""))
                    mn = st.text_input("Middle Name", value=donor.get("MN",""))
                    ln = st.text_input("Last Name", value=donor.get("LN",""))
                    dob_val = donor.get("DOB")
                    dob = safe_date_input("DOB", dob_val)
                    gender = st.selectbox("Gender", ["M","F"], index=0 if donor.get("Gender","M")=="M" else 1)
                    bgrp = st.text_input("Blood Group", value=donor.get("B_grp",""))
                    eligibility = st.checkbox("Eligibility_status (True = eligible)", value=bool(donor.get("Eligibility_status", True)))
                    save = st.form_submit_button("Save Changes")
                if save:
                    try:
                        q = """UPDATE Donor SET FN=%s, MN=%s, LN=%s, DOB=%s, Gender=%s, B_grp=%s, Eligibility_status=%s WHERE D_id=%s"""
                        params = (fn, mn, ln, dob, gender, bgrp, eligibility, did)
                        conn = get_connection()
                        cur = conn.cursor()
                        cur.execute(q, params)
                        conn.commit()
                        cur.close()
                        st.success("Donor updated")
                    except Exception as e:
                        st.error(f"Update error: {e}")

        st.markdown("---")
        st.warning("Delete donor (this will cascade remove phone numbers and related references depending on FK settings).")
        del_id = st.number_input("Donor ID to delete", min_value=1, step=1, key="del_donor")
        if st.button("Delete Donor"):
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("DELETE FROM Donor WHERE D_id=%s", (del_id,))
                conn.commit()
                cur.close()
                st.success(f"Deleted donor {del_id} (if existed)")
            except Exception as e:
                st.error(f"Delete error: {e}")

# ----------------------
# MANAGE PATIENTS (use stored procedure RegisterNewPatient)
# ----------------------
elif page == "Manage Patients":
    st.title("Manage Patients")
    conn = get_connection()
    if conn is None:
        st.stop()

    tab1, tab2 = st.tabs(["View Patients", "Register Patient"])

    with tab1:
        st.subheader("Patients")
        df = run_query("SELECT p.P_id, p.H_id, p.FN, p.MN, p.LN, p.DOB, p.Urgency_level, p.Gender, p.B_grp FROM Patient p ORDER BY P_id", fetch=True)
        df_to_table(df)

    with tab2:
        st.subheader("Register new patient (calls stored procedure)")
        with st.form("register_patient"):
            p_H_id = st.number_input("Hospital ID", min_value=1, step=1)
            p_FN = st.text_input("First Name")
            p_MN = st.text_input("Middle Name")
            p_LN = st.text_input("Last Name")
            p_DOB = st.date_input("DOB")
            p_Urgency_level = st.selectbox("Urgency level", ["High","Medium","Low","Critical"])
            p_Gender = st.selectbox("Gender", ["M","F"])
            p_B_grp = st.text_input("Blood Group")
            p_P_Ph_no = st.text_input("Phone Number")
            submitted = st.form_submit_button("Register Patient")
        if submitted:
            ok = call_proc("RegisterNewPatient", (int(p_H_id), p_FN, p_MN, p_LN, p_DOB, p_Urgency_level, p_Gender, p_B_grp, p_P_Ph_no))
            if ok:
                st.success("Patient registered via stored procedure")
            else:
                st.error("Could not register patient")

# ----------------------
# MANAGE DONATIONS (use AddDonation stored procedure)
# ----------------------
elif page == "Manage Donations":
    st.title("Add Donation (Stored Procedure)")
    conn = get_connection()
    if conn is None:
        st.stop()

    st.info("Use donor ID and hospital ID from database. This will call your AddDonation stored procedure and insert relevant rows into Donation, Blood or Organ tables depending on type.")

    with st.form("add_donation_form"):
        p_D_id = st.number_input("Donor ID", min_value=1, step=1)
        p_H_id = st.number_input("Hospital ID", min_value=1, step=1)
        p_Do_type = st.selectbox("Donation Type", ["Blood", "Organ"])
        p_Do_DT = st.date_input("Donation Date", value=date.today())
        p_success_status = st.selectbox("Success status", ["Success", "Failed"])
        p_collection_date = st.date_input("Collection Date", value=date.today())
        p_storage = st.text_input("Storage location (for Blood insert)", value="Storage A")
        p_type_detail = st.text_input("Organ type or blood-group detail", value="")
        submitted = st.form_submit_button("Add Donation")
    if submitted:
        ok = call_proc("AddDonation", (int(p_D_id), int(p_H_id), p_Do_type, p_Do_DT, p_success_status, p_collection_date, p_storage, p_type_detail))
        if ok:
            st.success("Donation added via stored procedure")
        else:
            st.error("Failed to add donation")

# ----------------------
# VIEW DONATIONS
# ----------------------
elif page == "View Donations":
    st.title("Donations")
    df = run_query("SELECT * FROM Donation ORDER BY Do_DT DESC", fetch=True)
    df_to_table(df)

# ----------------------
# BLOOD STOCK
# ----------------------
elif page == "Blood Stock":
    st.title("Blood Stock")
    df = run_query("SELECT B_id, Do_id, stor_loc, B_status, Expiry_date, B_collection_date FROM Blood ORDER BY B_id", fetch=True)
    df_to_table(df)

    st.markdown("---")
    st.subheader("Mark blood as issued/expired")
    b_id = st.number_input("B_id", min_value=1, step=1)
    new_status = st.selectbox("New status", ["Available", "Issued", "Expired"])
    if st.button("Update Blood Status"):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("UPDATE Blood SET B_status=%s WHERE B_id=%s", (new_status, int(b_id)))
            conn.commit()
            cur.close()
            st.success("Blood status updated")
        except Exception as e:
            st.error(f"Update error: {e}")

# ----------------------
# ORGAN STOCK
# ----------------------
elif page == "Organ Stock":
    st.title("Organ Stock")
    df = run_query("SELECT O_id, Do_id, O_type, O_DT, O_status, O_collection_DT FROM Organ ORDER BY O_id", fetch=True)
    df_to_table(df)

    st.markdown("---")
    st.subheader("Update Organ Status")
    o_id = st.number_input("O_id", min_value=1, step=1)
    o_status = st.selectbox("New organ status", ["Healthy", "Rejected", "Pending", "Used"])
    if st.button("Update Organ Status"):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("UPDATE Organ SET O_status=%s WHERE O_id=%s", (o_status, int(o_id)))
            conn.commit()
            cur.close()
            st.success("Organ status updated")
        except Exception as e:
            st.error(f"Update error: {e}")

# ----------------------
# HOSPITALS
# ----------------------
elif page == "Hospitals":
    st.title("Hospitals")
    df = run_query("SELECT h.H_id, h.H_name, h.H_Ph_no, ha.city, ha.state, ha.pincode FROM Hospital h LEFT JOIN Hospital_address ha ON h.H_id=ha.H_id ORDER BY h.H_id", fetch=True)
    df_to_table(df)

