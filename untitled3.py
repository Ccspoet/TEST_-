import streamlit as st
import requests
import json

# --- MATCHING PROTOTYPE STYLING ---
st.markdown("""
    <style>
    .alert-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border-left: 10px solid #2E7D32;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🐔 AgriAlert Mbour")

# --- ORANGE API LOGIC ---
# Credentials from your screenshot
CLIENT_ID = "NNwWwVlJrNuCRjs35aYf0YnblaZN4j8e"
CLIENT_SECRET = "gfgE0KJLqFYHqmFBInaud6elExp88PNKoYyaya03Lkua" # Replace with your actual secret

def get_orange_token():
    url = "https://api.orange.com/oauth/v3/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "client_credentials"}
    response = requests.post(url, headers=headers, data=data, auth=(CLIENT_ID, CLIENT_SECRET))
    return response.json().get("access_token")

def send_orange_sms(token, phone, message):
    # Endpoint for Orange Senegal 2.0
    url = "https://api.orange.com/smsmessaging/v1/outbound/tel%3A%2B2210000/requests"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "outboundSMSMessageRequest": {
            "address": f"tel:+{phone}",
            "senderAddress": "tel:+2210000",
            "outboundSMSTextMessage": {"message": message}
        }
    }
    return requests.post(url, json=payload, headers=headers)

# --- UI INTERFACE ---
with st.container():
    st.markdown('<div class="alert-card">', unsafe_allow_html=True)
    phone_number = st.text_input("Farmer Phone (e.g., 22177xxxxxxx)")
    msg = "Avia-Alert: Heat stress predicted in 48h. Increase ventilation now."
    
    if st.button("SEND LIFE-SAVING ALERT"):
        token = get_orange_token()
        if token:
            res = send_orange_sms(token, phone_number, msg)
            if res.status_code == 201:
                st.success("Alert sent successfully!")
            else:
                st.error(f"Error: {res.text} (Note: Subscription is still Pending)")
        else:
            st.error("Failed to retrieve token. Check your Client Secret.")
    st.markdown('</div>', unsafe_allow_html=True)
