import streamlit as st
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="CineScope – Movie Explorer", layout="wide")

# Apply background color to main area
st.markdown(
    """
    <style>
    .main {
        background-color: #f8f9fa;  /* soft grey */
        padding: 20px;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Load data
df = pd.read_csv("cleaned_movies.csv")
logo = Image.open("favicon.png")

# Title section with logo
col1, col2 = st.columns([1, 8])
with col1:
    st.image(logo, width=80)
with col2:
    st.markdown("<h1 style='color:#FF4B4B;'>CineScope – Movie Explorer</h1>", unsafe_allow_html=True)
    st.caption("Explore movies based on Genre, Year, and Popularity!")

# Sidebar
st.sidebar.markdown("## 🔍 Filter Movies")
selected_genre = st.sidebar.selectbox("🎭 Select Genre", sorted(df['Genre'].dropna().unique()))
selected_year = st.sidebar.selectbox("📅 Select Year", sorted(df['Release_Date'].dropna().unique(), reverse=True))
selected_vote = st.sidebar.selectbox("⭐ Select Vote Category", sorted(df['Vote_Average'].dropna().unique()))

# Filter
filtered_df = df[
    (df['Genre'] == selected_genre) &
    (df['Release_Date'] == selected_year) &
    (df['Vote_Average'] == selected_vote)
]

# Results section
st.markdown("### 🎞️ Filtered Movies")
st.dataframe(filtered_df[['Title', 'Popularity', 'Vote_Count']], use_container_width=True)

# Pie chart section
# Pie chart section
st.markdown("---")
st.markdown("### 🍿 Top 5 Popular Movies (Based on Filter)")

top5 = filtered_df[['Title', 'Popularity']].sort_values(by='Popularity', ascending=False).head(5)

if not top5.empty:
    fig, ax = plt.subplots(figsize=(4, 4))  
    ax.pie(top5['Popularity'], labels=top5['Title'], autopct='%1.1f%%', startangle=140)
    ax.axis('equal')
    st.pyplot(fig)
else:
    st.warning("No data available for the selected filters.")

st.markdown("---")
st.caption("© 2025 CineScope | 👨‍💻 Developed by **Ankit Kumar**")





