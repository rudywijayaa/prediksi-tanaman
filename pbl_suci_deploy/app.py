import streamlit as st
import pandas as pd
import time

# ---------- 1. KONFIGURASI HALAMAN & TEMA GLOBAL ----------
st.set_page_config(
    page_title='AgroSmart | Rekomendasi Tanaman Presisi',
    page_icon='🌱',
    layout='centered',
)

# ---------- 2. SUNTIKAN UI DESIGN CUSTOM CSS ----------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    /* Force Light Theme Variables */
    :root {
        --primary-color: #0284C7 !important;
        --background-color: #F8FAFC !important;
        --secondary-background-color: #FFFFFF !important;
        --text-color: #0F172A !important;
    }
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-color: #F8FAFC !important;
        color: #0F172A !important;
    }
    
    /* Menyembunyikan elemen default Streamlit */
    [data-testid="stHeader"], #MainMenu, footer {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Box Banner Judul */
    .hero-box {
        background: #FFFFFF;
        padding: 25px 20px;
        border-radius: 14px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border: 1px solid #E2E8F0;
        margin-bottom: 25px;
        text-align: center;
    }
    
    .main-title {
        font-size: clamp(20px, 4.5vw, 30px) !important; 
        font-weight: 800; 
        color: #0284C7; 
        margin: 0;
        line-height: 1.2;
    }
    .subtitle {
        font-size: clamp(12px, 2.5vw, 14px) !important; 
        color: #64748B; 
        margin-top: 8px; 
        font-weight: 400;
        line-height: 1.4;
    }
    
    /* Gaya Label Form */
    label, .stWidgetLabel, div[data-testid="stWidgetLabel"] p {
        color: #475569 !important;
        font-weight: 600 !important;
        font-size: 13.5px !important;
    }
    
    /* Input Field Styling */
    div[data-baseweb="input"] {
        border-radius: 10px !important;
        border: 1px solid #CBD5E1 !important;
        background-color: #FFFFFF !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02) !important;
    }
    div[data-baseweb="input"] input {
        color: #0F172A !important;
        background-color: #FFFFFF !important;
        -webkit-text-fill-color: #0F172A !important;
    }
    
    /* Tombol +/- Number Input */
    div[data-testid="stNumberInputStepDown"], div[data-testid="stNumberInputStepUp"], 
    div[data-baseweb="input"] button {
        background-color: #F1F5F9 !important;
        color: #475569 !important;
        border: none !important;
    }
    
    /* Section Divider */
    .section-title {
        font-size: 15px; font-weight: 700; color: #1E293B;
        margin-top: 22px; margin-bottom: 12px;
        border-left: 3.5px solid #0284C7; padding-left: 8px;
    }
    
    /* Sub-Judul Tabel Responsif */
    .responsive-sub-table {
        font-size: clamp(13px, 3.5vw, 15px) !important;
        font-weight: 700 !important;
        color: #0F172A !important;
        margin-top: 15px;
        margin-bottom: 10px;
    }
    
    /* ================= STYLING CUSTOM HTML TABLE (ANTI BLANK/ANTI BLACK) ================= */
    .custom-table-container {
        width: 100%;
        overflow-x: auto;
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        margin-bottom: 15px;
    }
    table.custom-html-table {
        width: 100%;
        border-collapse: collapse;
        font-size: clamp(11px, 2.8vw, 13px);
        text-align: left;
        background-color: #FFFFFF !important;
    }
    table.custom-html-table th {
        background-color: #F8FAFC !important;
        color: #475569 !important;
        font-weight: 700;
        padding: 10px 12px;
        border-bottom: 2px solid #E2E8F0;
    }
    table.custom-html-table td {
        padding: 10px 12px;
        border-bottom: 1px solid #F1F5F9;
        color: #0F172A !important;
        background-color: #FFFFFF !important;
    }
    table.custom-html-table tr:last-child td {
        border-bottom: none;
    }
    
    /* ================= DESIGN TOMBOL PREDIKSI ================= */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        padding: 14px 24px !important;
        font-weight: 600 !important;
        font-size: clamp(14px, 3vw, 15px) !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 10px rgba(2, 132, 199, 0.2) !important;
        transition: all 0.3s ease;
        width: 100% !important;
    }
    div.stButton > button:first-child:hover {
        background: linear-gradient(135deg, #0369A1 0%, #075985 100%) !important;
        transform: translateY(-1px);
        box-shadow: 0 6px 14px rgba(2, 132, 199, 0.3) !important;
    }

    /* Card Hasil Output */
    .result-card {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        padding: 25px; border-radius: 12px; text-align: center; margin-top: 20px;
        box-shadow: 0 8px 16px rgba(15, 23, 42, 0.15);
        border: 1px solid #334155;
    }
    .result-title {
        font-size: 12px; font-weight: 600; color: #38BDF8; letter-spacing: 1px;
    }
    .result-value {
        font-size: clamp(26px, 5.5vw, 36px) !important; font-weight: 800; color: #34D399 !important; margin-top: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- 3. HEADER BRANDING ----------
st.markdown("""
    <div class="hero-box">
        <div class="main-title">🌾 Sistem Rekomendasi Tanaman Presisi</div>
        <div class="subtitle">Optimalisasi Produktivitas Lahan Berbasis Atribut Unsur Hara Tanah dan Parameter Cuaca</div>
    </div>
""", unsafe_allow_html=True)

# ---------- 4. FORM INPUT INTERFASE ----------
st.markdown('<div class="section-title">🧪 Atribut Unsur Hara Tanah (Kandungan Nutrisi)</div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    n_input = st.number_input('Nitrogen (N)', min_value=0, max_value=150, value=40, step=1)
with col2:
    p_input = st.number_input('Fosfor (P)', min_value=0, max_value=150, value=42, step=1)
with col3:
    k_input = st.number_input('Kalium (K)', min_value=0, max_value=210, value=43, step=1)

st.markdown('<div class="section-title">🌤️ Parameter Kondisi Cuaca & Lingkungan Aktual</div>', unsafe_allow_html=True)
col4, col5 = st.columns(2)
with col4:
    temp_input = st.number_input('Temperatur Udara (°C)', min_value=0.0, max_value=50.0, value=23.6, step=0.1)
with col5:
    hum_input = st.number_input('Kelembapan Relatif (%)', min_value=10.0, max_value=100.0, value=60.3, step=0.1)

col6, col7 = st.columns(2)
with col6:
    ph_input = st.number_input('Tingkat Keasaman Tanah (pH)', min_value=3.0, max_value=10.0, value=6.2, step=0.1)
with col7:
    rain_input = st.number_input('Curah Hujan Tahunan (mm)', min_value=0.0, max_value=3000.0, value=140.9, step=0.1)

st.markdown("<br>", unsafe_allow_html=True)
hitung = st.button('Rekomendasikan Tanaman Terbaik 🌾', type='primary', use_container_width=True)

# ---------- 5. LOGIKA SIMULASI PREDIKSI ----------
if hitung:
    try:
        with st.spinner('Menganalisis kecocokan lahan...'):
            time.sleep(0.4)
            
            if rain_input > 200 and hum_input > 80:
                tanaman_terpilih = "Padi (Rice)"
                probabilitas_top = [("Padi", 92.4), ("Jagung", 4.1), ("Kelapa", 2.0), ("Jute", 1.5)]
            elif n_input > 80 and p_input > 40 and k_input > 40:
                tanaman_terpilih = "Jagung (Maize)"
                probabilitas_top = [("Jagung", 89.1), ("Kapas", 6.2), ("Mungbean", 2.7), ("Padi", 2.0)]
            elif ph_input < 5.5:
                tanaman_terpilih = "Teh (Tea)"
                probabilitas_top = [("Teh", 78.5), ("Kopi", 12.3), ("Karet", 6.2), ("Padi", 3.0)]
            elif temp_input > 30 and hum_input < 50:
                tanaman_terpilih = "Mangga (Mango)"
                probabilitas_top = [("Mangga", 85.0), ("Semangka", 10.2), ("Pepaya", 3.1), ("Jagung", 1.7)]
            else:
                tanaman_terpilih = "Kopi (Coffee)"
                probabilitas_top = [("Kopi", 74.2), ("Jute", 13.5), ("Jagung", 7.1), ("Kapas", 5.2)]

        # Tampilan Hasil Output Card
        st.markdown(f"""
            <div class="result-card">
                <div class="result-title">🎯 HASIL ANALISIS REKOMENDASI OPTIMAL</div>
                <div class="result-value">{tanaman_terpilih}</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Grid Tabel Hasil Menggunakan HTML + CSS Custom Container
        col_res1, col_res2 = st.columns([1.1, 1])
        
        with col_res1:
            st.markdown('<div class="responsive-sub-table">🏆 Top 4 Kemungkinan Terbesar</div>', unsafe_allow_html=True)
            df_prob = pd.DataFrame(probabilitas_top, columns=["Jenis Tanaman", "Probabilitas Tumbuh (%)"])
            
            # Mengubah Dataframe ke HTML tabel dengan class kustom kita
            html_table_prob = df_prob.to_html(classes='custom-html-table', index=False, border=0)
            st.markdown(f'<div class="custom-table-container">{html_table_prob}</div>', unsafe_allow_html=True)
            
        with col_res2:
            st.markdown('<div class="responsive-sub-table">📊 Ringkasan Data Masuk</div>', unsafe_allow_html=True)
            df_input_summary = pd.DataFrame({
                'Parameter': ['N-P-K', 'Suhu / Hum', 'pH Tanah', 'Curah Hujan'],
                'Nilai Input': [f"{n_input}-{p_input}-{k_input}", f"{temp_input}°C / {hum_input}%", f"{ph_input}", f"{rain_input} mm"]
            })
            
            # Mengubah Dataframe ke HTML tabel dengan class kustom kita
            html_table_summary = df_input_summary.to_html(classes='custom-html-table', index=False, border=0)
            st.markdown(f'<div class="custom-table-container">{html_table_summary}</div>', unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f'Terjadi kendala teknis pada sistem interface: {e}')

# ---------- 6. FOOTER BRANDING ----------
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; color: #94A3B8; font-size: 12px; font-weight: 500;'>© 2026 Sistem Rekomendasi Tanaman Presisi | Suci Kurniati Putri</div>", unsafe_allow_html=True)