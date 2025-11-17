# 🩸 Blood & Organ Donation Management System  
*A Complete DBMS Project using Python (Streamlit) + MySQL*

This project is a fully functional **Blood & Organ Donation Management System** designed using:

- **Python** (Streamlit UI)  
- **MySQL** (database with triggers, functions, stored procedures, constraints)  

It demonstrates **advanced DBMS concepts**, interactive UI, CRUD operations, form handling, stored procedure integration, and animations.

---

# 📌 Key Features  

## ✔️ Application Features
- Animated Streamlit UI  
- Dashboard (donors, patients, donations, blood units)  
- Donor management (CRUD)  
- Patient registration via stored procedure  
- Add donation (Blood/Organ) via stored procedure  
- Search donors  
- Update blood / organ stock  
- View Hospitals & Addresses  
- Styled metric cards, tables & transitions  

## ✔️ Database Features
- **13 fully connected tables**  
- **Sample data inserted for all entities**  
- **Stored Procedures**
  - `RegisterNewPatient`
  - `AddDonation`
- **Functions**
  - `CalculateDonorAge`
  - `DonorFullName`
- **Triggers**
  - Before successful donation, mark donor as *ineligible*
  - Auto-mark blood as *Expired* on expiry date  
- **Cascading delete/update**  
- **Auto-increment primary keys**  
- **Strong referential integrity**  

---

# 🚀 How to Run the Project

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
```

## 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

## 3️⃣ Set Up the MySQL Database

Run the provided SQL script:
- Creates database
- Creates tables
- Inserts sample data
- Creates triggers
- Creates functions
- Creates stored procedures

Update DB credentials in app.py:
```bash
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="blood_organ_donation"
)
```

## 4️⃣ Run the Streamlit Application
``` bash
streamlit run app.py
```


