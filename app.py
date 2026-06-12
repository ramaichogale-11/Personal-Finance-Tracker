import streamlit as st
import pandas as pd
import os
from datetime import datetime

CSV_FILE = "expenses.csv"
CATEGORIES = ["Food", "Transport", "Shopping", "Entertainment", "Savings", "Other"]

st.set_page_config(page_title="Trackly", page_icon="💸", layout="centered")

st.title("💸 Trackly")
st.write("A student-friendly finance tracker to record expenses and understand spending habits.")

def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    return pd.DataFrame(columns=["Date", "Category", "Name", "Amount"])

def save_data(df):
    df.to_csv(CSV_FILE, index=False)

df = load_data()

st.header("Add Expense")

with st.form("expense_form"):
    category = st.selectbox("Category", CATEGORIES)
    name = st.text_input("Expense name")
    amount = st.number_input("Amount (₹)", min_value=0.0, step=10.0)

    submitted = st.form_submit_button("Add Expense")

    if submitted:
        if name.strip() == "":
            st.error("Expense name cannot be empty.")
        elif amount <= 0:
            st.error("Amount must be greater than 0.")
        else:
            new_row = {
                "Date": datetime.now().strftime("%d-%m-%Y"),
                "Category": category,
                "Name": name,
                "Amount": amount
            }

            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_data(df)
            st.success(f"Saved: {name} ₹{amount:.2f}")

st.header("Expense History")

if df.empty:
    st.info("No expenses recorded yet.")
else:
    st.dataframe(df, use_container_width=True)

    total = df["Amount"].sum()
    st.metric("Total Spending", f"₹{total:.2f}")

    st.header("Spending by Category")
    category_summary = df.groupby("Category")["Amount"].sum().reset_index()
    st.dataframe(category_summary, use_container_width=True)

    st.bar_chart(category_summary.set_index("Category"))

    st.header("Delete Expense")
    delete_index = st.number_input("Enter row number to delete", min_value=0, max_value=len(df)-1, step=1)

    if st.button("Delete Selected Expense"):
        df = df.drop(delete_index).reset_index(drop=True)
        save_data(df)
        st.success("Expense deleted. Refresh the app to see changes.")
