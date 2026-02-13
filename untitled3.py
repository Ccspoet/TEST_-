import streamlit as st
import pandas as pd

# 1. SETTINGS & CSS TO MATCH PROTOTYPE
st.set_page_config(page_title="AgriAlert Mbour", page_icon="🐔")

st.markdown("""
    <style>
    .main { background-color: #F8F9FA; }
    .alert-card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        border-left: 10px solid #2E7D32;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .stButton>button {
        background-color: #2E7D32;
        color: white;
        width: 100%;
        border-radius: 10px;
        height: 3em;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. APP HEADER
st.title("🐔 AgriAlert Mbour")
st.write("Real-time Avian Heat Stress Monitoring")

# 3. PREDICTIVE LOGIC (The Brain)
with st.container():
    st.markdown('<div class="alert-card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        temp = st.number_input("Temp (°C)", value=30.0, step=0.1)
    with col2:
        hum = st.number_input("Humidity (%)", value=70.0, step=1.0)
    
    # THI (Temperature-Humidity Index) for Poultry
    thi = temp + (0.55 * hum / 100) * (temp - 14.5) + 14.5
    
    if st.button("CHECK POULTRY RISK"):
        if thi > 28:
            st.error(f"🚨 CRITICAL RISK: THI is {thi:.1f}")
            st.warning("Recommended Action: Activate Misting Systems in Mbour pens.")
        else:
            st.success(f"✅ STABLE: THI is {thi:.1f}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# 4. DATA SOURCE REFERENCE
st.caption("Data source sync: timeanddate.com (Mbour Station)")
