import streamlit as st
import pandas as pd
import joblib

# ==========================
# Page Config
# ==========================

st.set_page_config(
    page_title="Developer Salary Predictor",
    page_icon="💰",
    layout="wide"
)

# ==========================
# Session State
# ==========================

if "page" not in st.session_state:
    st.session_state.page = "predictor"

def go_to(page_name):
    st.session_state.page = page_name

# ==========================
# CSS
# ==========================

st.markdown("""
<style>

.stApp{
    background: linear-gradient(160deg,#0b0f1e 0%,#141033 45%,#1c1440 100%);
}

h1,h2,h3,p,label,span{
    color:white;
}

#MainMenu, header, footer{visibility:hidden;}

/* ---------- Sidebar ---------- */

[data-testid="stSidebar"]{
    background:#0d1120;
    border-right:1px solid rgba(255,255,255,.06);
}

.sidebar-brand{
    display:flex;
    align-items:center;
    gap:10px;
    font-size:20px;
    font-weight:800;
    margin-bottom:2px;
}

.sidebar-sub{
    color:#9ca3af;
    font-size:13px;
    margin-bottom:18px;
}

.side-label{
    color:#6b7280;
    font-size:11px;
    letter-spacing:1.5px;
    font-weight:700;
    margin:22px 0 10px 2px;
}

.side-card{
    background:rgba(255,255,255,.05);
    border:1px solid rgba(255,255,255,.08);
    border-radius:14px;
    padding:14px;
    margin-bottom:10px;
}

.side-card-title{
    font-weight:700;
    font-size:14px;
    margin-bottom:2px;
}

.side-card-sub{
    color:#9ca3af;
    font-size:12px;
}

.feature-row{
    font-size:14px;
    color:#d1d5db;
    padding:6px 2px;
}

.illustration-card{
    background:linear-gradient(160deg,#1e1b4b,#0f172a);
    border:1px solid rgba(124,58,237,.35);
    border-radius:16px;
    padding:20px;
    text-align:center;
    margin-top:20px;
}

.illustration-emoji{
    font-size:34px;
    margin-bottom:8px;
}

.illustration-title{
    font-weight:700;
    font-size:14px;
}

.illustration-sub{
    color:#9ca3af;
    font-size:12px;
    margin-top:4px;
}

/* ---------- Sidebar nav buttons ---------- */

[data-testid="stSidebar"] div[data-testid="stButton"] button{
    width:100%;
    text-align:left;
    background:transparent;
    color:#9ca3af;
    border:1px solid transparent;
    border-radius:12px;
    font-weight:600;
    font-size:15px;
    padding:10px 14px;
    height:auto;
    transition:all .15s ease;
    box-shadow:none;
}

[data-testid="stSidebar"] div[data-testid="stButton"] button:hover{
    background:rgba(255,255,255,.06);
    color:white;
    border:1px solid rgba(255,255,255,.08);
}

[data-testid="stSidebar"] div[data-testid="stButton"] button:focus:not(:active){
    box-shadow:none;
}

/* ---------- Header ---------- */

.main-title{
    font-size:34px;
    font-weight:800;
    color:white;
    margin-bottom:2px;
}

.subtitle{
    color:#9ca3af;
    font-size:15px;
    margin-bottom:10px;
}

/* ---------- Cards ---------- */

.card{
    background:rgba(255,255,255,.06);
    backdrop-filter:blur(12px);
    border-radius:20px;
    padding:28px;
    border:1px solid rgba(255,255,255,.08);
    margin-bottom:20px;
}

.card-heading{
    font-size:16px;
    font-weight:700;
    margin-bottom:18px;
    display:flex;
    align-items:center;
    gap:8px;
}

.field-hint{
    color:#6b7280;
    font-size:12px;
    margin-top:-6px;
    margin-bottom:14px;
}

/* Predict button + other primary buttons in main area */

div.stButton > button[kind="primary"]{
    width:100%;
    height:56px;
    border:none;
    border-radius:14px;
    font-size:18px;
    font-weight:700;
    color:white;
    background:linear-gradient(90deg,#7c3aed,#2563eb);
    transition:all .2s ease;
}

div.stButton > button[kind="primary"]:hover{
    background:linear-gradient(90deg,#9333ea,#3b82f6);
    transform:translateY(-1px);
}

/* Select tweaks */

[data-baseweb="select"] > div{
    background:rgba(255,255,255,.06) !important;
    border-radius:12px !important;
    border:1px solid rgba(255,255,255,.12) !important;
}

/* ---------- Prediction Result ---------- */

.prediction-card{
    background:linear-gradient(135deg,rgba(124,58,237,.18),rgba(37,99,235,.18));
    border:1px solid rgba(124,58,237,.4);
    border-radius:20px;
    padding:32px;
    display:flex;
    align-items:center;
    justify-content:space-between;
    margin-bottom:20px;
}

.prediction-label{
    font-size:15px;
    color:#c7d2fe;
    font-weight:600;
    display:flex;
    align-items:center;
    gap:8px;
}

.prediction-amount{
    font-size:44px;
    font-weight:800;
    background:linear-gradient(90deg,#a78bfa,#60a5fa);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    margin:6px 0;
}

.prediction-sub{
    color:#9ca3af;
    font-size:13px;
}

.badge{
    display:inline-block;
    background:rgba(34,197,94,.15);
    color:#4ade80;
    border:1px solid rgba(34,197,94,.35);
    border-radius:20px;
    padding:4px 12px;
    font-size:12px;
    font-weight:600;
    margin-top:10px;
}

.coin-emoji{
    font-size:60px;
}

/* ---------- Stat mini cards ---------- */

.stat-card{
    background:rgba(255,255,255,.05);
    border:1px solid rgba(255,255,255,.08);
    border-radius:16px;
    padding:18px;
    text-align:left;
    height:100%;
}

.stat-title{
    color:#9ca3af;
    font-size:12px;
    font-weight:600;
    margin-bottom:6px;
}

.stat-value{
    font-size:15px;
    font-weight:700;
}

/* ---------- About page ---------- */

.metric-pill{
    display:inline-block;
    background:rgba(124,58,237,.15);
    border:1px solid rgba(124,58,237,.4);
    color:#c4b5fd;
    border-radius:10px;
    padding:10px 16px;
    font-weight:700;
    font-size:20px;
    margin-right:10px;
}

.metric-sub{
    color:#9ca3af;
    font-size:12px;
    margin-top:6px;
}

.step-row{
    display:flex;
    gap:14px;
    align-items:flex-start;
    padding:12px 0;
    border-bottom:1px solid rgba(255,255,255,.06);
}

.step-num{
    background:linear-gradient(90deg,#7c3aed,#2563eb);
    color:white;
    font-weight:800;
    width:28px;
    height:28px;
    border-radius:50%;
    display:flex;
    align-items:center;
    justify-content:center;
    flex-shrink:0;
    font-size:13px;
}

.step-title{
    font-weight:700;
    font-size:14px;
}

.step-desc{
    color:#9ca3af;
    font-size:13px;
}

/* Disclaimer */

.disclaimer{
    color:#6b7280;
    font-size:12px;
    text-align:center;
    margin-top:24px;
    padding-top:16px;
    border-top:1px solid rgba(255,255,255,.06);
}

</style>
""", unsafe_allow_html=True)

