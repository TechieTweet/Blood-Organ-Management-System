# app.py
# Blood & Organ Donation Management System
# Final copy-paste file with UI enhancements: blood-drop animations, animated dashboard, page transitions.
# Database: blood_organ_donation
# NOTE: If your MySQL password or host differ, edit get_connection() accordingly.

import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd
from datetime import datetime, date, time

# -----------------------
# Streamlit config
# -----------------------
st.set_page_config(page_title="Blood & Organ Donation System", layout="wide", page_icon="🩸")

# -----------------------
# CSS + Animations
# -----------------------
st.markdown(r"""
<style>
html, body, [class*="css"] { font-family: 'Segoe UI', sans-serif; }

/* Page fade-in */
.main { animation: fadeIn 0.9s ease; }
@keyframes fadeIn { from {opacity:0;} to {opacity:1;} }

/* Blood drops */
.blood-drop {
  position: fixed;
  top: -24px;
  width: 12px;
  height: 18px;
  background: #b10018;
  border-radius: 50%;
  animation: drop 3s linear infinite;
  opacity: 0.9;
  z-index: 0;
}
@keyframes drop {
  0% { transform: translateY(0px); opacity: 1; }
  90% { transform: translateY(95vh); opacity: 1; }
  100% { transform: translateY(100vh); opacity: 0; }
}
.blood-drop:nth-child(1){ left:10%; animation-delay:0s; }
.blood-drop:nth-child(2){ left:28%; animation-delay:0.6s; }
.blood-drop:nth-child(3){ left:48%; animation-delay:1.2s; }
.blood-drop:nth-child(4){ left:68%; animation-delay:1.8s; }
.blood-drop:nth-child(5){ left:86%; animation-delay:2.4s; }

/* Header */
.big-header {
  padding: 22px;
  text-align: center;
  color: white;
  font-size: 30px;
  font-weight: 700;
  background: linear-gradient(90deg, #e63946, #b10018);
  border-radius: 14px;
  margin-bottom: 20px;
  box-shadow: 0 6px 18px rgba(0,0,0,0.25);
}

/* Metric cards */
[data-testid="metric-container"] {
  animation: zoomIn 0.8s ease;
  background: #fff;
  padding: 14px;
  border-radius: 14px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.12);
  border-left: 6px solid #e63946;
}
@keyframes zoomIn { 0% { transform: scale(0.75); opacity:0; } 100% { transform: scale(1); opacity:1; } }
[data-testid="metric-container"] > label { color: #8a000f; font-weight:700; }
[data-testid="metric-container"] > div { color: #b10018; font-weight:800; font-size:28px; }

/* Buttons */
.stButton > button {
  background: linear-gradient(90deg, #ff4655, #d90429) !important;
  color: white !important;
  padding: 10px 20px !important;
  border-radius: 10px !important;
  font-weight: 700 !important;
  border: none !important;
  box-shadow: 0 4px 12px rgba(160,0,0,0.25);
}
.stButton > button:hover { transform: scale(1.04); }

/* Inputs */
input, select, textarea {
  border-radius: 8px !important;
  border: 1.8px solid #e63946 !important;
}
input:focus, select:focus, textarea:focus {
  box-shadow: 0 0 8px rgba(200,0,0,0.2) !important;
  border-color: #b10018 !important;
}

/* Tables */
.dataframe { border-radius: 10px !important; overflow: hidden; box-shadow: 0 3px 12px rgba(0,0,0,0.12); }
.dataframe thead th { background: #e63946 !important; color: white !important; font-weight:700; }

/* Small helpers */
.card { background: white; padding: 16px; border-radius: 12px; box-shadow: 0 3px 10px rgba(0,0,0,0.08); }

</style>

<!-- Blood drops -->
<div class="blood-drop"></div><div class="blood-drop"></div><div class="blood-drop"></div><div class="blood-drop"></div><div class="blood-drop"></div>
""", unsafe_allow_html=True)

st.markdown("<div class='big-header'>🩸 Blood & Organ Donation Management System</div>", unsafe_allow_html=True)

