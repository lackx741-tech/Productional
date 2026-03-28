import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("🧠 Smart Wallet Ops Dashboard")

menu = ["Create Wallet", "View Wallet", "Send Transaction"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Create Wallet":
    st.subheader("Create Wallet")

    owner = st.text_input("Owner")

    if st.button("Create"):
        try:
            res = requests.post(f"{API_URL}/wallet", json={"owner": owner}, timeout=10)
            res.raise_for_status()
            st.write(res.json())
        except requests.exceptions.ConnectionError:
            st.error("Cannot reach the API. Is the backend running?")
        except requests.exceptions.HTTPError as e:
            st.error(f"API error: {e.response.json().get('detail', str(e))}")
        except Exception as e:
            st.error(f"Unexpected error: {e}")


elif choice == "View Wallet":
    st.subheader("View Wallet")

    wallet_id = st.number_input("Wallet ID", step=1)

    if st.button("Fetch"):
        try:
            res = requests.get(f"{API_URL}/wallet/{int(wallet_id)}", timeout=10)
            res.raise_for_status()
            st.write(res.json())
        except requests.exceptions.ConnectionError:
            st.error("Cannot reach the API. Is the backend running?")
        except requests.exceptions.HTTPError as e:
            st.error(f"API error: {e.response.json().get('detail', str(e))}")
        except Exception as e:
            st.error(f"Unexpected error: {e}")


elif choice == "Send Transaction":
    st.subheader("Transaction")

    wallet_id = st.number_input("Wallet ID", step=1)
    amount = st.number_input("Amount")
    tx_type = st.selectbox("Type", ["credit", "debit"])

    if st.button("Execute"):
        try:
            res = requests.post(
                f"{API_URL}/transaction",
                json={
                    "wallet_id": int(wallet_id),
                    "amount": amount,
                    "type": tx_type
                },
                timeout=10
            )
            res.raise_for_status()
            st.write(res.json())
        except requests.exceptions.ConnectionError:
            st.error("Cannot reach the API. Is the backend running?")
        except requests.exceptions.HTTPError as e:
            st.error(f"API error: {e.response.json().get('detail', str(e))}")
        except Exception as e:
            st.error(f"Unexpected error: {e}")