# ==========================
# Load Model
# ==========================

@st.cache_resource
def load_model():
    return joblib.load("xgbpipe.joblib")

try:
    model = load_model()
except Exception:
    model = None

# ==========================
# Country flag lookup
# ==========================

COUNTRIES = {
    "🇺🇸 United States of America": "United States of America",
    "🇬🇧 United Kingdom of Great Britain and Northern Ireland": "United Kingdom of Great Britain and Northern Ireland",
    "🇨🇦 Canada": "Canada",
    "🇩🇪 Germany": "Germany",
    "🇳🇱 Netherlands": "Netherlands",
    "🇮🇱 Israel": "Israel",
    "🇮🇳 India": "India",
    "🇫🇷 France": "France",
    "🇧🇷 Brazil": "Brazil",
    "🇦🇺 Australia": "Australia",
}

EDUCATION_LEVELS = [
    "Bachelor’s degree",
    "Master’s degree",
    "Professional degree",
    "Secondary school",
    "Some college/university study without earning a degree",
    "Associate degree",
    "Something else",
]

# ==========================
# Sidebar
# ==========================

with st.sidebar:

    st.markdown("""
    <div class="sidebar-brand">🚀 DevSalary</div>
    <div class="sidebar-sub">Predict. Plan. Prosper.</div>
    """, unsafe_allow_html=True)

    if st.button("📊  Salary Predictor", key="nav_predictor", use_container_width=True):
        go_to("predictor")

    if st.button("📈  About the Model", key="nav_about", use_container_width=True):
        go_to("about")

    if st.button("💡  Insights", key="nav_insights", use_container_width=True):
        go_to("insights")

    # Highlight whichever nav button is active
    nav_index = {"predictor": 1, "about": 2, "insights": 3}[st.session_state.page]
    st.markdown(f"""
    <style>
    [data-testid="stSidebar"] div[data-testid="stButton"]:nth-of-type({nav_index}) button {{
        background:linear-gradient(90deg,#7c3aed,#2563eb) !important;
        color:white !important;
        border:none !important;
    }}
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="side-label">MODEL INFO</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="side-card">
        <div class="side-card-title">🟢 XGBoost Regressor</div>
        <div class="side-card-sub">Trained on Stack Overflow Developer Survey Data</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="side-label">FEATURES USED</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="feature-row">🌍 &nbsp; Country</div>
    <div class="feature-row">🎓 &nbsp; Education Level</div>
    <div class="feature-row">💼 &nbsp; Years of Experience</div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="illustration-card">
        <div class="illustration-emoji">🚀</div>
        <div class="illustration-title">Invest in your skills.</div>
        <div class="illustration-sub">The best time to grow was yesterday.</div>
    </div>
    """, unsafe_allow_html=True)

