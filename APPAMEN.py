import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# ══════════════════════════════════════════════════════════════
#  CONFIGURATION PAGE
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Amendis — Prévision Électrique",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════════════
#  CSS DESIGN SAAS PREMIUM
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

    * { box-sizing: border-box; }

    /* ── Fond & police ── */
    .stApp {
        background: #080c14;
        font-family: 'DM Sans', sans-serif;
    }

    /* ── Grille de fond subtile ── */
    .stApp::before {
        content: '';
        position: fixed;
        inset: 0;
        background-image:
            linear-gradient(rgba(0,212,255,0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0,212,255,0.03) 1px, transparent 1px);
        background-size: 40px 40px;
        pointer-events: none;
        z-index: 0;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: #0d1117 !important;
        border-right: 1px solid rgba(255,255,255,0.06) !important;
    }
    [data-testid="stSidebar"] > div {
        padding-top: 0 !important;
    }

    /* ── Header sidebar logo ── */
    .sb-logo {
        padding: 28px 20px 20px;
        border-bottom: 1px solid rgba(255,255,255,0.06);
        margin-bottom: 16px;
    }
    .sb-logo-badge {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        background: linear-gradient(135deg, rgba(0,212,255,0.15), rgba(0,212,255,0.05));
        border: 1px solid rgba(0,212,255,0.25);
        border-radius: 10px;
        padding: 10px 14px;
        width: 100%;
    }
    .sb-logo-icon {
        font-size: 1.4rem;
        line-height: 1;
    }
    .sb-logo-text h3 {
        margin: 0;
        font-size: 0.95rem;
        font-weight: 700;
        color: #e2e8f0;
        letter-spacing: 0.02em;
    }
    .sb-logo-text p {
        margin: 2px 0 0;
        font-size: 0.7rem;
        color: #00d4ff;
        font-family: 'Space Mono', monospace;
        letter-spacing: 0.05em;
    }

    /* ── Navigation pills ── */
    [data-testid="stRadio"] label {
        display: flex !important;
        align-items: center !important;
        padding: 9px 14px !important;
        border-radius: 8px !important;
        transition: all 0.2s !important;
        cursor: pointer !important;
        color: #8892b0 !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        margin: 2px 0 !important;
    }
    [data-testid="stRadio"] label:hover {
        background: rgba(0,212,255,0.06) !important;
        color: #cdd6f4 !important;
    }
    div[data-baseweb="radio"] [aria-checked="true"] + label,
    div[data-baseweb="radio"] input:checked ~ label {
        background: rgba(0,212,255,0.1) !important;
        color: #00d4ff !important;
        border-left: 2px solid #00d4ff !important;
    }

    /* ── Cards KPI ── */
    .kpi-card {
        background: #0d1117;
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 14px;
        padding: 22px 20px;
        position: relative;
        overflow: hidden;
        transition: border-color 0.2s, transform 0.2s;
    }
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, var(--accent, #00d4ff), transparent);
    }
    .kpi-card:hover {
        border-color: rgba(0,212,255,0.2);
        transform: translateY(-1px);
    }
    .kpi-icon {
        font-size: 1.2rem;
        margin-bottom: 10px;
        display: block;
    }
    .kpi-value {
        font-size: 1.7rem;
        font-weight: 700;
        color: #e2e8f0;
        letter-spacing: -0.02em;
        line-height: 1.2;
        font-family: 'Space Mono', monospace;
    }
    .kpi-label {
        font-size: 0.75rem;
        color: #636e8a;
        margin-top: 5px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    .kpi-accent { color: var(--accent, #00d4ff); }

    /* ── Section headers ── */
    .sh {
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 28px 0 16px;
        padding-bottom: 10px;
        border-bottom: 1px solid rgba(255,255,255,0.06);
    }
    .sh-bar {
        width: 3px;
        height: 18px;
        background: #00d4ff;
        border-radius: 2px;
        flex-shrink: 0;
    }
    .sh-title {
        font-size: 0.9rem;
        font-weight: 600;
        color: #cdd6f4;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }
    .sh-badge {
        margin-left: auto;
        background: rgba(0,212,255,0.1);
        color: #00d4ff;
        font-size: 0.7rem;
        font-family: 'Space Mono', monospace;
        padding: 3px 9px;
        border-radius: 20px;
        border: 1px solid rgba(0,212,255,0.2);
    }

    /* ── Metric containers natifs ── */
    [data-testid="metric-container"] {
        background: #0d1117;
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 10px;
        padding: 14px 16px;
    }
    [data-testid="metric-container"] label {
        color: #636e8a !important;
        font-size: 0.72rem !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #e2e8f0 !important;
        font-family: 'Space Mono', monospace;
        font-size: 1.3rem !important;
    }

    /* ── Boutons ── */
    .stButton > button {
        background: rgba(0,212,255,0.08) !important;
        color: #00d4ff !important;
        border: 1px solid rgba(0,212,255,0.3) !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.83rem !important;
        letter-spacing: 0.03em !important;
        padding: 8px 18px !important;
        transition: all 0.2s !important;
        font-family: 'DM Sans', sans-serif !important;
    }
    .stButton > button:hover {
        background: rgba(0,212,255,0.15) !important;
        border-color: rgba(0,212,255,0.6) !important;
        box-shadow: 0 0 20px rgba(0,212,255,0.2) !important;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        background: transparent;
        border-bottom: 1px solid rgba(255,255,255,0.07);
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: #636e8a !important;
        font-size: 0.82rem !important;
        font-weight: 500 !important;
        border: none !important;
        border-bottom: 2px solid transparent !important;
        border-radius: 0 !important;
        padding: 10px 16px !important;
        transition: all 0.15s;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #cdd6f4 !important;
        background: rgba(255,255,255,0.03) !important;
    }
    .stTabs [aria-selected="true"] {
        color: #00d4ff !important;
        border-bottom-color: #00d4ff !important;
    }

    /* ── Tables ── */
    [data-testid="stDataFrame"] {
        border: 1px solid rgba(255,255,255,0.07) !important;
        border-radius: 10px !important;
        overflow: hidden !important;
    }

    /* ── Inputs ── */
    [data-testid="stSlider"] > div,
    [data-testid="stSelectbox"] > div {
        background: transparent;
    }
    .stSlider [data-testid="stMarkdownContainer"] p {
        font-size: 0.78rem;
        color: #8892b0;
    }

    /* ── Expanders ── */
    [data-testid="stExpander"] {
        background: #0d1117 !important;
        border: 1px solid rgba(255,255,255,0.07) !important;
        border-radius: 8px !important;
    }
    [data-testid="stExpander"] summary {
        font-size: 0.82rem !important;
        color: #8892b0 !important;
        font-weight: 600 !important;
    }

    /* ── Séparateur sidebar ── */
    .sb-sep {
        height: 1px;
        background: rgba(255,255,255,0.06);
        margin: 12px 0;
    }
    .sb-section-label {
        font-size: 0.65rem;
        color: #3d4460;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 700;
        padding: 4px 0;
    }

    /* ── Page titles ── */
    .page-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #e2e8f0;
        letter-spacing: -0.02em;
        margin-bottom: 4px;
    }
    .page-subtitle {
        font-size: 0.82rem;
        color: #636e8a;
        margin-bottom: 24px;
        font-weight: 400;
    }

    /* ── Status badges ── */
    .badge-green {
        display: inline-block;
        background: rgba(0,255,136,0.1);
        color: #00ff88;
        border: 1px solid rgba(0,255,136,0.2);
        border-radius: 20px;
        font-size: 0.7rem;
        padding: 3px 10px;
        font-family: 'Space Mono', monospace;
    }
    .badge-blue {
        display: inline-block;
        background: rgba(0,212,255,0.1);
        color: #00d4ff;
        border: 1px solid rgba(0,212,255,0.2);
        border-radius: 20px;
        font-size: 0.7rem;
        padding: 3px 10px;
        font-family: 'Space Mono', monospace;
    }
    .badge-orange {
        display: inline-block;
        background: rgba(255,165,2,0.1);
        color: #ffa502;
        border: 1px solid rgba(255,165,2,0.2);
        border-radius: 20px;
        font-size: 0.7rem;
        padding: 3px 10px;
        font-family: 'Space Mono', monospace;
    }

    /* ── Divider ── */
    hr { border-color: rgba(255,255,255,0.06) !important; }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: #080c14; }
    ::-webkit-scrollbar-thumb { background: #1e2130; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #2d3748; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  HELPERS VISUELS
# ══════════════════════════════════════════════════════════════
def sh(title, badge=None):
    b = f'<span class="sh-badge">{badge}</span>' if badge else ''
    st.markdown(f"""
    <div class="sh">
        <div class="sh-bar"></div>
        <span class="sh-title">{title}</span>
        {b}
    </div>""", unsafe_allow_html=True)

def kpi(value, label, accent="#00d4ff", icon=""):
    st.markdown(f"""
    <div class="kpi-card" style="--accent:{accent}">
        <span class="kpi-icon">{icon}</span>
        <div class="kpi-value">{value}</div>
        <div class="kpi-label">{label}</div>
    </div>""", unsafe_allow_html=True)

THEME = dict(
    template='plotly_dark',
    paper_bgcolor='#0d1117',
    plot_bgcolor='#0d1117',
    font=dict(family='DM Sans', color='#8892b0', size=12),
    margin=dict(l=10, r=10, t=40, b=10),
)

COLOR_MAIN    = '#00d4ff'
COLOR_WARN    = '#ffa502'
COLOR_SUCCESS = '#00ff88'
COLOR_DANGER  = '#ff4757'
COLOR_PURPLE  = '#a855f7'
PALETTE       = [COLOR_MAIN, COLOR_WARN, COLOR_SUCCESS, COLOR_PURPLE, COLOR_DANGER]

# ══════════════════════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════════════════════
for key in ['df','df_processed','models_results','best_model',
            'clusters_df','predictions_df','features_list',
            'X_train','X_test','y_train','y_test']:
    if key not in st.session_state:
        st.session_state[key] = None

# ══════════════════════════════════════════════════════════════
#  FONCTIONS MÉTIER
# ══════════════════════════════════════════════════════════════
@st.cache_data
def load_data(file):
    try:
        return pd.read_excel(file)
    except Exception as e:
        st.error(f"Erreur chargement : {e}")
        return None

@st.cache_data
def compute_features(_df):
    df = _df.copy().fillna(0)
    df = df.sort_values(['N° Client','Mois']).reset_index(drop=True)
    tranche_enc = {'T1 (0-100 kWh)':0,'T2 (101-150 kWh)':1,
                   'T3 (151-210 kWh)':2,'T4 (211-310 kWh)':3,
                   'T5 (311-510 kWh)':4,'T6 (>510 kWh)':5}
    df['tranche_enc'] = df['Tranche'].map(tranche_enc).fillna(0).astype(int)
    grp = df.groupby('N° Client')['Consommation (kWh)']
    df['lag_1']       = grp.shift(1).fillna(0)
    df['lag_2']       = grp.shift(2).fillna(0)
    df['lag_3']       = grp.shift(3).fillna(0)
    df['roll_mean_3'] = grp.transform(lambda x: x.shift(1).rolling(3,min_periods=1).mean()).fillna(0)
    df['roll_std_3']  = grp.transform(lambda x: x.shift(1).rolling(3,min_periods=1).std()).fillna(0)
    stats = grp.agg(conso_moy_client='mean',conso_std_client='std',conso_max_client='max').fillna(0)
    df = df.merge(stats, on='N° Client', how='left')
    df['trimestre'] = ((df['Mois']-1)//3+1)
    df['is_summer'] = df['Mois'].isin([7,8,9]).astype(int)
    df['is_winter'] = df['Mois'].isin([12,1,2]).astype(int)
    df['y'] = grp.shift(-1)
    return df.dropna(subset=['y'])

def compute_metrics(y_true, y_pred):
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    mae  = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2   = r2_score(y_true, y_pred)
    mask = y_true != 0
    mape = np.mean(np.abs((y_true[mask]-y_pred[mask])/y_true[mask]))*100 if mask.any() else 0
    return dict(MAE=mae, RMSE=rmse, R2=r2, MAPE=mape)

# ══════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="sb-logo">
        <div class="sb-logo-badge">
            <span class="sb-logo-icon">⚡</span>
            <div class="sb-logo-text">
                <h3>Amendis ML</h3>
                <p>TÉTOUAN · 2025</p>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    page = st.radio("nav", [
        "Données & EDA",
        "Segmentation Clients",
        "Modélisation",
        "Tableau de Bord",
    ], label_visibility="collapsed")

    st.markdown('<div class="sb-sep"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-section-label">Paramètres Modèles</div>', unsafe_allow_html=True)

    with st.expander("Random Forest"):
        rf_n_est    = st.slider("n_estimators",    50,500,200,50, key='rf_n')
        rf_depth    = st.slider("max_depth",         3, 20, 10, 1, key='rf_d')
        rf_mss      = st.slider("min_samples_split", 2, 20,  5, 1, key='rf_m')
        rf_features = st.selectbox("max_features", ['sqrt','log2','auto'], key='rf_f')

    with st.expander("XGBoost"):
        xgb_n_est = st.slider("n_estimators",    50,500,200,50,   key='xgb_n')
        xgb_lr    = st.slider("learning_rate", 0.01,0.3,0.1,0.01, key='xgb_l', format="%.2f")
        xgb_depth = st.slider("max_depth",         3, 15,  6, 1,  key='xgb_d')
        xgb_sub   = st.slider("subsample",       0.5,1.0,0.8,0.1, key='xgb_s', format="%.1f")
        xgb_col   = st.slider("colsample_bytree",0.5,1.0,0.8,0.1, key='xgb_c', format="%.1f")

    with st.expander("Régression Linéaire"):
        lr_type      = st.selectbox("Type", ['LinearRegression','Ridge','Lasso'], key='lr_t')
        lr_alpha     = st.slider("Alpha", 0.01, 100.0, 1.0, key='lr_a')
        lr_intercept = st.checkbox("fit_intercept", True, key='lr_i')

    with st.expander("Gradient Boosting"):
        gbm_n_est = st.slider("n_estimators",    50,500,200,50,   key='gbm_n')
        gbm_lr    = st.slider("learning_rate", 0.01,0.3,0.1,0.01, key='gbm_l', format="%.2f")
        gbm_depth = st.slider("max_depth",         3, 10,  4, 1,  key='gbm_d')
        gbm_sub   = st.slider("subsample",       0.5,1.0,0.8,0.1, key='gbm_s', format="%.1f")

    st.markdown('<div class="sb-sep"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-section-label">Configuration</div>', unsafe_allow_html=True)
    train_size = st.slider("Train / Test split (%)", 60, 90, 80, 5)
    cv_folds   = st.selectbox("Cross-Validation folds", [3, 5, 10], index=1)

# ══════════════════════════════════════════════════════════════
#  PAGE 1 · DONNÉES & EDA
# ══════════════════════════════════════════════════════════════
if page == "Données & EDA":
    st.markdown('<div class="page-title">Données & Analyse Exploratoire</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Chargez votre fichier Excel Amendis pour démarrer l\'analyse.</div>', unsafe_allow_html=True)

    uploaded = st.file_uploader("Fichier Excel (.xlsx / .xls)", type=['xlsx','xls'])
    if uploaded:
        df = load_data(uploaded)
        st.session_state['df'] = df
    elif st.session_state['df'] is None:
        st.info("Chargez votre fichier Excel pour commencer.")
        st.stop()

    df = st.session_state['df']

    # ── Métriques rapides ──────────────────────────────────────
    sh("Vue d'ensemble", badge=f"{df.shape[0]:,} lignes")
    c1,c2,c3,c4,c5 = st.columns(5)
    with c1: kpi(f"{df.shape[0]:,}", "Enregistrements", accent=COLOR_MAIN)
    with c2: kpi(f"{df.shape[1]}", "Variables", accent=COLOR_WARN)
    with c3: kpi(f"{df['N° Client'].nunique():,}", "Clients uniques", accent=COLOR_SUCCESS)
    with c4: kpi(f"{df['Mois'].nunique()}", "Mois couverts", accent=COLOR_PURPLE)
    with c5: kpi(f"{df.isnull().sum().sum():,}", "Valeurs manquantes", accent=COLOR_DANGER)

    tab1,tab2,tab3,tab4,tab5,tab6 = st.tabs([
        "Données brutes", "Statistiques", "Distributions",
        "Corrélations", "Séries temporelles", "Outliers"
    ])

    with tab1:
        sh("Aperçu des données")
        st.dataframe(df.head(200), use_container_width=True, height=380)
        col1, col2 = st.columns(2)
        with col1:
            sh("Types de colonnes")
            st.dataframe(df.dtypes.reset_index().rename(
                columns={'index':'Colonne',0:'Type'}), height=260)
        with col2:
            sh("Valeurs manquantes")
            nan_df = df.isnull().sum().reset_index()
            nan_df.columns = ['Colonne','NaN']
            nan_df['Taux (%)'] = (nan_df['NaN']/len(df)*100).round(2)
            st.dataframe(nan_df.sort_values('NaN', ascending=False), height=260)

    with tab2:
        sh("Statistiques descriptives")
        stats = df.describe().T.round(3)
        st.dataframe(stats, use_container_width=True)

        sh("Répartition par Tranche tarifaire")
        tc = df['Tranche'].value_counts().reset_index()
        tc.columns = ['Tranche','Count']
        tc['%'] = (tc['Count']/tc['Count'].sum()*100).round(1)
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=tc['Tranche'], y=tc['Count'],
            marker=dict(
                color=tc['Count'],
                colorscale=[[0,'#0d1117'],[0.5,'#00448a'],[1,'#00d4ff']],
                line=dict(color='rgba(0,212,255,0.3)', width=1)
            ),
            text=[f"{p}%" for p in tc['%']], textposition='outside',
            textfont=dict(color='#8892b0', size=11)
        ))
        fig.update_layout(**THEME, height=300, title="Répartition par Tranche",
                          xaxis_tickangle=-20)
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        num_cols = df.select_dtypes(include=np.number).columns.tolist()
        sh("Distributions des variables")
        sel_col = st.selectbox("Variable à analyser", num_cols)
        c1, c2, c3 = st.columns(3)
        with c1:
            fig = px.histogram(df, x=sel_col, nbins=60,
                               color_discrete_sequence=[COLOR_MAIN], **THEME)
            fig.update_layout(title=f"Histogramme — {sel_col}", bargap=0.05,
                              height=280)
            fig.update_traces(marker_line_color='rgba(0,212,255,0.2)', marker_line_width=0.5)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            fig = px.box(df, y=sel_col, color_discrete_sequence=[COLOR_WARN], **THEME)
            fig.update_layout(title=f"Boxplot — {sel_col}", height=280)
            st.plotly_chart(fig, use_container_width=True)
        with c3:
            from scipy import stats as sp_stats
            vals = df[sel_col].dropna()
            qqx  = np.sort(vals)
            n    = len(qqx)
            p    = (np.arange(1, n+1) - 0.5) / n
            qqy  = sp_stats.norm.ppf(p, loc=vals.mean(), scale=vals.std())
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=qqy, y=qqx, mode='markers',
                marker=dict(color=COLOR_MAIN, size=3, opacity=0.5), name='Q-Q'))
            mn = min(qqx.min(), qqy.min()); mx = max(qqx.max(), qqy.max())
            fig.add_trace(go.Scatter(x=[mn,mx], y=[mn,mx], mode='lines',
                line=dict(color=COLOR_DANGER, dash='dash', width=1.5), name='Normal'))
            fig.update_layout(**THEME, title="Q-Q Plot", height=280, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        sh("Distributions multiples")
        fig = make_subplots(rows=2, cols=3,
            subplot_titles=[c for c in num_cols[:6]],
            vertical_spacing=0.12, horizontal_spacing=0.06)
        colors_cycle = [COLOR_MAIN, COLOR_WARN, COLOR_SUCCESS,
                        COLOR_PURPLE, COLOR_DANGER, '#ff6b81']
        for i, col in enumerate(num_cols[:6]):
            r, c_idx = divmod(i, 3)
            vals = df[col].dropna()
            fig.add_trace(go.Histogram(x=vals, nbinsx=40,
                marker_color=colors_cycle[i], opacity=0.75,
                marker_line_color='rgba(255,255,255,0.1)',
                marker_line_width=0.5, showlegend=False),
                row=r+1, col=c_idx+1)
        fig.update_layout(**THEME, height=420)
        st.plotly_chart(fig, use_container_width=True)

    with tab4:
        sh("Heatmap de corrélation")
        num_df = df[num_cols].corr().round(2)
        fig = px.imshow(num_df, text_auto=True, aspect='auto',
                        color_continuous_scale=['#ff4757','#1e2130','#00d4ff'],
                        **THEME)
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

        sh("Analyse bivariée")
        col1, col2 = st.columns(2)
        x_col = col1.selectbox("Axe X", num_cols, index=0, key='sc_x')
        y_col = col2.selectbox("Axe Y", num_cols, index=1, key='sc_y')
        sample = df.sample(min(3000, len(df)))
        color_col = 'Tranche' if 'Tranche' in df.columns else None
        fig = px.scatter(sample, x=x_col, y=y_col,
                         color=color_col,
                         marginal_x='histogram', marginal_y='histogram',
                         opacity=0.5,
                         color_discrete_sequence=PALETTE, **THEME)
        fig.update_layout(height=460)
        st.plotly_chart(fig, use_container_width=True)

    with tab5:
        sh("Évolution mensuelle de la consommation")
        ts = df.groupby('Mois')['Consommation (kWh)'].agg(
            Total='sum', Moyenne='mean', Ecart='std').reset_index().fillna(0)
        MOIS = {1:'Jan',2:'Fév',3:'Mar',4:'Avr',5:'Mai',6:'Jun',
                7:'Jul',8:'Aoû',9:'Sep',10:'Oct',11:'Nov',12:'Déc'}
        ts['M'] = ts['Mois'].map(MOIS)

        fig = make_subplots(rows=2, cols=1,
            subplot_titles=["Consommation Totale (kWh)","Consommation Moyenne ± Écart-type"],
            vertical_spacing=0.12, row_heights=[0.55, 0.45])

        # Bar + area
        fig.add_trace(go.Bar(x=ts['M'], y=ts['Total'],
            marker=dict(color=ts['Total'],
                colorscale=[[0,'#0d2233'],[0.5,'#006699'],[1,'#00d4ff']],
                line=dict(color='rgba(0,212,255,0.3)', width=0.5)),
            text=(ts['Total']/1000).round(1).astype(str)+'k',
            textposition='outside', textfont=dict(size=10, color='#636e8a'),
            showlegend=False, name='Total'), row=1, col=1)

        fig.add_trace(go.Scatter(x=ts['M'], y=ts['Moyenne']+ts['Ecart'],
            mode='lines', line=dict(width=0), showlegend=False, name='+σ'), row=2, col=1)
        fig.add_trace(go.Scatter(x=ts['M'], y=ts['Moyenne']-ts['Ecart'],
            mode='lines', line=dict(width=0), fill='tonexty',
            fillcolor='rgba(0,212,255,0.08)', showlegend=False, name='-σ'), row=2, col=1)
        fig.add_trace(go.Scatter(x=ts['M'], y=ts['Moyenne'],
            mode='lines+markers', line=dict(color=COLOR_MAIN, width=2),
            marker=dict(size=7, color=COLOR_MAIN, line=dict(color='#0d1117',width=2)),
            name='Moyenne', showlegend=False), row=2, col=1)

        fig.update_layout(**THEME, height=520)
        st.plotly_chart(fig, use_container_width=True)

        sh("Top 20 clients consommateurs")
        top20 = df.groupby('N° Client')['Consommation (kWh)'].sum().nlargest(20).reset_index()
        fig = go.Figure(go.Bar(
            x=top20['Consommation (kWh)'], y=top20['N° Client'].astype(str),
            orientation='h',
            marker=dict(
                color=top20['Consommation (kWh)'],
                colorscale=[[0,'#001a26'],[1,'#00d4ff']],
                line=dict(color='rgba(0,212,255,0.2)', width=0.5)
            ),
            text=top20['Consommation (kWh)'].round(0).astype(int).astype(str)+' kWh',
            textposition='outside', textfont=dict(size=10, color='#8892b0')
        ))
        fig.update_layout(**THEME, height=500, yaxis=dict(autorange='reversed'))
        st.plotly_chart(fig, use_container_width=True)

    with tab6:
        sh("Détection des outliers (méthode IQR)")
        q1  = df['Consommation (kWh)'].quantile(0.25)
        q3  = df['Consommation (kWh)'].quantile(0.75)
        iqr = q3 - q1
        borne = q3 + 1.5*iqr
        outliers = df[df['Consommation (kWh)'] > borne]

        c1,c2,c3,c4 = st.columns(4)
        with c1: kpi(f"{len(outliers):,}", "Outliers détectés", accent=COLOR_DANGER)
        with c2: kpi(f"{len(outliers)/len(df)*100:.1f}%", "Part du dataset", accent=COLOR_WARN)
        with c3: kpi(f"{borne:.0f}", "Borne sup. IQR (kWh)", accent=COLOR_MAIN)
        with c4: kpi(f"{df['Consommation (kWh)'].max():.0f}", "Valeur max (kWh)", accent=COLOR_PURPLE)

        st.markdown("")
        fig = go.Figure()
        normal = df[df['Consommation (kWh)'] <= borne]
        fig.add_trace(go.Scatter(x=normal.index, y=normal['Consommation (kWh)'],
            mode='markers', marker=dict(color='rgba(100,110,138,0.3)', size=2),
            name='Normal', showlegend=True))
        fig.add_trace(go.Scatter(x=outliers.index, y=outliers['Consommation (kWh)'],
            mode='markers', marker=dict(color=COLOR_DANGER, size=5, opacity=0.7,
                line=dict(color='rgba(255,71,87,0.3)', width=3)),
            name='Outlier', showlegend=True))
        fig.add_hline(y=borne, line_dash='dash', line_color=COLOR_WARN, line_width=1,
            annotation_text=f"Borne IQR : {borne:.0f} kWh",
            annotation_font_color=COLOR_WARN)
        fig.update_layout(**THEME, height=380, title="Scatter — Outliers Consommation (kWh)",
                          xaxis_title="Index", yaxis_title="Consommation (kWh)")
        st.plotly_chart(fig, use_container_width=True)

        sh("Distribution par Tranche vs Outliers")
        out_tranche = outliers['Tranche'].value_counts().reset_index()
        out_tranche.columns = ['Tranche','Outliers']
        all_tranche = df['Tranche'].value_counts().reset_index()
        all_tranche.columns = ['Tranche','Total']
        merged = all_tranche.merge(out_tranche, on='Tranche', how='left').fillna(0)
        merged['Taux (%)'] = (merged['Outliers']/merged['Total']*100).round(1)
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Total', x=merged['Tranche'], y=merged['Total'],
            marker_color='rgba(0,212,255,0.2)'))
        fig.add_trace(go.Bar(name='Outliers', x=merged['Tranche'], y=merged['Outliers'],
            marker_color=COLOR_DANGER))
        fig.update_layout(**THEME, barmode='overlay', height=320,
                          legend=dict(orientation='h', y=1.1))
        st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════
