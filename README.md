# 🫀 AI Cuffless Blood Pressure Monitor

A Streamlit dashboard powered by MAX30102 PPG sensors and Deep Residual Networks for blood pressure monitoring without an arm cuff.

## 📋 Features

- **Live Blood Pressure Monitoring**: Real-time systolic and diastolic readings
- **AI Calibration**: Personalized calibration based on traditional cuff readings
- **Historical Tracking**: 50-reading history with interactive Plotly charts
- **Responsive UI**: Built with Streamlit and Plotly for smooth interactions

## 🚀 Local Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the app:
```bash
streamlit run app.py
```

3. Open in browser: `http://localhost:8501`

## 🌐 Deploy to Streamlit Cloud

1. **Initialize Git repository:**
```bash
git init
git add .
git commit -m "Initial commit"
```

2. **Create GitHub repository:**
   - Go to [github.com](https://github.com) and create a new public repository
   - Push your code:
```bash
git remote add origin https://github.com/YOUR_USERNAME/blood_pressure_model.git
git branch -M main
git push -u origin main
```

3. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your GitHub repository and `app.py` as the main file
   - Click "Deploy"

## 📁 Files

- `app.py` - Entry point for Streamlit
- `dashboard.py` - Main dashboard application
- `max30102_bp_model.keras` - Pre-trained TensorFlow/Keras model
- `requirements.txt` - Python dependencies

## ⚙️ Calibration

1. Get a reading from a traditional arm-cuff blood pressure monitor
2. Enter the systolic and diastolic values in the Calibration Panel
3. Click "Calibrate AI"
4. The system will calculate personalized offsets for accurate readings

## 📊 Live Monitoring

1. Click "Start Live Monitoring" checkbox
2. The dashboard will update every 1.5 seconds
3. Uncheck to stop monitoring
4. Historical data is displayed in the interactive chart

## 🛠️ Future Enhancements

- Connect real MAX30102 sensor via PySerial
- Add data export functionality (CSV/PDF)
- Implement user profiles for multiple patients
- Add risk assessment based on BP trends

---

**Note:** This is a demonstration application. For medical use, consult healthcare professionals and validate with clinical studies.
