import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

from streamlit_option_menu import option_menu


# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------

st.set_page_config(
    page_title="Energy Consumption Analytics",
    layout="wide"
)


# ----------------------------------------------------
# CSS SAAS DESIGN
# ----------------------------------------------------

st.markdown("""
<style>

.stApp{
background:#0f172a;
color:white;
}

[data-testid="stSidebar"]{
background:#020617;
border-right:1px solid #1e293b;
}

.card{
background:#111827;
padding:20px;
border-radius:10px;
border:1px solid #1f2937;
box-shadow:0 10px 30px rgba(0,0,0,0.4);
}

.kpi{
font-size:30px;
font-weight:700;
color:#38bdf8;
}

.kpi-label{
font-size:14px;
color:#94a3b8;
}

.section{
font-size:20px;
font-weight:600;
margin-top:20px;
margin-bottom:10px;
}

</style>
""", unsafe_allow_html=True)


# ----------------------------------------------------
# SIDEBAR
# ----------------------------------------------------

with st.sidebar:

    st.title("Energy Analytics")

    selected = option_menu(
        None,
        ["Data", "Segmentation", "Modeling", "Dashboard"],
        icons=["database","diagram-3","cpu","bar-chart"],
        default_index=0
    )


# ----------------------------------------------------
# SESSION
# ----------------------------------------------------

if "df" not in st.session_state:
    st.session_state.df=None


# ----------------------------------------------------
# DATA PAGE
# ----------------------------------------------------

if selected=="Data":

    st.title("Data Upload & Exploration")

    file=st.file_uploader("Upload Excel File",type=["xlsx"])

    if file:

        df=pd.read_excel(file)

        st.session_state.df=df

    if st.session_state.df is None:
        st.stop()

    df=st.session_state.df


    col1,col2,col3=st.columns(3)

    col1.metric("Rows",len(df))
    col2.metric("Clients",df["N° Client"].nunique())
    col3.metric("Months",df["Mois"].nunique())


    st.subheader("Dataset")

    st.dataframe(df.head(100))


    st.subheader("Consumption Distribution")

    fig=px.histogram(
        df,
        x="Consommation (kWh)",
        template="plotly_dark",
        nbins=50
    )

    st.plotly_chart(fig,use_container_width=True)


    st.subheader("Monthly Consumption")

    ts=df.groupby("Mois")["Consommation (kWh)"].sum().reset_index()

    fig=px.line(
        ts,
        x="Mois",
        y="Consommation (kWh)",
        markers=True,
        template="plotly_dark"
    )

    st.plotly_chart(fig,use_container_width=True)



# ----------------------------------------------------
# SEGMENTATION
# ----------------------------------------------------

elif selected=="Segmentation":

    st.title("Client Segmentation")

    if st.session_state.df is None:
        st.stop()

    df=st.session_state.df

    pivot=df.pivot_table(
        index="N° Client",
        columns="Mois",
        values="Consommation (kWh)",
        aggfunc="sum"
    ).fillna(0)

    scaler=StandardScaler()

    X=scaler.fit_transform(pivot)

    k=st.slider("Clusters",2,10,4)

    model=KMeans(n_clusters=k)

    labels=model.fit_predict(X)

    pivot["cluster"]=labels


    from sklearn.decomposition import PCA

    pca=PCA(n_components=2)

    pca_result=pca.fit_transform(X)

    pca_df=pd.DataFrame()

    pca_df["PC1"]=pca_result[:,0]
    pca_df["PC2"]=pca_result[:,1]
    pca_df["cluster"]=labels.astype(str)


    fig=px.scatter(
        pca_df,
        x="PC1",
        y="PC2",
        color="cluster",
        template="plotly_dark"
    )

    st.plotly_chart(fig,use_container_width=True)


    st.subheader("Cluster Statistics")

    pivot["mean"]=pivot.drop("cluster",axis=1).mean(axis=1)

    stats=pivot.groupby("cluster")["mean"].mean().reset_index()

    st.dataframe(stats)



# ----------------------------------------------------
# MODELING
# ----------------------------------------------------

elif selected=="Modeling":

    st.title("Machine Learning Models")

    if st.session_state.df is None:
        st.stop()

    df=st.session_state.df


    df=df.sort_values(["N° Client","Mois"])

    df["lag1"]=df.groupby("N° Client")["Consommation (kWh)"].shift(1)

    df=df.dropna()

    X=df[["lag1","Mois"]]

    y=df["Consommation (kWh)"]


    X_train,X_test,y_train,y_test=train_test_split(
        X,y,test_size=0.2,random_state=42
    )


    model_name=st.selectbox(
        "Model",
        ["Random Forest","XGBoost"]
    )


    if st.button("Train Model"):

        if model_name=="Random Forest":

            model=RandomForestRegressor()

        else:

            model=XGBRegressor()


        model.fit(X_train,y_train)

        preds=model.predict(X_test)

        mae=mean_absolute_error(y_test,preds)

        r2=r2_score(y_test,preds)

        st.metric("MAE",round(mae,2))

        st.metric("R2",round(r2,3))


        fig=px.scatter(
            x=y_test,
            y=preds,
            template="plotly_dark"
        )

        fig.add_shape(
            type="line",
            x0=y_test.min(),
            y0=y_test.min(),
            x1=y_test.max(),
            y1=y_test.max()
        )

        st.plotly_chart(fig,use_container_width=True)



# ----------------------------------------------------
# DASHBOARD
# ----------------------------------------------------

elif selected=="Dashboard":

    st.title("Energy Dashboard")

    if st.session_state.df is None:
        st.stop()

    df=st.session_state.df


    total=df["Consommation (kWh)"].sum()

    avg=df["Consommation (kWh)"].mean()

    peak=df["Consommation (kWh)"].max()


    col1,col2,col3=st.columns(3)

    with col1:

        st.markdown(f"""
        <div class="card">
        <div class="kpi">{total/1000:.1f} MWh</div>
        <div class="kpi-label">Total Consumption</div>
        </div>
        """,unsafe_allow_html=True)

    with col2:

        st.markdown(f"""
        <div class="card">
        <div class="kpi">{avg:.0f} kWh</div>
        <div class="kpi-label">Average Consumption</div>
        </div>
        """,unsafe_allow_html=True)

    with col3:

        st.markdown(f"""
        <div class="card">
        <div class="kpi">{peak:.0f} kWh</div>
        <div class="kpi-label">Peak Consumption</div>
        </div>
        """,unsafe_allow_html=True)



    st.subheader("Monthly Consumption")

    ts=df.groupby("Mois")["Consommation (kWh)"].sum().reset_index()

    fig=px.bar(
        ts,
        x="Mois",
        y="Consommation (kWh)",
        template="plotly_dark"
    )

    st.plotly_chart(fig,use_container_width=True)



    st.subheader("Consumption by Tariff")

    tar=df.groupby("Tranche")["Consommation (kWh)"].sum().reset_index()

    fig=px.pie(
        tar,
        names="Tranche",
        values="Consommation (kWh)",
        template="plotly_dark"
    )

    st.plotly_chart(fig,use_container_width=True)