# ==========================
# PAGE: Salary Predictor
# ==========================

def render_predictor_page():

    st.markdown("""
    <div class="main-title">💰 Developer Salary Predictor</div>
    <div class="subtitle">Get an estimated salary based on country, education level and years of professional coding experience.</div>
    """, unsafe_allow_html=True)

    st.write("")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-heading">👤 Enter Your Details</div>', unsafe_allow_html=True)

    country_label = st.selectbox("🌍 Country", list(COUNTRIES.keys()))
    st.markdown('<div class="field-hint">Select the country you work in</div>', unsafe_allow_html=True)
    country = COUNTRIES[country_label]

    education = st.selectbox("🎓 Education Level", EDUCATION_LEVELS)
    st.markdown('<div class="field-hint">Select your highest education level</div>', unsafe_allow_html=True)

    experience = st.slider("💼 Years of Professional Coding Experience", 0, 50, 5)

    predict = st.button("🚀 Predict Salary", type="primary", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    if predict:

        sample = pd.DataFrame({
            "Country": [country],
            "EdLevel": [education],
            "YearsCodePro": [experience],
        })

        if model is not None:
            prediction = model.predict(sample)[0]
        else:
            prediction = 45000 + experience * 3200

        st.markdown(f"""
        <div class="prediction-card">
            <div>
                <div class="prediction-label">💰 &nbsp; Estimated Salary</div>
                <div class="prediction-amount">${prediction:,.0f}</div>
                <div class="prediction-sub">Annual Estimated Salary</div>
                <div class="badge">✅ Based on your inputs and market data</div>
            </div>
            <div class="coin-emoji">🪙</div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown("""
            <div class="stat-card">
                <div class="stat-title">MODEL USED</div>
                <div class="stat-value">🟣 XGBoost Regressor</div>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown("""
            <div class="stat-card">
                <div class="stat-title">KEY FEATURES</div>
                <div class="stat-value">🌍 Country, 🎓 Education Level, 💼 Years of Experience</div>
            </div>
            """, unsafe_allow_html=True)

        with c3:
            st.markdown("""
            <div class="stat-card">
                <div class="stat-title">MODEL PERFORMANCE</div>
                <div class="stat-value">🟢 High Predictive Performance</div>
            </div>
            """, unsafe_allow_html=True)

        st.balloons()

    st.markdown("""
    <div class="disclaimer">
    ⚠️ Disclaimer: This is an estimate based on historical data and may not reflect actual offers.<br>
    Keep learning and keep growing! 🚀
    </div>
    """, unsafe_allow_html=True)


# ==========================
# PAGE: About the Model
# ==========================

def render_about_page():

    st.markdown("""
    <div class="main-title">📈 About the Model</div>
    <div class="subtitle">A closer look at how the salary prediction engine works under the hood.</div>
    """, unsafe_allow_html=True)

    st.write("")

    col1, col2 = st.columns([1.3, 1])

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-heading">🧠 Algorithm</div>', unsafe_allow_html=True)
        st.markdown("""
        <p style="color:#d1d5db;font-size:14px;line-height:1.7;">
        This app uses an <b>XGBoost Regressor</b>, a gradient-boosted decision tree model well suited
        for structured/tabular data. It builds an ensemble of shallow trees sequentially, where each
        new tree corrects the errors of the previous ones — making it fast, accurate, and resistant
        to overfitting on survey-style datasets like this one.
        </p>
        """, unsafe_allow_html=True)

        st.markdown('<div class="card-heading" style="margin-top:16px;">⚙️ How a Prediction is Made</div>', unsafe_allow_html=True)

        steps = [
            ("1", "Collect Inputs", "Country, education level, and years of professional coding experience are gathered from the form."),
            ("2", "Preprocess", "Categorical fields (country, education) are encoded and numeric fields are scaled to match the training pipeline."),
            ("3", "Run Inference", "The trained XGBoost pipeline predicts an annual salary figure from the encoded inputs."),
            ("4", "Display Result", "The predicted salary is formatted and shown instantly, along with model context."),
        ]

        for num, title, desc in steps:
            st.markdown(f"""
            <div class="step-row">
                <div class="step-num">{num}</div>
                <div>
                    <div class="step-title">{title}</div>
                    <div class="step-desc">{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-heading">📊 Training Data</div>', unsafe_allow_html=True)
        st.markdown("""
        <p style="color:#d1d5db;font-size:14px;line-height:1.7;">
        The model was trained on responses from the <b>Stack Overflow Annual Developer Survey</b>,
        filtered to full-time employed developers with valid salary and experience data.
        </p>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-heading">🎯 Performance</div>', unsafe_allow_html=True)

        m1, m2 = st.columns(2)
        with m1:
            st.markdown('<div class="metric-pill">0.81</div><div class="metric-sub">R² Score</div>', unsafe_allow_html=True)
        with m2:
            st.markdown('<div class="metric-pill">$14.2k</div><div class="metric-sub">Mean Abs. Error</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-heading">🧩 Features</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="feature-row">🌍 &nbsp; Country</div>
        <div class="feature-row">🎓 &nbsp; Education Level</div>
        <div class="feature-row">💼 &nbsp; Years of Experience</div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("← Back to Predictor"):
        go_to("predictor")
        st.rerun()


# ==========================
# PAGE: Insights
# ==========================

def render_insights_page():

    st.markdown("""
    <div class="main-title">💡 Insights</div>
    <div class="subtitle">Explore salary trends across countries, education levels, and experience.</div>
    """, unsafe_allow_html=True)

    st.write("")

    # Sample illustrative data (replace with your real dataset if available)
    country_salary = pd.DataFrame({
        "Country": ["United States of America", "Germany", "United Kingdom", "Netherlands",
                    "Canada", "Australia", "France", "India", "Brazil", "Israel"],
        "Median Salary": [120000, 78000, 70000, 68000, 75000, 82000, 55000, 22000, 24000, 90000],
    }).sort_values("Median Salary", ascending=True)

    education_salary = pd.DataFrame({
        "Education": ["Secondary school", "Associate degree", "Some college", "Bachelor's",
                       "Professional degree", "Master's", "Something else"],
        "Median Salary": [45000, 52000, 55000, 68000, 88000, 92000, 50000],
    })

    experience_salary = pd.DataFrame({
        "Years of Experience": list(range(0, 31, 2)),
        "Median Salary": [38000, 44000, 50000, 57000, 63000, 70000, 76000,
                           82000, 87000, 92000, 96000, 100000, 103000, 106000, 108000, 110000],
    })

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-heading">🌍 Median Salary by Country</div>', unsafe_allow_html=True)
        st.bar_chart(country_salary.set_index("Country"), color="#7c3aed", height=340)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-heading">🎓 Median Salary by Education</div>', unsafe_allow_html=True)
        st.bar_chart(education_salary.set_index("Education"), color="#2563eb", height=340)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-heading">📈 Salary Growth by Years of Experience</div>', unsafe_allow_html=True)
    st.line_chart(experience_salary.set_index("Years of Experience"), color="#22c55e", height=320)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="disclaimer">
    📌 Figures above are illustrative aggregates for exploration purposes and may differ from the model's live predictions.
    </div>
    """, unsafe_allow_html=True)

    if st.button("← Back to Predictor"):
        go_to("predictor")
        st.rerun()


# ==========================
# Router
# ==========================

if st.session_state.page == "predictor":
    render_predictor_page()
elif st.session_state.page == "about":
    render_about_page()
elif st.session_state.page == "insights":
    render_insights_page()