#  PAGE 2 · SEGMENTATION CLIENTS
# ══════════════════════════════════════════════════════════════
elif page == "Segmentation Clients":
    st.markdown('<div class="page-title">Segmentation Clients</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Clustering K-Means sur les profils de consommation.</div>', unsafe_allow_html=True)

    if st.session_state['df'] is None:
        st.warning("Chargez d'abord les données."); st.stop()

    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
    from sklearn.decomposition import PCA
    from sklearn.metrics import silhouette_score

    df = st.session_state['df']

    pivot    = df.pivot_table(index='N° Client', columns='Mois',
                              values='Consommation (kWh)', aggfunc='sum').fillna(0)
    stats_cl = df.groupby('N° Client')['Consommation (kWh)'].agg(
        Moy='mean', Std='std', Max='max', Min='min', Total='sum').fillna(0)
    stats_cl['CV'] = stats_cl['Std'] / (stats_cl['Moy'] + 1)
    pivot.columns = [f'M{c}' for c in pivot.columns]
    feat_cl  = pd.concat([stats_cl, pivot], axis=1).fillna(0)

    scaler_cl = StandardScaler()
    X_cl      = scaler_cl.fit_transform(feat_cl)

    n_clusters = st.slider("Nombre de clusters K", 2, 10, 4)

    sh("Méthode du coude & Score Silhouette")
    with st.spinner("Calcul en cours…"):
        inertias, sil_scores = [], []
        K_range = range(2, 11)
        for k in K_range:
            km = KMeans(n_clusters=k, random_state=42, n_init=10)
            km.fit(X_cl)
            inertias.append(km.inertia_)
            sil_scores.append(silhouette_score(X_cl, km.labels_))

    fig = make_subplots(rows=1, cols=2,
                        subplot_titles=["Inertie (Elbow)", "Score Silhouette"])

    fig.add_trace(go.Scatter(x=list(K_range), y=inertias,
        mode='lines+markers',
        line=dict(color=COLOR_MAIN, width=2),
        marker=dict(size=8, color=COLOR_MAIN,
                    line=dict(color='#0d1117', width=2)),
        fill='tozeroy', fillcolor='rgba(0,212,255,0.05)',
        showlegend=False), row=1, col=1)

    fig.add_trace(go.Scatter(x=list(K_range), y=sil_scores,
        mode='lines+markers',
        line=dict(color=COLOR_SUCCESS, width=2),
        marker=dict(size=8, color=COLOR_SUCCESS,
                    line=dict(color='#0d1117', width=2)),
        fill='tozeroy', fillcolor='rgba(0,255,136,0.05)',
        showlegend=False), row=1, col=2)

    for fig_obj in [fig]:
        fig_obj.add_vline(x=n_clusters, line_dash='dot', line_color=COLOR_WARN, line_width=1.5)

    fig.update_layout(**THEME, height=320)
    st.plotly_chart(fig, use_container_width=True)

    # KMeans final
    km_final = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels   = km_final.fit_predict(X_cl)
    sil_final= silhouette_score(X_cl, labels)

    c1,c2,c3 = st.columns(3)
    with c1: kpi(f"{n_clusters}", "Clusters", accent=COLOR_MAIN)
    with c2: kpi(f"{sil_final:.4f}", "Score Silhouette", accent=COLOR_SUCCESS)
    with c3: kpi(f"{len(feat_cl):,}", "Clients segmentés", accent=COLOR_WARN)

    # PCA 2D
    pca    = PCA(n_components=2)
    pca2   = pca.fit_transform(X_cl)
    pca_df = pd.DataFrame({'PC1':pca2[:,0],'PC2':pca2[:,1],
                           'Cluster':labels.astype(str),
                           'Client':feat_cl.index})

    sh("Visualisation PCA 2D des clusters",
       badge=f"PC1={pca.explained_variance_ratio_[0]:.1%} + PC2={pca.explained_variance_ratio_[1]:.1%}")

    fig = px.scatter(pca_df, x='PC1', y='PC2', color='Cluster',
                     hover_data=['Client'],
                     color_discrete_sequence=PALETTE,
                     **THEME)
    fig.update_traces(marker=dict(size=5, opacity=0.65,
                                  line=dict(width=0.5, color='rgba(255,255,255,0.1)')))
    fig.update_layout(height=460,
        legend=dict(orientation='h', y=1.05, font=dict(size=11)),
        xaxis=dict(gridcolor='rgba(255,255,255,0.04)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.04)'))
    st.plotly_chart(fig, use_container_width=True)

    # Profils clusters
    sh("Profils des clusters")
    clusters_df  = stats_cl.copy()
    clusters_df['Cluster'] = labels
    profile      = clusters_df.groupby('Cluster').agg(
        Nb_Clients=('Moy','count'), Conso_Moy=('Moy','mean'),
        Conso_Std=('Std','mean'), Conso_Max=('Max','mean'),
        Conso_Total=('Total','sum'), CV_Moy=('CV','mean')
    ).round(2).reset_index()
    CLUSTER_LABELS = {0:'Frugaux',1:'Moyens',2:'Saisonniers',3:'Grands'}
    profile['Profil'] = profile['Cluster'].map(lambda x: CLUSTER_LABELS.get(x, f'C{x}'))

    st.dataframe(profile, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(profile, x='Profil', y='Conso_Moy',
                     color='Conso_Moy', text='Nb_Clients',
                     color_continuous_scale=[[0,'#001a26'],[1,'#00d4ff']],
                     **THEME)
        fig.update_traces(texttemplate='%{text} clients', textposition='outside',
                          textfont=dict(color='#636e8a', size=10))
        fig.update_layout(height=320, title="Consommation Moyenne / Cluster",
                          coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.pie(profile, names='Profil', values='Nb_Clients',
                     color_discrete_sequence=PALETTE, **THEME, hole=0.5)
        fig.update_layout(height=320, title="Répartition des clients",
                          legend=dict(orientation='h', y=-0.1))
        st.plotly_chart(fig, use_container_width=True)

    # Radar chart profils
    sh("Radar — Profils comparatifs")
    cats = ['Conso_Moy','Conso_Std','Conso_Max','CV_Moy']
    profile_norm = profile.copy()
    for c in cats:
        rng = profile_norm[c].max() - profile_norm[c].min()
        if rng > 0:
            profile_norm[c] = (profile_norm[c] - profile_norm[c].min()) / rng

    fig = go.Figure()
    for i, row in profile_norm.iterrows():
        vals = [row[c] for c in cats] + [row[cats[0]]]
        fig.add_trace(go.Scatterpolar(
            r=vals, theta=cats+[cats[0]], name=row['Profil'],
            line=dict(color=PALETTE[i % len(PALETTE)], width=2),
            fill='toself', fillcolor=f'rgba({",".join(str(int(c)) for c in px.colors.hex_to_rgb(PALETTE[i%len(PALETTE)]))},0.08)'
        ))
    fig.update_layout(**THEME, height=380,
        polar=dict(bgcolor='#0d1117',
            radialaxis=dict(gridcolor='rgba(255,255,255,0.06)', tickfont=dict(size=9)),
            angularaxis=dict(gridcolor='rgba(255,255,255,0.06)')),
        legend=dict(orientation='h', y=-0.12))
    st.plotly_chart(fig, use_container_width=True)

    client_clusters = pd.Series(labels, index=feat_cl.index, name='Cluster')
    st.session_state['clusters_df'] = client_clusters
    st.success(f"Segmentation terminée — {n_clusters} clusters | Silhouette : {sil_final:.4f}")

# ══════════════════════════════════════════════════════════════
#  PAGE 3 · MODÉLISATION
# ══════════════════════════════════════════════════════════════
elif page == "Modélisation":
    st.markdown('<div class="page-title">Modélisation Prédictive</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Entraînement, GridSearch, Cross-Validation et prédictions.</div>', unsafe_allow_html=True)

    if st.session_state['df'] is None:
        st.warning("Chargez d'abord les données."); st.stop()

    from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
    from sklearn.linear_model import LinearRegression, Ridge, Lasso
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline import Pipeline
    from xgboost import XGBRegressor

    df = st.session_state['df']

    with st.spinner("Feature engineering…"):
        df_feat = compute_features(df)
        if st.session_state['clusters_df'] is not None:
            df_feat['cluster'] = df_feat['N° Client'].map(
                st.session_state['clusters_df']).fillna(0).astype(int)
        else:
            df_feat['cluster'] = 0

    features_list = ['lag_1','lag_2','lag_3','roll_mean_3','roll_std_3',
                     'conso_moy_client','conso_std_client','conso_max_client',
                     'Mois','trimestre','is_summer','is_winter','cluster','tranche_enc']

    split_month = int(12 * train_size / 100)
    train_data  = df_feat[df_feat['Mois'] <= split_month]
    test_data   = df_feat[df_feat['Mois'] >  split_month]
    X_train = train_data[features_list].fillna(0)
    y_train = train_data['y'].fillna(0)
    X_test  = test_data[features_list].fillna(0)
    y_test  = test_data['y'].fillna(0)

    st.session_state.update(dict(
        X_train=X_train, X_test=X_test,
        y_train=y_train, y_test=y_test,
        features_list=features_list
    ))

    sh("Données d'entraînement", badge=f"Split mois 1→{split_month} / {split_month+1}→12")
    c1,c2,c3,c4 = st.columns(4)
    with c1: kpi(f"{len(X_train):,}", "Train samples", accent=COLOR_MAIN)
    with c2: kpi(f"{len(X_test):,}", "Test samples",  accent=COLOR_WARN)
    with c3: kpi(f"{len(features_list)}", "Features",  accent=COLOR_SUCCESS)
    with c4: kpi(f"{cv_folds}", "CV Folds",           accent=COLOR_PURPLE)

    if st.session_state['models_results'] is None:
        st.session_state['models_results'] = {}

    # ── Feature importance baseline ────────────────────────────
    sh("Visualisation des Features")
    feat_corr = pd.Series({f: abs(np.corrcoef(X_train[f], y_train)[0,1])
                           for f in features_list}).sort_values(ascending=True)
    fig = go.Figure(go.Bar(
        x=feat_corr.values, y=feat_corr.index, orientation='h',
        marker=dict(color=feat_corr.values,
                    colorscale=[[0,'#001a26'],[0.5,'#006699'],[1,'#00d4ff']],
                    line=dict(color='rgba(0,212,255,0.15)', width=0.5)),
        text=feat_corr.round(3), textposition='outside',
        textfont=dict(size=10, color='#636e8a')
    ))
    fig.update_layout(**THEME, height=380,
                      title="Corrélation |r| avec la cible (mois suivant)",
                      xaxis_title="Corrélation absolue")
    st.plotly_chart(fig, use_container_width=True)

    # ── Onglets modèles ────────────────────────────────────────
    tab1,tab2,tab3,tab4 = st.tabs([
        "Random Forest", "XGBoost", "Régression Linéaire", "Gradient Boosting"
    ])

    def plot_model_results(y_test_vals, y_pred_vals, feat_imp, feat_names, color, model_name):
        fig = make_subplots(rows=1, cols=3,
            subplot_titles=["Réel vs Prédit", "Feature Importance Top 10", "Distribution des Résidus"],
            horizontal_spacing=0.07)

        # Réel vs Prédit
        fig.add_trace(go.Scatter(x=y_test_vals, y=y_pred_vals,
            mode='markers', marker=dict(color=color, size=3, opacity=0.4,
                line=dict(color='rgba(255,255,255,0.05)', width=0.5)),
            showlegend=False), row=1, col=1)
        lim = [min(y_test_vals.min(), y_pred_vals.min()),
               max(y_test_vals.max(), y_pred_vals.max())]
        fig.add_trace(go.Scatter(x=lim, y=lim, mode='lines',
            line=dict(color=COLOR_DANGER, dash='dash', width=1.5),
            showlegend=False), row=1, col=1)

        # Feature importance
        if feat_imp is not None:
            imp = pd.Series(feat_imp, index=feat_names).nlargest(10)
            fig.add_trace(go.Bar(x=imp.values, y=imp.index, orientation='h',
                marker=dict(color=imp.values,
                    colorscale=[[0,'#001a26'],[1,color]],
                    line=dict(color='rgba(255,255,255,0.05)', width=0.5)),
                showlegend=False), row=1, col=2)

        # Résidus
        residuals = y_test_vals - y_pred_vals
        fig.add_trace(go.Histogram(x=residuals, nbinsx=50,
            marker_color=color, opacity=0.7,
            marker_line_color='rgba(255,255,255,0.1)',
            showlegend=False), row=1, col=3)
        fig.add_vline(x=0, line_dash='dash', line_color=COLOR_DANGER,
                      line_width=1.5, row=1, col=3)

        fig.update_layout(**THEME, height=380, showlegend=False)
        return fig

    # ── Random Forest ──────────────────────────────────────────
    with tab1:
        sh("Random Forest Regressor")
        c1, c2 = st.columns([3,1])
        with c2:
            use_grid = st.checkbox("GridSearchCV", key='gs_rf')
            train_btn = st.button("Entraîner RF", key='train_rf')
        if train_btn:
            with st.spinner("Entraînement Random Forest…"):
                if use_grid:
                    prog = st.progress(0, "Grid Search…")
                    model = GridSearchCV(
                        RandomForestRegressor(random_state=42),
                        {'n_estimators':[100,rf_n_est],'max_depth':[rf_depth,None],
                         'min_samples_split':[2,rf_mss]},
                        cv=cv_folds, scoring='neg_mean_absolute_error', n_jobs=-1)
                    model.fit(X_train, y_train); prog.progress(100)
                    st.success(f"Meilleurs params : {model.best_params_}")
                else:
                    model = RandomForestRegressor(
                        n_estimators=rf_n_est, max_depth=rf_depth,
                        min_samples_split=rf_mss, random_state=42, n_jobs=-1)
                    model.fit(X_train, y_train)
                y_pred   = model.predict(X_test)
                metrics  = compute_metrics(y_test, y_pred)
                est      = model.best_estimator_ if hasattr(model,'best_estimator_') else model
                cv_sc    = cross_val_score(est, X_train, y_train, cv=cv_folds,
                                           scoring='neg_mean_absolute_error', n_jobs=-1)
                metrics['CV_MAE'] = -cv_sc.mean(); metrics['CV_std'] = cv_sc.std()
                st.session_state['models_results']['Random Forest'] = dict(
                    metrics=metrics, model=model, y_pred=y_pred, cv=cv_sc)
                st.success("Random Forest entraîné")

        res = st.session_state['models_results'].get('Random Forest')
        if res:
            m = res['metrics']
            c1,c2,c3,c4,c5 = st.columns(5)
            c1.metric("MAE",    f"{m['MAE']:.2f} kWh")
            c2.metric("RMSE",   f"{m['RMSE']:.2f} kWh")
            c3.metric("R²",     f"{m['R2']:.4f}")
            c4.metric("MAPE",   f"{m['MAPE']:.2f}%")
            c5.metric("CV MAE", f"{m['CV_MAE']:.2f} ±{m['CV_std']:.2f}")
            est = res['model'].best_estimator_ if hasattr(res['model'],'best_estimator_') else res['model']
            fig = plot_model_results(y_test.values, res['y_pred'],
                                     est.feature_importances_, features_list, COLOR_MAIN, 'RF')
            st.plotly_chart(fig, use_container_width=True)

    # ── XGBoost ────────────────────────────────────────────────
    with tab2:
        sh("XGBoost Regressor")
        c1, c2 = st.columns([3,1])
        with c2:
            use_grid = st.checkbox("GridSearchCV", key='gs_xgb')
            train_btn = st.button("Entraîner XGBoost", key='train_xgb')
        if train_btn:
            with st.spinner("Entraînement XGBoost…"):
                if use_grid:
                    prog = st.progress(0, "Grid Search…")
                    model = GridSearchCV(
                        XGBRegressor(random_state=42, verbosity=0),
                        {'n_estimators':[100,xgb_n_est],'max_depth':[4,xgb_depth],
                         'learning_rate':[0.05,xgb_lr],'subsample':[0.8,xgb_sub]},
                        cv=cv_folds, scoring='neg_mean_absolute_error', n_jobs=-1)
                    model.fit(X_train, y_train); prog.progress(100)
                    st.success(f"Meilleurs params : {model.best_params_}")
                else:
                    model = XGBRegressor(n_estimators=xgb_n_est, max_depth=xgb_depth,
                        learning_rate=xgb_lr, subsample=xgb_sub,
                        colsample_bytree=xgb_col, random_state=42, verbosity=0)
                    model.fit(X_train, y_train)
                y_pred  = model.predict(X_test)
                metrics = compute_metrics(y_test, y_pred)
                est     = model.best_estimator_ if hasattr(model,'best_estimator_') else model
                cv_sc   = cross_val_score(est, X_train, y_train, cv=cv_folds,
                                          scoring='neg_mean_absolute_error', n_jobs=-1)
                metrics['CV_MAE'] = -cv_sc.mean(); metrics['CV_std'] = cv_sc.std()
                st.session_state['models_results']['XGBoost'] = dict(
                    metrics=metrics, model=model, y_pred=y_pred, cv=cv_sc)
                st.success("XGBoost entraîné")

        res = st.session_state['models_results'].get('XGBoost')
        if res:
            m = res['metrics']
            c1,c2,c3,c4,c5 = st.columns(5)
            c1.metric("MAE",  f"{m['MAE']:.2f} kWh")
            c2.metric("RMSE", f"{m['RMSE']:.2f} kWh")
            c3.metric("R²",   f"{m['R2']:.4f}")
            c4.metric("MAPE", f"{m['MAPE']:.2f}%")
            c5.metric("CV MAE",f"{m['CV_MAE']:.2f} ±{m['CV_std']:.2f}")
            est = res['model'].best_estimator_ if hasattr(res['model'],'best_estimator_') else res['model']
            fig = plot_model_results(y_test.values, res['y_pred'],
                                     est.feature_importances_, features_list, COLOR_WARN, 'XGB')
            st.plotly_chart(fig, use_container_width=True)

    # ── Régression Linéaire ────────────────────────────────────
    with tab3:
        sh("Régression Linéaire")
        c1, c2 = st.columns([3,1])
        with c2:
            train_btn = st.button("Entraîner Régression", key='train_lr')
        if train_btn:
            with st.spinner("Entraînement Régression…"):
                reg = (Ridge(alpha=lr_alpha, fit_intercept=lr_intercept) if lr_type=='Ridge'
                       else Lasso(alpha=lr_alpha, fit_intercept=lr_intercept) if lr_type=='Lasso'
                       else LinearRegression(fit_intercept=lr_intercept))
                model   = Pipeline([('scaler', StandardScaler()), ('model', reg)])
                model.fit(X_train, y_train)
                y_pred  = model.predict(X_test)
                metrics = compute_metrics(y_test, y_pred)
                cv_sc   = cross_val_score(model, X_train, y_train, cv=cv_folds,
                                          scoring='neg_mean_absolute_error', n_jobs=-1)
                metrics['CV_MAE'] = -cv_sc.mean(); metrics['CV_std'] = cv_sc.std()
                st.session_state['models_results']['Régression Linéaire'] = dict(
                    metrics=metrics, model=model, y_pred=y_pred, cv=cv_sc)
                st.success(f"{lr_type} entraîné")

        res = st.session_state['models_results'].get('Régression Linéaire')
        if res:
            m = res['metrics']
            c1,c2,c3,c4,c5 = st.columns(5)
            c1.metric("MAE",  f"{m['MAE']:.2f} kWh")
            c2.metric("RMSE", f"{m['RMSE']:.2f} kWh")
            c3.metric("R²",   f"{m['R2']:.4f}")
            c4.metric("MAPE", f"{m['MAPE']:.2f}%")
            c5.metric("CV MAE",f"{m['CV_MAE']:.2f} ±{m['CV_std']:.2f}")
            coefs = np.abs(res['model'].named_steps['model'].coef_)
            fig   = plot_model_results(y_test.values, res['y_pred'],
                                       coefs, features_list, COLOR_SUCCESS, 'LR')
            st.plotly_chart(fig, use_container_width=True)

    # ── GBM ───────────────────────────────────────────────────
    with tab4:
        sh("Gradient Boosting Regressor")
        c1, c2 = st.columns([3,1])
        with c2:
            use_grid = st.checkbox("GridSearchCV", key='gs_gbm')
            train_btn = st.button("Entraîner GBM", key='train_gbm')
        if train_btn:
            with st.spinner("Entraînement GBM… (peut prendre quelques minutes)"):
                if use_grid:
                    prog = st.progress(0, "Grid Search…")
                    model = GridSearchCV(
                        GradientBoostingRegressor(random_state=42),
                        {'n_estimators':[100,gbm_n_est],'max_depth':[3,gbm_depth],
                         'learning_rate':[0.05,gbm_lr],'subsample':[0.8,gbm_sub]},
                        cv=cv_folds, scoring='neg_mean_absolute_error', n_jobs=-1)
                    model.fit(X_train, y_train); prog.progress(100)
                    st.success(f"Meilleurs params : {model.best_params_}")
                else:
                    model = GradientBoostingRegressor(
                        n_estimators=gbm_n_est, max_depth=gbm_depth,
                        learning_rate=gbm_lr, subsample=gbm_sub, random_state=42)
                    model.fit(X_train, y_train)
                y_pred  = model.predict(X_test)
                metrics = compute_metrics(y_test, y_pred)
                est     = model.best_estimator_ if hasattr(model,'best_estimator_') else model
                cv_sc   = cross_val_score(est, X_train, y_train, cv=cv_folds,
                                          scoring='neg_mean_absolute_error', n_jobs=-1)
                metrics['CV_MAE'] = -cv_sc.mean(); metrics['CV_std'] = cv_sc.std()
                st.session_state['models_results']['GBM'] = dict(
                    metrics=metrics, model=model, y_pred=y_pred, cv=cv_sc)
                st.success("GBM entraîné")

        res = st.session_state['models_results'].get('GBM')
        if res:
            m = res['metrics']
            c1,c2,c3,c4,c5 = st.columns(5)
            c1.metric("MAE",  f"{m['MAE']:.2f} kWh")
            c2.metric("RMSE", f"{m['RMSE']:.2f} kWh")
            c3.metric("R²",   f"{m['R2']:.4f}")
            c4.metric("MAPE", f"{m['MAPE']:.2f}%")
            c5.metric("CV MAE",f"{m['CV_MAE']:.2f} ±{m['CV_std']:.2f}")
            est = res['model'].best_estimator_ if hasattr(res['model'],'best_estimator_') else res['model']
            fig = plot_model_results(y_test.values, res['y_pred'],
                                     est.feature_importances_, features_list, COLOR_PURPLE, 'GBM')
            st.plotly_chart(fig, use_container_width=True)

    # ── Tableau de prédictions complet ────────────────────────
    if st.session_state['models_results']:
        sh("Tableau de Prédictions Complet")

        best_name = max(st.session_state['models_results'],
                        key=lambda k: st.session_state['models_results'][k]['metrics']['R2'])
        best_res  = st.session_state['models_results'][best_name]
        st.markdown(f'<span class="badge-blue">Meilleur modèle : {best_name}</span>',
                    unsafe_allow_html=True)
        st.markdown("")

        preds_df = test_data[['N° Client','Mois','Consommation (kWh)']].copy()
        preds_df = preds_df.iloc[:len(best_res['y_pred'])].copy()
        preds_df['Valeur_Réelle'] = y_test.values[:len(best_res['y_pred'])]
        preds_df['Prédiction']    = best_res['y_pred']
        preds_df['Erreur']        = preds_df['Valeur_Réelle'] - preds_df['Prédiction']
        preds_df['Erreur%']       = (preds_df['Erreur'].abs() /
                                     (preds_df['Valeur_Réelle'].abs()+1)*100).round(2)
        margin = preds_df['Erreur'].std() * 1.96
        preds_df['IC_Bas']  = (preds_df['Prédiction'] - margin).round(2)
        preds_df['IC_Haut'] = (preds_df['Prédiction'] + margin).round(2)

        seuil_err = st.slider("Seuil erreur% pour surlignage rouge", 5, 50, 20)

        def highlight_errors(row):
            c = 'background-color:#1a0808;color:#ff6b6b' if row['Erreur%'] > seuil_err else ''
            return [c]*len(row)

        st.dataframe(preds_df.round(2).style.apply(highlight_errors, axis=1),
                     use_container_width=True, height=380)

        # Graphique Réel vs Prédit mensuel
        sh("Réel vs Prédit — Agrégé par mois")
        agg = preds_df.groupby('Mois').agg(
            Réel=('Valeur_Réelle','sum'),
            Prédit=('Prédiction','sum')).reset_index()
        MOIS = {1:'Jan',2:'Fév',3:'Mar',4:'Avr',5:'Mai',6:'Jun',
                7:'Jul',8:'Aoû',9:'Sep',10:'Oct',11:'Nov',12:'Déc'}
        agg['M'] = agg['Mois'].map(MOIS)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=agg['M'], y=agg['Réel'],
            mode='lines+markers', name='Réel',
            line=dict(color=COLOR_MAIN, width=2.5),
            marker=dict(size=9, color=COLOR_MAIN, line=dict(color='#0d1117',width=2))))
        fig.add_trace(go.Scatter(x=agg['M'], y=agg['Prédit'],
            mode='lines+markers', name=f'Prédit ({best_name})',
            line=dict(color=COLOR_WARN, width=2.5, dash='dot'),
            marker=dict(size=9, symbol='square', color=COLOR_WARN,
                        line=dict(color='#0d1117',width=2))))
        # Zone d'erreur
        fig.add_trace(go.Scatter(
            x=pd.concat([agg['M'], agg['M'][::-1]]),
            y=pd.concat([agg['Prédit']+margin, (agg['Prédit']-margin)[::-1]]),
            fill='toself', fillcolor='rgba(255,165,2,0.06)',
            line=dict(color='rgba(255,165,2,0)', width=0),
            name='IC 95%', showlegend=True))
        fig.update_layout(**THEME, height=380,
                          legend=dict(orientation='h', y=1.05),
                          yaxis=dict(gridcolor='rgba(255,255,255,0.04)'),
                          xaxis=dict(gridcolor='rgba(255,255,255,0.04)'))
        st.plotly_chart(fig, use_container_width=True)

        # Export Excel
        sh("Téléchargements")
        from io import BytesIO
        buf = BytesIO()
        with pd.ExcelWriter(buf, engine='openpyxl') as writer:
            preds_df.round(2).to_excel(writer, sheet_name='Prédictions', index=False)
            agg.to_excel(writer, sheet_name='Agrégé Mensuel', index=False)
        buf.seek(0)
        st.download_button("Télécharger Prédictions Excel",
                            data=buf, file_name='predictions_amendis.xlsx',
                            mime='application/vnd.ms-excel')

        st.session_state['predictions_df'] = preds_df
        st.session_state['best_model']     = best_name

