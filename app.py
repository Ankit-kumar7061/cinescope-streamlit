import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px

# ================= Page Config =================
st.set_page_config(page_title="CineScope – Movie Explorer", layout="wide")

# ================= Load Data =================
df = pd.read_csv("cleaned_movies.csv")
logo = Image.open("favicon.png")

# ================= Custom CSS =================
st.markdown(
    """
    <style>
    /* ---- Animated Neon Gradient Background ---- */
    @keyframes gradientShift {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .stApp {
        background: linear-gradient(120deg, #0f2027, #203a43, #2c5364, #1a2a6c, #b21f1f, #fdbb2d);
        background-size: 400% 400%;
        animation: gradientShift 18s ease infinite;
        color: white;
    }

    /* ---- Cards (Glassmorphism) ---- */
    .glass-card {
        background: rgba(255,255,255,0.08);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 24px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 10px 35px rgba(0,0,0,0.45), inset 0 0 0 1px rgba(255,255,255,0.06);
        color: white;
        transition: transform 0.35s ease, box-shadow 0.35s ease;
    }
    .glass-card:hover {
        transform: translateY(-6px) scale(1.015);
        box-shadow: 0 18px 45px rgba(0,255,255,0.35), inset 0 0 0 1px rgba(255,255,255,0.10);
    }

    /* ---- Headings with subtle neon glow ---- */
    h1,h2,h3 {
        color:#00fff7 !important;
        text-shadow: 0 0 6px rgba(0,255,247,0.75), 0 0 16px rgba(0,255,247,0.35);
        letter-spacing: .3px;
    }

    /* ---- Buttons ---- */
    .stButton>button {
        background: linear-gradient(45deg, #00c6ff, #0072ff);
        border: none;
        color: white;
        border-radius: 14px;
        padding: 0.6rem 1.1rem;
        transition: transform 0.25s ease, box-shadow 0.25s ease;
        box-shadow: 0 0 0 0 rgba(0, 198, 255, 0.0);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 22px rgba(0, 198, 255, 0.45);
    }

    /* ---- Sidebar glass effect ---- */
    [data-testid="stSidebar"] {
        background: rgba(0,0,0,0.35) !important;
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        border-right: 1px solid rgba(255,255,255,0.12);
    }

    /* ---- Dataframe tweaks ---- */
    .stDataFrame {
        border-radius: 14px;
        overflow: hidden;
    }

    /* ---- Subtle fade-in for sections ---- */
    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(8px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .fade {
        animation: fadeUp .5s ease both;
    }

    /* ---- Code block & captions readable ---- */
    .markdown-text-container, .stMarkdown, .stCaption, .stText, .stTitle {
        color: #ffffff;
    }

    /* ---- Scrollbar (WebKit) ---- */
    ::-webkit-scrollbar { width: 10px; height: 10px; }
    ::-webkit-scrollbar-thumb {
        background: rgba(255,255,255,0.25);
        border-radius: 10px;
        border: 2px solid rgba(0,0,0,0);
        background-clip: padding-box;
    }
    ::-webkit-scrollbar-track { background: rgba(255,255,255,0.05); }
    </style>
    """,
    unsafe_allow_html=True
)

# ================= Title =================
col1, col2 = st.columns([1, 8])
with col1:
    st.image(logo, width=80)
with col2:
    st.markdown("<h1 class='fade'>CineScope – Movie Explorer</h1>", unsafe_allow_html=True)
    st.caption("Explore movies based on Genre, Year, and Popularity!")
# ================= Sidebar =================
st.sidebar.markdown("## <span style='color:white;'>🔍 Filter Movies</span>", unsafe_allow_html=True)

st.sidebar.markdown("### <span style='color:white;'>🎭 Select Genre</span>", unsafe_allow_html=True)
selected_genre = st.sidebar.selectbox(
    "", sorted(df['Genre'].dropna().unique())
)

st.sidebar.markdown("### <span style='color:white;'>📅 Select Year</span>", unsafe_allow_html=True)
selected_year = st.sidebar.selectbox(
    "", sorted(df['Release_Date'].dropna().unique(), reverse=True)
)

st.sidebar.markdown("### <span style='color:white;'>⭐ Select Vote Category</span>", unsafe_allow_html=True)
selected_vote = st.sidebar.selectbox(
    "", sorted(df['Vote_Average'].dropna().unique())
)


# ================= Filter Data =================
filtered_df = df[
    (df['Genre'] == selected_genre) &
    (df['Release_Date'] == selected_year) &
    (df['Vote_Average'] == selected_vote)
]

# ================= Top 3 Movies Cards =================
top3 = filtered_df.sort_values(by='Popularity', ascending=False).head(3)
st.markdown("<div class='fade'><h3>🏆 Top 3 Movies</h3></div>", unsafe_allow_html=True)
cols = st.columns(3)
for i, (_, row) in enumerate(top3.iterrows()):
    with cols[i]:
        st.markdown(
            f"""
            <div class='glass-card fade'>
                <h3 style="margin-bottom:6px;">{row['Title']}</h3>
                <p style="margin:.2rem 0;">🔥 Popularity: <b>{row['Popularity']}</b></p>
                <p style="margin:.2rem 0;">🗳️ Votes: <b>{row['Vote_Count']}</b></p>
            </div>
            """,
            unsafe_allow_html=True
        )

# ================= Remaining Movies =================
rest_movies = filtered_df.sort_values(by='Popularity', ascending=False).iloc[3:]
st.markdown("<div class='glass-card fade'>", unsafe_allow_html=True)
st.markdown("### 🎞️ Other Movies")
st.dataframe(rest_movies[['Title','Popularity','Vote_Count']], use_container_width=True, hide_index=True)
st.markdown("</div>", unsafe_allow_html=True)

# ================= Advanced Pie Chart (Modern) =================
st.markdown("<div class='glass-card fade'>", unsafe_allow_html=True)
st.markdown("### 🍿 Top 10 Popular Movies (Modern Pie)")

top10 = filtered_df.sort_values(by='Popularity', ascending=False).head(10)
if not top10.empty:
    fig = px.pie(
        top10,
        names='Title',
        values='Popularity',
        color='Title',
        color_discrete_sequence=px.colors.sequential.Turbo,  # vibrant, modern palette
        hole=0.45
    )
    fig.update_traces(
        textinfo='percent+label',
        hovertemplate="<b>%{label}</b><br>Popularity: %{value}<br>%{percent}",
        pull=[0.06]*len(top10),
        marker=dict(line=dict(color='white', width=2))
    )
    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=True,
        legend=dict(
            font=dict(color='white', size=13),
            bgcolor='rgba(0,0,0,0.35)',
            bordercolor='rgba(255,255,255,0.4)',
            borderwidth=1,
            orientation='v',
            x=1.02, y=0.5
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=14)
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data available for selected filters.")
st.markdown("</div>", unsafe_allow_html=True)

# ================= Footer =================
st.markdown("<div class='glass-card fade'>", unsafe_allow_html=True)
st.caption("© 2025 CineScope | 👨‍💻 Developed by **Ankit Kumar**")
st.markdown("</div>", unsafe_allow_html=True)
