import streamlit as st
import numpy as np
import time
import pandas as pd
import plotly.graph_objects as go

# ==========================================
# 1. PAGE SETUP & SESSION STATE
# ==========================================
st.set_page_config(page_title="AI Cuffless BP Monitor", layout="wide")

# Session state to remember calibration offsets and historical data
if 'sys_offset' not in st.session_state:
    st.session_state.sys_offset = 0.0
if 'dia_offset' not in st.session_state:
    st.session_state.dia_offset = 0.0
if 'is_calibrated' not in st.session_state:
    st.session_state.is_calibrated = False
if 'history_sys' not in st.session_state:
    st.session_state.history_sys = []
if 'history_dia' not in st.session_state:
    st.session_state.history_dia = []
if 'history_time' not in st.session_state:
    st.session_state.history_time = []

# ==========================================
# 2. AI MODEL LOADER (Mock for Cloud Deployment)
# ==========================================
@st.cache_resource
def load_ai_model():
    """Mock model for Streamlit Cloud - simulates AI predictions"""
    class MockModel:
        def predict(self, inputs, verbose=0):
            # Simulate realistic BP readings (130/80 as base)
            sys_base = 130 + np.random.normal(0, 5)
            dia_base = 80 + np.random.normal(0, 3)
            return np.array([[[sys_base, dia_base]]])
    
    return MockModel()

model = load_ai_model()

# ==========================================
# 3. HARDWARE SIMULATOR
# ==========================================
def get_sensor_data():
    """Simulate sensor data"""
    t = np.linspace(0, 4, 512)
    simulated_wave = np.sin(2 * np.pi * 1.2 * t) + np.random.normal(0, 0.05, 512)
    seq_data = simulated_wave.reshape(1, 512, 1)
    tab_data = np.array([[0.5, 0.1, 120.5, 72.0, 0.04]])
    return seq_data, tab_data

# ==========================================
# 4. SIDEBAR: CALIBRATION PANEL
# ==========================================
st.sidebar.title("⚙️ Calibration Panel")
st.sidebar.markdown("Enter the reading from a traditional arm-cuff to calibrate the AI to this specific patient's arterial health.")

true_sys = st.sidebar.number_input("True Systolic (mmHg)", min_value=60, max_value=200, value=120)
true_dia = st.sidebar.number_input("True Diastolic (mmHg)", min_value=40, max_value=130, value=80)

if st.sidebar.button("Calibrate AI"):
    seq, tab = get_sensor_data()
    preds = model.predict({"input_sequence": seq, "input_tabular": tab}, verbose=0)
    ai_base_sys = preds[0][0][0]
    ai_base_dia = preds[0][0][1]
    
    st.session_state.sys_offset = true_sys - ai_base_sys
    st.session_state.dia_offset = true_dia - ai_base_dia
    st.session_state.is_calibrated = True
    
    st.sidebar.success(f"✅ Calibrated Successfully!\n\nSys Offset: {st.session_state.sys_offset:+.1f}\nDia Offset: {st.session_state.dia_offset:+.1f}")

if not st.session_state.is_calibrated:
    st.sidebar.warning("⚠️ Device is currently uncalibrated. Readings may have high variance based on patient demographics.")

# ==========================================
# 5. MAIN DASHBOARD UI
# ==========================================
st.title("🫀 Live Cuffless Blood Pressure Monitor")
st.markdown("Powered by MAX30102 PPG & Deep Residual Networks")
st.info("📱 **Demo Version**: Using simulated sensor data. For production use, connect a real MAX30102 sensor.")

col1, col2, col3 = st.columns(3)
sys_metric = col1.empty()
dia_metric = col2.empty()
hr_metric = col3.empty()

st.subheader("Continuous Blood Pressure Trend")
chart_placeholder = st.empty()

# ==========================================
# 6. THE LIVE MONITORING LOOP
# ==========================================
if 'is_monitoring' not in st.session_state:
    st.session_state.is_monitoring = False

run_monitor = st.checkbox("Start Live Monitoring", value=st.session_state.is_monitoring)

if run_monitor != st.session_state.is_monitoring:
    st.session_state.is_monitoring = run_monitor
    
if st.session_state.is_monitoring and model is not None:
    st.info("📊 Live monitoring active. Readings update every 2 seconds...")
    
    placeholder = st.empty()
    
    for _ in range(5):
        seq, tab = get_sensor_data()
        
        preds = model.predict({"input_sequence": seq, "input_tabular": tab}, verbose=0)
        raw_sys = preds[0][0][0]
        raw_dia = preds[0][0][1]
        
        final_sys = raw_sys + st.session_state.sys_offset
        final_dia = raw_dia + st.session_state.dia_offset
        
        final_sys += np.random.uniform(-1.5, 1.5)
        final_dia += np.random.uniform(-1.0, 1.0)
        current_hr = tab[0][3] + np.random.uniform(-0.5, 0.5)

        sys_metric.metric("Systolic (mmHg)", f"{final_sys:.1f}")
        dia_metric.metric("Diastolic (mmHg)", f"{final_dia:.1f}")
        hr_metric.metric("Heart Rate (BPM)", f"{current_hr:.1f}")
        
        current_time = pd.Timestamp.now()
        st.session_state.history_time.append(current_time)
        st.session_state.history_sys.append(final_sys)
        st.session_state.history_dia.append(final_dia)
        
        if len(st.session_state.history_sys) > 50:
            st.session_state.history_time.pop(0)
            st.session_state.history_sys.pop(0)
            st.session_state.history_dia.pop(0)
            
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=st.session_state.history_time, y=st.session_state.history_sys, 
                                 mode='lines+markers', name='Systolic', line=dict(color='red', width=3)))
        fig.add_trace(go.Scatter(x=st.session_state.history_time, y=st.session_state.history_dia, 
                                 mode='lines+markers', name='Diastolic', line=dict(color='blue', width=3)))
        fig.update_layout(yaxis=dict(range=[40, 180]), margin=dict(l=0, r=0, t=30, b=0), height=400)
        
        chart_placeholder.plotly_chart(fig, use_container_width=True)
        
        time.sleep(2)
else:
    if len(st.session_state.history_sys) > 0:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=st.session_state.history_time, y=st.session_state.history_sys, 
                                 mode='lines+markers', name='Systolic', line=dict(color='red', width=3)))
        fig.add_trace(go.Scatter(x=st.session_state.history_time, y=st.session_state.history_dia, 
                                 mode='lines+markers', name='Diastolic', line=dict(color='blue', width=3)))
        fig.update_layout(yaxis=dict(range=[40, 180]), margin=dict(l=0, r=0, t=30, b=0), height=400)
        chart_placeholder.plotly_chart(fig, use_container_width=True)
    else:
        chart_placeholder.info("📈 No data yet. Start monitoring to see readings.")


