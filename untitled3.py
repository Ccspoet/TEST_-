import streamlit as st
import requests
from twilio.rest import Client

# --- BRANDING ---
st.set_page_config(page_title="Avia-Alert | Mbour", page_icon="🐔")

# --- TWILIO CONFIG (The SMS Clincher) ---
# In production, use Streamlit Secrets for these credentials
TWILIO_SID = "your_sid_here"
TWILIO_AUTH = "your_auth_token_here"
TWILIO_PHONE = "+1234567890"

def send_avia_alert(to_phone, message):
    try:
        client = Client(TWILIO_SID, TWILIO_AUTH)
        client.messages.create(body=message, from_=TWILIO_PHONE, to=to_phone)
        return True
    except:
        return False

# --- UI DESIGN ---
st.title("🐔 Avia-Alert Command Center")
st.markdown("### Hyper-local Prediction for Mbour, Senegal")

# --- 1. DATA SOURCE (Hyper-local weather) ---
# Pulling 48-hour forecast data for Mbour
city = "Mbour"
# Using a simple API for demonstration (wttr.in)
weather_url = f"https://wttr.in/{city}?format=j1"
response = requests.get(weather_url).json()
curr_temp = float(response['current_condition'][0]['temp_C'])
curr_hum = float(response['current_condition'][0]['humidity'])

# --- 2. THE PREDICTIVE "BRAIN" ---
# Temperature-Humidity Index (THI) predictive logic
thi = curr_temp + (0.55 * curr_hum / 100) * (curr_temp - 14.5) + 14.5

# --- 3. THE "WHAT, WHEN, & HOW" ---
st.subheader("Current Status")
if thi > 28:
    status = "🚨 EMERGENCY"
    instruction = "WHAT: Critical Heat Stress. WHEN: Immediate. HOW: Add electrolytes to water and increase airflow."
    color = "red"
elif thi > 26:
    status = "⚠️ WARNING"
    instruction = "WHAT: Rising Heat Stress. WHEN: Within 4 hours. HOW: Ensure all fans are active and check water levels."
    color = "orange"
else:
    status = "✅ STABLE"
    instruction = "WHAT: Conditions Normal. WHEN: 48 Hours. HOW: Standard feeding and care."
    color = "green"

st.markdown(f"<h1 style='color:{color};'>{status}</h1>", unsafe_allow_html=True)
st.info(f"**Life-Saving Instruction:** {instruction}")

# --- 4. SMS DELIVERY (Works on any phone) ---
st.divider()
st.subheader("Deliver Alert to Farmer")
farmer_phone = st.text_input("Enter Farmer Phone Number (e.g., +221...)", placeholder="+221770000000")

if st.button("SEND SMS ALERT"):
    if farmer_phone:
        success = send_avia_alert(farmer_phone, f"AVIA-ALERT: {instruction}")
        if success:
            st.success(f"Alert sent to {farmer_phone} successfully!")
        else:
            st.error("Error: Check your Twilio credentials.")
    else:
        st.warning("Please enter a phone number.")
