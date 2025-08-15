import streamlit as st
import pandas as pd
import sqlite3
import os
from datetime import datetime

# Get correct path to menu.csv
menu_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'menu.csv')
menu_path = os.path.abspath(menu_path)

# Read menu data
menu_df = pd.read_csv(menu_path)

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'restaurant.db')

st.title("🍽️ Restaurant Billing System")

selected_items = []

# Display menu
st.subheader("📋 Menu")
for index, row in menu_df.iterrows():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"**{row['Item']}**  \n{row['category']}")
    with col2:
        qty = st.number_input(f"{row['Item']} (₹{row['Price']})", min_value=0, key=index)
        if qty > 0:
            selected_items.append({
                "Item": row['Item'],
                "Price": row['Price'],
                "GST": row['GST'],
                "Qty": qty
            })

# Billing summary
if selected_items:
    st.markdown("---")
    st.subheader("🧾 Bill Summary")

    subtotal = sum(item["Price"] * item["Qty"] for item in selected_items)
    gst_total = sum((item["Price"] * item["GST"] * item["Qty"]) / 100 for item in selected_items)
    discount = 0

    if subtotal > 500:
        discount = subtotal * 0.1  # 10% discount

    grand_total = subtotal + gst_total - discount

    st.write(f"Subtotal: ₹{subtotal:.2f}")
    st.write(f"GST Total: ₹{gst_total:.2f}")
    st.write(f"Discount: ₹{discount:.2f}")
    st.write(f"**Grand Total: ₹{grand_total:.2f}**")

    payment_method = st.selectbox("Payment Method", ["Cash", "UPI", "Card"])

    if st.button("✅ Confirm Order"):
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cur.execute("""
                INSERT INTO orders (order_type, total_amount, gst_amount, discount, payment_method, order_time)
                VALUES (?, ?, ?, ?, ?, ?)
            """, ("Dine-in", grand_total, gst_total, discount, payment_method, now))
            order_id = cur.lastrowid

            for item in selected_items:
                cur.execute("""
                    INSERT INTO order_items (order_id, item_name, quantity, price)
                    VALUES (?, ?, ?, ?)
                """, (order_id, item["Item"], item["Qty"], item["Price"]))

            conn.commit()
            st.success("✅ Order confirmed and saved to database!")

else:
    st.info("Please select at least one item to generate the bill.")