# -----------------------
# Database helpers
# -----------------------
@st.cache_resource
def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="#Swathi@1234",
            database="blood_organ_donation",
            autocommit=False
        )
        return conn
    except Error as e:
        st.error(f"MySQL connection error: {e}")
        return None

def run_query(query, params=None, fetch=True):
    """
    Execute a query. If fetch=True returns a pandas DataFrame.
    If fetch=False executes and commits, returning True/False.
    """
    conn = get_connection()
    if conn is None:
        return None
    cur = conn.cursor()
    try:
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
        if fetch:
            cols = [c[0] for c in cur.description] if cur.description else []
            rows = cur.fetchall()
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
        cur.close()

def call_proc(proc_name, args=()):
    conn = get_connection()
    if conn is None:
        return False
    cur = conn.cursor()
    try:
        cur.callproc(proc_name, args)
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        st.error(f"Stored procedure error: {e}")
        return False
    finally:
        cur.close()

def df_to_table(df):
    if df is None:
        st.warning("No data (query failed or returned None).")
        return
    if df.empty:
        st.info("No records found.")
        return
    st.dataframe(df, use_container_width=True)

# -----------------------
# Sidebar navigation
# -----------------------
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

# -----------------------
# Pages
# -----------------------

# DASHBOARD
if page == "Dashboard":
    st.title("📊 Dashboard")
    donors = run_query("SELECT COUNT(*) AS cnt FROM Donor")
    patients = run_query("SELECT COUNT(*) AS cnt FROM Patient")
    donations = run_query("SELECT COUNT(*) AS cnt FROM Donation")
    blood_units = run_query("SELECT COUNT(*) AS cnt FROM Blood WHERE B_status='Available'")

    d_count = int(donors['cnt'].iloc[0]) if donors is not None and not donors.empty else 0
    p_count = int(patients['cnt'].iloc[0]) if patients is not None and not patients.empty else 0
    don_count = int(donations['cnt'].iloc[0]) if donations is not None and not donations.empty else 0
    b_count = int(blood_units['cnt'].iloc[0]) if blood_units is not None and not blood_units.empty else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Donors", d_count)
    c2.metric("Patients", p_count)
    c3.metric("Donations", don_count)
    c4.metric("Available Blood Units", b_count)

    st.markdown("---")
    st.subheader("Recent Donations")
    recent = run_query("SELECT Do_id, D_id, H_id, Do_type, Do_DT, success_status FROM Donation ORDER BY Do_DT DESC LIMIT 10")
    df_to_table(recent)

