import streamlit as st
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('lost_found.db')
c = conn.cursor()

# Create a "items" table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT,
        description TEXT,
        location TEXT,
        date TEXT,
        image BLOB,
        is_lost INTEGER,
        contact_name TEXT,
        contact_email TEXT
    )
''')

# Set page config to wide layout
st.set_page_config(layout="wide")

# Create a title and subtitle for the website with special effects
st.title("🔍 FindItNow")

# Create a sidebar with options to report a lost item or a found item
menu = ["Report Lost Item", "Report Found Item", "View Lost Items", "View Found Items"]
choice = st.sidebar.selectbox("📋 Select an option", menu)

# Depending on the option chosen, show different form fields for the user to fill out
if choice == "Report Lost Item":
    st.markdown ("#### Report Lost Item")
    st.write("Please fill out the form below to report a lost item:")
    col1, col2 = st.columns(2)

    with col1:
        item_name = st.text_input("Item Name")
        description = st.text_area("Description")
        contact_name = st.text_input("Your Name")
        contact_email = st.text_input("Your Email")

    with col2:
        lost_location = st.text_input("Lost Location")
        date_lost = st.date_input("Date Lost")

    image = st.file_uploader("📷 Upload an image of the lost item")

    if st.button("Submit"):
        if item_name and description and lost_location and date_lost and image:
            # Save the form data to SQLite database
            c.execute('''
                INSERT INTO items (item_name, description, location, date, image, is_lost, contact_name, contact_email)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (item_name, description, lost_location, str(date_lost), image.read(), 1, contact_name, contact_email))
            conn.commit()
            st.success("👍 Lost item reported successfully!")
        else:
            st.warning("⚠️ Please fill out all the form fields and upload an image.")

elif choice == "Report Found Item":
    st.markdown("#### Report Found Item")
    st.write("Please fill out the form below to report a found item:")
    col1, col2 = st.columns(2)

    with col1:
        item_name = st.text_input("Item Name")
        description = st.text_area("Description")
        contact_name = st.text_input("Your Name")
        contact_email = st.text_input("Your Email")

    with col2:
        found_location = st.text_input("Found Location")
        date_found = st.date_input("Date Found")

    image = st.file_uploader("📷 Upload an image of the found item")

    if st.button("Submit"):
        if item_name and description and found_location and date_found and image:
            # Save the form data to SQLite database
            c.execute('''
                INSERT INTO items (item_name, description, location, date, image, is_lost, contact_name, contact_email)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (item_name, description, found_location, str(date_found), image.read(), 0, contact_name, contact_email))
            conn.commit()
            st.success("👍 Found item reported successfully!")
        else:
            st.warning("⚠️ Please fill out all the form fields and upload an image.")

elif choice == "View Lost Items":
    st.markdown("---")
    st.write("🔍 Lost Items:")
    c.execute("SELECT * FROM items WHERE is_lost = 1")
    rows = c.fetchall()
    for row in rows:
        st.write("Item Name:", row[1])
        st.write("Description:", row[2])
        st.write("Lost Location:", row[3])
        st.write("Date Lost:", row[4])
        st.write("Contact Name:", row[7])
        st.write("Contact Email:", row[8])
        st.image(row[5], caption=row[1], use_column_width=True)
        st.markdown("---")

elif choice == "View Found Items":
    st.markdown("---")
    st.write("🔍 Found Items:")
    c.execute("SELECT * FROM items WHERE is_lost = 0")
    rows = c.fetchall()
    for row in rows:
        st.write("Item Name:", row[1])
        st.write("Description:", row[2])
        st.write("Found Location:", row[3])
        st.write("Date Found:", row[4])
        st.write("Contact Name:", row[7])
        st.write("Contact Email:", row[8])
        st.image(row[5], caption=row[1], use_column_width=True)
        st.markdown("---")

# Close the SQLite database connection
conn.close()
