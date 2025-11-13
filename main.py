import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Smart Data Visualizer", page_icon="📊", layout="wide")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
    <style>
    /* Global App Styling */
    .stApp {
        background-color: #FFFFFF;
        font-family: 'Poppins', sans-serif;
        color: #262730;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #F5F5F5;
        border-right: 2px solid #E0E0E0;
    }

    /* Headers */
    h1, h2, h3, h4 {
        color: #FF4B4B;
        font-weight: 600;
    }

    /* Buttons */
    button[data-testid="baseButton-secondary"] {
        background-color: #FF4B4B !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
    }
    button[data-testid="baseButton-secondary"]:hover {
        background-color: #E04343 !important;
    }

    /* Download Button */
    div.stDownloadButton > button {
        background-color: #FF4B4B;
        color: white;
        border-radius: 10px;
        font-weight: 600;
    }
    div.stDownloadButton > button:hover {
        background-color: #E04343;
    }

    /* Dataframes */
    .stDataFrame {
        border-radius: 10px !important;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background-color: #fafafa !important;
        font-weight: 600;
    }

    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #FF4B4B;
        font-weight: 700;
    }

    /* Footer */
    footer {
        visibility: hidden;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚙️ Controls")

uploaded_file = st.sidebar.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx"])

st.title("📊 Smart Data Visualizer")
st.write("Upload your dataset and generate instant insights & visualizations.")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data(uploaded_file):
    if uploaded_file.name.endswith(".csv"):
        return pd.read_csv(uploaded_file)
    else:
        return pd.read_excel(uploaded_file)

if uploaded_file:
    df = load_data(uploaded_file)
    st.success("✅ File uploaded successfully!")

    # Data preview
    st.subheader("📄 Data Preview")
    st.dataframe(df.head())

    # ---------------- DATA SUMMARY ----------------
    st.subheader("🧾 Data Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Missing Values", df.isnull().sum().sum())

    with st.expander("🔍 Data Types & Missing Values"):
        st.write(df.dtypes)
        st.write("Missing Values per Column:")
        st.write(df.isnull().sum())

    with st.expander("📊 Descriptive Statistics"):
        st.write(df.describe())

    # ---------------- VISUALIZATION ----------------
    st.subheader("🎨 Visualization Playground")

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    all_cols = df.columns.tolist()

    chart_type = st.selectbox(
        "Select a chart type",
        ["Scatter Plot", "Line Chart", "Histogram", "Box Plot", "Correlation Heatmap", "Count Plot"]
    )

    fig, ax = plt.subplots(figsize=(8, 5))
    plt.style.use("seaborn-v0_8-darkgrid")

    if chart_type == "Scatter Plot":
        x = st.selectbox("X-axis", numeric_cols)
        y = st.selectbox("Y-axis", numeric_cols)
        sns.scatterplot(data=df, x=x, y=y, ax=ax, color="#FF4B4B")

    elif chart_type == "Line Chart":
        x = st.selectbox("X-axis", all_cols)
        y = st.selectbox("Y-axis", numeric_cols)
        sns.lineplot(data=df, x=x, y=y, ax=ax, color="#FF4B4B")

    elif chart_type == "Histogram":
        column = st.selectbox("Select Column", numeric_cols)
        sns.histplot(df[column], kde=True, ax=ax, color="#FF4B4B")

    elif chart_type == "Box Plot":
        column = st.selectbox("Select Column", numeric_cols)
        sns.boxplot(data=df, y=column, ax=ax, color="#FF4B4B")

    elif chart_type == "Count Plot":
        column = st.selectbox("Select Column", all_cols)
        sns.countplot(data=df, x=column, ax=ax, color="#FF4B4B")
        plt.xticks(rotation=45)

    elif chart_type == "Correlation Heatmap":
        sns.heatmap(df.corr(), annot=True, cmap="coolwarm", ax=ax)

    st.pyplot(fig)

    # ---------------- DOWNLOAD CHART ----------------
    buf = BytesIO()
    fig.savefig(buf, format="png")
    st.download_button(
        label="📥 Download Chart as PNG",
        data=buf.getvalue(),
        file_name="chart.png",
        mime="image/png"
    )

    # ---------------- AUTO INSIGHTS ----------------
    st.subheader("🧠 Quick Insights")
    if len(numeric_cols) >= 2:
        corr_matrix = df[numeric_cols].corr()
        top_corr = (
            corr_matrix.abs().unstack().sort_values(ascending=False)
            .drop_duplicates().head(5)
        )
        st.write("Top Correlated Features:")
        st.write(top_corr)

else:
    st.info("👆 Upload a CSV or Excel file to get started.")

st.markdown("""
---
<p style='text-align:center; color:#FF4B4B; font-weight:600;'>
Made with ❤️ by <b>Manan Chawla</b> <br> Smart Data Visualizer v2.0
</p>
""", unsafe_allow_html=True)