# ══════════════════════════════════════════════════════════════
#  PAGE 4 · TABLEAU DE BORD
# ══════════════════════════════════════════════════════════════
elif page == "Tableau de Bord":
    st.markdown('<div class="page-title">Tableau de Bord KPI</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Vue synthétique des indicateurs de performance et comparaison des modèles.</div>', unsafe_allow_html=True)

    if st.session_state['df'] is None:
        st.warning("Chargez d'abord les données."); st.stop()

    df = st.session_state['df']

    # ── KPIs principaux ─────────────────────────────────────────
    total = df['Consommation (kWh)'].sum()
    moy   = df['Consommation (kWh)'].mean()
    pic   = df['Consommation (kWh)'].max()
    nb_cl = df['N° Client'].nunique()
    bm    = st.session_state.get('best_model') or '—'

    sh("Indicateurs Clés")
    c1,c2,c3,c4,c5 = st.columns(5)
    with c1: kpi(f"{total/1e6:.2f} GWh", "Conso. Totale 2025", accent=COLOR_MAIN)
    with c2: kpi(f"{moy:.0f} kWh",       "Consommation Moyenne", accent=COLOR_WARN)
    with c3: kpi(f"{pic:.0f} kWh",       "Pic de Consommation",  accent=COLOR_DANGER)
    with c4: kpi(f"{nb_cl:,}",           "Clients actifs",       accent=COLOR_SUCCESS)
    with c5: kpi(bm,                     "Meilleur Modèle",      accent=COLOR_PURPLE)

    # ── Évolution mensuelle ─────────────────────────────────────
    sh("Évolution mensuelle 2025")
    MOIS = {1:'Jan',2:'Fév',3:'Mar',4:'Avr',5:'Mai',6:'Jun',
            7:'Jul',8:'Aoû',9:'Sep',10:'Oct',11:'Nov',12:'Déc'}
    ts = df.groupby('Mois')['Consommation (kWh)'].agg(
        Total='sum', Moy='mean', NbFactures='count').reset_index()
    ts['M'] = ts['Mois'].map(MOIS)

    fig = make_subplots(rows=1, cols=2,
        subplot_titles=["Consommation Totale mensuelle", "Nombre de Factures par Mois"])
    fig.add_trace(go.Bar(x=ts['M'], y=ts['Total'],
        marker=dict(color=ts['Total'],
            colorscale=[[0,'#0d1a26'],[0.5,'#005588'],[1,'#00d4ff']],
            line=dict(color='rgba(0,212,255,0.2)',width=0.5)),
        text=(ts['Total']/1000).round(1).astype(str)+' k',
        textposition='outside', textfont=dict(size=9,color='#636e8a'),
        showlegend=False), row=1, col=1)
    fig.add_trace(go.Scatter(x=ts['M'], y=ts['NbFactures'],
        mode='lines+markers', line=dict(color=COLOR_SUCCESS, width=2),
        marker=dict(size=7, color=COLOR_SUCCESS, line=dict(color='#0d1117',width=2)),
        showlegend=False), row=1, col=2)
    fig.update_layout(**THEME, height=340)
    st.plotly_chart(fig, use_container_width=True)

    # ── Répartition par tranche ─────────────────────────────────
    sh("Analyse par Tranche Tarifaire")
    c1, c2 = st.columns(2)
    with c1:
        tc = df['Tranche'].value_counts().reset_index()
        tc.columns = ['Tranche','Count']
        fig = go.Figure(go.Pie(
            labels=tc['Tranche'], values=tc['Count'],
            hole=0.55,
            marker=dict(colors=PALETTE, line=dict(color='#0d1117',width=2)),
            textinfo='label+percent',
            insidetextorientation='radial',
            textfont=dict(size=11)
        ))
        fig.update_layout(**THEME, height=340, title="Clients par Tranche",
                          showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        conso_tr = df.groupby('Tranche')['Consommation (kWh)'].agg(
            Moy='mean', Total='sum', Nb='count').round(1).reset_index()
        fig = px.bar(conso_tr, x='Tranche', y='Moy',
                     color='Moy',
                     color_continuous_scale=[[0,'#001a26'],[1,'#00d4ff']],
                     text='Nb', **THEME)
        fig.update_traces(texttemplate='%{text}', textposition='outside',
                          textfont=dict(size=9, color='#636e8a'))
        fig.update_layout(height=340, title="Conso. Moy. par Tranche",
                          coloraxis_showscale=False, xaxis_tickangle=-20)
        st.plotly_chart(fig, use_container_width=True)

    # ── Comparaison modèles ─────────────────────────────────────
    if st.session_state['models_results']:
        sh("Comparaison des Modèles")
        results = st.session_state['models_results']
        comp_df = pd.DataFrame([
            {'Modèle':k, 'MAE':v['metrics']['MAE'], 'RMSE':v['metrics']['RMSE'],
             'R²':v['metrics']['R2'], 'MAPE%':v['metrics']['MAPE'],
             'CV MAE':v['metrics'].get('CV_MAE',0)}
            for k,v in results.items()
        ]).sort_values('R²', ascending=False).reset_index(drop=True)

        medals = ['1er','2e','3e','4e']
        comp_df.insert(0,'Rang',[medals[i] for i in range(len(comp_df))])
        st.dataframe(comp_df.round(4), use_container_width=True)

        # Bar chart 3 métriques
        fig = make_subplots(rows=1, cols=3,
            subplot_titles=["MAE (min meilleur)", "RMSE (min meilleur)", "R² (max meilleur)"],
            horizontal_spacing=0.08)
        for i, metric in enumerate(['MAE','RMSE','R²']):
            fig.add_trace(go.Bar(
                x=comp_df['Modèle'], y=comp_df[metric],
                marker=dict(color=PALETTE[:len(comp_df)],
                            line=dict(color='rgba(255,255,255,0.05)',width=0.5)),
                text=comp_df[metric].round(3),
                textposition='outside',
                textfont=dict(size=10,color='#636e8a'),
                showlegend=False), row=1, col=i+1)
        fig.update_layout(**THEME, height=360)
        st.plotly_chart(fig, use_container_width=True)

        # Gauges
        sh("Performance du Meilleur Modèle")
        best_r2   = comp_df.iloc[0]['R²']
        best_mape = comp_df.iloc[0]['MAPE%']
        best_nm   = comp_df.iloc[0]['Modèle']

        c1, c2, c3 = st.columns(3)
        with c1:
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=best_r2,
                number=dict(font=dict(color='#e2e8f0', family='Space Mono'), suffix=''),
                title=dict(text=f"R² — {best_nm}", font=dict(color='#8892b0', size=13)),
                delta=dict(reference=0.8, increasing=dict(color=COLOR_SUCCESS),
                           decreasing=dict(color=COLOR_DANGER)),
                gauge=dict(
                    axis=dict(range=[0,1], tickcolor='#3d4460',
                              tickfont=dict(color='#636e8a', size=10)),
                    bar=dict(color=COLOR_MAIN, thickness=0.25),
                    bgcolor='#0d1117',
                    borderwidth=0,
                    steps=[
                        dict(range=[0,0.6],  color='rgba(255,71,87,0.08)'),
                        dict(range=[0.6,0.8],color='rgba(255,165,2,0.08)'),
                        dict(range=[0.8,1.0],color='rgba(0,255,136,0.08)')
                    ],
                    threshold=dict(line=dict(color=COLOR_WARN,width=2),
                                   thickness=0.75, value=0.9)
                )
            ))
            fig.update_layout(**THEME, height=280)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=best_mape,
                number=dict(font=dict(color='#e2e8f0', family='Space Mono'), suffix='%'),
                title=dict(text=f"MAPE — {best_nm}", font=dict(color='#8892b0', size=13)),
                gauge=dict(
                    axis=dict(range=[0,50], tickcolor='#3d4460',
                              tickfont=dict(color='#636e8a', size=10)),
                    bar=dict(color=COLOR_WARN, thickness=0.25),
                    bgcolor='#0d1117', borderwidth=0,
                    steps=[
                        dict(range=[0,10], color='rgba(0,255,136,0.08)'),
                        dict(range=[10,25],color='rgba(255,165,2,0.08)'),
                        dict(range=[25,50],color='rgba(255,71,87,0.08)')
                    ],
                    threshold=dict(line=dict(color=COLOR_DANGER,width=2),
                                   thickness=0.75, value=20)
                )
            ))
            fig.update_layout(**THEME, height=280)
            st.plotly_chart(fig, use_container_width=True)

        with c3:
            best_mae = comp_df.iloc[0]['MAE']
            fig = go.Figure(go.Indicator(
                mode="number+delta",
                value=best_mae,
                number=dict(suffix=' kWh', font=dict(color='#e2e8f0',
                            family='Space Mono', size=32)),
                delta=dict(reference=comp_df['MAE'].mean(),
                           decreasing=dict(color=COLOR_SUCCESS),
                           increasing=dict(color=COLOR_DANGER),
                           suffix=' kWh'),
                title=dict(text=f"MAE — {best_nm}<br><span style='font-size:12px;color:#636e8a'>vs moyenne modèles</span>",
                           font=dict(color='#8892b0', size=13))
            ))
            fig.update_layout(**THEME, height=280)
            st.plotly_chart(fig, use_container_width=True)

        # CV Boxplot
        sh("Distribution Cross-Validation")
        fig = go.Figure()
        for i, (name, res) in enumerate(results.items()):
            fig.add_trace(go.Box(
                y=-res['cv'], name=name,
                boxpoints='all', jitter=0.4, pointpos=-1.8,
                marker=dict(color=PALETTE[i%len(PALETTE)], size=5, opacity=0.7),
                line=dict(color=PALETTE[i%len(PALETTE)], width=1.5),
                fillcolor=f'rgba({",".join(str(int(c)) for c in px.colors.hex_to_rgb(PALETTE[i%len(PALETTE)]))},0.1)'
            ))
        fig.update_layout(**THEME, height=340, title="MAE par Fold (Cross-Validation)",
                          yaxis_title="MAE (kWh)",
                          xaxis=dict(gridcolor='rgba(255,255,255,0.04)'),
                          yaxis=dict(gridcolor='rgba(255,255,255,0.04)'))
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("Entraînez d'abord les modèles dans la page **Modélisation** pour voir le comparatif.")

    # ── Prédictions si disponibles ─────────────────────────────
    if st.session_state['predictions_df'] is not None:
        sh("Analyse des Prédictions")
        preds_df = st.session_state['predictions_df']

        c1, c2 = st.columns(2)
        with c1:
            fig = px.histogram(preds_df, x='Erreur%', nbins=50,
                               color_discrete_sequence=[COLOR_PURPLE], **THEME)
            fig.update_layout(height=300, title="Distribution des Erreurs (%)")
            fig.add_vline(x=0, line_dash='dash', line_color=COLOR_DANGER, line_width=1.5)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            err_by_mois = preds_df.groupby('Mois')['Erreur%'].mean().reset_index()
            err_by_mois['M'] = err_by_mois['Mois'].map(MOIS)
            fig = px.bar(err_by_mois, x='M', y='Erreur%',
                         color='Erreur%',
                         color_continuous_scale=[[0,'#0f2d1a'],[0.5,'#2d2a0f'],[1,'#3d1515']],
                         **THEME)
            fig.update_layout(height=300, title="Erreur Moyenne (%) par Mois",
                              coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)