# MANAGE DONORS
elif page == "Manage Donors":
    st.title("🧑‍🤝‍🧑 Manage Donors")
    conn = get_connection()
    if conn is None:
        st.stop()

    tab1, tab2, tab3 = st.tabs(["View Donors", "Add Donor", "Edit / Delete Donor"])

    # View Donors
    with tab1:
        st.subheader("All donors")
        donors_df = run_query("SELECT * FROM Donor ORDER BY D_id")
        df_to_table(donors_df)

        q = st.text_input("Search by name or blood group (partial)")
        if q:
            qp = f"%{q}%"
            df = run_query("SELECT * FROM Donor WHERE FN LIKE %s OR MN LIKE %s OR LN LIKE %s OR B_grp LIKE %s",
                           params=(qp, qp, qp, qp))
            df_to_table(df)

    # Add Donor
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
        if 'loaded_donor' not in st.session_state:
            st.session_state.loaded_donor = None

        did = st.number_input("Donor ID", min_value=1, step=1, key="edit_donor_id")
        if st.button("Load Donor"):
            df = run_query("SELECT * FROM Donor WHERE D_id=%s", params=(did,))
            if df is None or df.empty:
                st.warning("Donor not found")
                st.session_state.loaded_donor = None
            else:
                st.session_state.loaded_donor = df.iloc[0].to_dict()
                st.session_state.loaded_donor['D_id'] = did
                st.success(f"Loaded donor {did}")

        if st.session_state.loaded_donor is not None:
            donor = st.session_state.loaded_donor
            with st.form("edit_donor_form"):
                fn = st.text_input("First Name", value=donor.get("FN",""))
                mn = st.text_input("Middle Name", value=donor.get("MN",""))
                ln = st.text_input("Last Name", value=donor.get("LN",""))
                dob_val = donor.get("DOB")
                try:
                    dob_input = st.date_input("DOB", value=dob_val if isinstance(dob_val, date) else date.today())
                except:
                    dob_input = st.date_input("DOB")
                gender = st.selectbox("Gender", ["M","F"], index=0 if donor.get("Gender","M")=="M" else 1)
                bgrp = st.text_input("Blood Group", value=donor.get("B_grp",""))
                eligibility = st.checkbox("Eligibility_status (True = eligible)", value=bool(donor.get("Eligibility_status", True)))
                save = st.form_submit_button("Save Changes")
            if save:
                try:
                    q = """UPDATE Donor SET FN=%s, MN=%s, LN=%s, DOB=%s, Gender=%s, B_grp=%s, Eligibility_status=%s WHERE D_id=%s"""
                    params = (fn, mn, ln, dob_input, gender, bgrp, eligibility, donor['D_id'])
                    cur = conn.cursor()
                    cur.execute(q, params)
                    conn.commit()
                    cur.close()
                    st.success(f"Donor {donor['D_id']} updated successfully!")
                    st.session_state.loaded_donor = None
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"Update error: {e}")

        st.markdown("---")
        st.warning("Delete donor (this will cascade remove phone numbers and related references depending on FK settings).")
        del_id = st.number_input("Donor ID to delete", min_value=1, step=1, key="del_donor")
        if st.button("Delete Donor"):
            try:
                cur = conn.cursor()
                cur.execute("DELETE FROM Donor WHERE D_id=%s", (del_id,))
                conn.commit()
                cur.close()
                st.success(f"Deleted donor {del_id} (if existed)")
            except Exception as e:
                st.error(f"Delete error: {e}")

# MANAGE PATIENTS
elif page == "Manage Patients":
    st.title("Manage Patients")
    conn = get_connection()
    if conn is None:
        st.stop()

    tab1, tab2 = st.tabs(["View Patients", "Register Patient"])

    with tab1:
        st.subheader("Patients")
        df = run_query("SELECT p.P_id, p.H_id, p.FN, p.MN, p.LN, p.DOB, p.Urgency_level, p.Gender, p.B_grp FROM Patient p ORDER BY P_id")
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

# MANAGE DONATIONS
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

# VIEW DONATIONS
elif page == "View Donations":
    st.title("Donations")
    df = run_query("SELECT * FROM Donation ORDER BY Do_DT DESC")
    df_to_table(df)

# BLOOD STOCK
elif page == "Blood Stock":
    st.title("Blood Stock")
    df = run_query("SELECT B_id, Do_id, stor_loc, B_status, Expiry_date, B_collection_date FROM Blood ORDER BY B_id")
    df_to_table(df)

    st.markdown("---")
    st.subheader("Mark blood as issued/expired")
    b_id = st.number_input("B_id", min_value=1, step=1, key="update_b_id")
    new_status = st.selectbox("New status", ["Available", "Issued", "Expired"], key="update_b_status")
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

# ORGAN STOCK
elif page == "Organ Stock":
    st.title("Organ Stock")
    df = run_query("SELECT O_id, Do_id, O_type, O_DT, O_status, O_collection_DT FROM Organ ORDER BY O_id")
    df_to_table(df)

    st.markdown("---")
    st.subheader("Update Organ Status")
    o_id = st.number_input("O_id", min_value=1, step=1, key="update_o_id")
    o_status = st.selectbox("New organ status", ["Healthy", "Rejected", "Pending", "Used"], key="update_o_status")
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

# HOSPITALS
elif page == "Hospitals":
    st.title("Hospitals")
    df = run_query("""SELECT h.H_id, h.H_name, h.H_Ph_no, ha.city, ha.state, ha.pincode
                      FROM Hospital h LEFT JOIN Hospital_address ha ON h.H_id=ha.H_id ORDER BY h.H_id""")
    df_to_table(df)


