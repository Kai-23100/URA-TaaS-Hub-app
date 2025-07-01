import streamlit as st
import uuid
import datetime

# In-memory mock databases
users_db = {}
transactions_db = []

# Utility Functions
def generate_tin():
    return str(uuid.uuid4())[:8].upper()

def register_user(name, nid):
    tin = generate_tin()
    users_db[tin] = {
        "name": name,
        "nid": nid,
        "tin": tin,
        "wallet_balance": 0,
        "compliance_score": 0,
        "registration_date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "transactions": []
    }
    return users_db[tin]

def record_transaction(tin, amount, tx_type):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    transaction = {
        "tin": tin,
        "amount": amount,
        "type": tx_type,
        "timestamp": timestamp
    }
    transactions_db.append(transaction)
    users_db[tin]["transactions"].append(transaction)
    if tx_type == 'deposit':
        users_db[tin]['wallet_balance'] += amount
    elif tx_type == 'payment':
        if users_db[tin]['wallet_balance'] >= amount:
            users_db[tin]['wallet_balance'] -= amount
        else:
            return False
    users_db[tin]['compliance_score'] += 5
    return transaction

# Streamlit UI Config
st.set_page_config(page_title="URA TaaS Hub", layout="centered")
st.title("📲 URA TaaS Hub – Simplifying Tax for the Informal Sector")
st.caption("Digital innovation aligned with global best practices – inspired by Taiwan, Argentina, and Tanzania.")

# Main Navigation Tabs
tabs = st.tabs(["Register TIN", "Dashboard", "Tax Wallet", "Generate Receipt"])

# --- Register TIN ---
with tabs[0]:
    st.header("📝 Quick Taxpayer Registration")
    st.write("Get your Tax Identification Number (TIN) in just a few seconds and unlock access to tax services.")
    name = st.text_input("Full Name")
    nid = st.text_input("National ID Number")
    if st.button("Register"):
        if name and nid:
            user = register_user(name, nid)
            st.success(f"Registration Successful! Your TIN is: {user['tin']}")
            st.info("This TIN will help identify your business and enable tax compliance support.")
        else:
            st.warning("Please fill in all fields to proceed.")

# --- Dashboard ---
with tabs[1]:
    st.header("📊 My Tax Compliance Dashboard")
    tin_input = st.text_input("Enter Your TIN")
    if st.button("Load Dashboard"):
        user = users_db.get(tin_input)
        if user:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Name", user['name'])
                st.metric("National ID", user['nid'])
                st.metric("TIN", user['tin'])
            with col2:
                st.metric("Wallet Balance", f"UGX {user['wallet_balance']:.2f}")
                st.metric("Compliance Score", user['compliance_score'])
                st.metric("Registered On", user['registration_date'])

            with st.expander("🔍 View Recent Transactions"):
                if user['transactions']:
                    for tx in reversed(user['transactions'][-5:]):
                        st.write(f"{tx['timestamp']} | {tx['type'].capitalize()} | UGX {tx['amount']:.2f}")
                else:
                    st.info("No transactions found.")
            st.success("You're building a digital compliance record. Keep it up!")
        else:
            st.error("TIN not found. Please verify your entry or register above.")

# --- Tax Wallet ---
with tabs[2]:
    st.header("💰 URA Tax Wallet")
    st.write("Easily deposit or pay your taxes in micro amounts to stay compliant and avoid surprises.")
    tin_wallet = st.text_input("TIN")
    amount = st.number_input("Amount (UGX)", min_value=500, step=500)
    action = st.radio("Select Action", ["Deposit", "Pay Tax"])
    if st.button("Submit Transaction") and tin_wallet in users_db:
        if action == "Deposit":
            record_transaction(tin_wallet, amount, 'deposit')
            st.success(f"UGX {amount} deposited successfully.")
        elif action == "Pay Tax":
            success = record_transaction(tin_wallet, amount, 'payment')
            if success:
                st.success(f"UGX {amount} paid successfully.")
            else:
                st.error("Insufficient funds. Please deposit first.")

# --- Receipt Generator ---
with tabs[3]:
    st.header("🧾 Smart Receipt Generator")
    st.write("Generate official digital receipts to share with customers. Builds trust and tax compliance history.")
    tin_receipt = st.text_input("Your TIN")
    customer_name = st.text_input("Customer Name")
    sale_amount = st.number_input("Sale Amount (UGX)", min_value=100)
    if st.button("Generate Receipt") and tin_receipt in users_db:
        receipt_id = str(uuid.uuid4())[:6].upper()
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        st.markdown(f"""
        **Receipt ID:** {receipt_id}  
        **Issued By (TIN):** {tin_receipt}  
        **Customer:** {customer_name}  
        **Amount:** UGX {sale_amount:.2f}  
        **Date Issued:** {timestamp}
        """)
        st.success("Receipt successfully generated.")

# Footer
st.markdown("---")
st.caption("URA TaaS Hub – Empowering Uganda’s informal sector to grow through smart, inclusive taxation.")
