import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Video Games Sales Dashboard", page_icon=":video_game:", layout="wide")

# ---- READ EXCEL ----
@st.cache_data
def get_data_from_excel():
    df = pd.read_excel(
        io="Video Games Sales.xlsx",
        engine="openpyxl",
        sheet_name="Video Games Sales",
        skiprows=6,
        usecols="A:L",
        nrows=1914,
    )
    return df

df = get_data_from_excel()

# ---- SIDEBAR ----
st.sidebar.header("Filter Here:")

game = st.sidebar.multiselect(
    "Select Game:",
    options=df["Game_Title"].unique(),
    # default=df["Game_Title"].unique()
)

df_selection = df.query(
    "Game_Title == @game "
)

# ---- MAINPAGE ----
st.title(":video_game: Video Games Sales Dashboard")
st.markdown("##")

# TOP KPI's
total_sales_north_america = int(df_selection["North_America"].sum())
total_sales_europe = int(df_selection["Europe"].sum())
total_sales_japan= int(df_selection["Japan"].sum())
review = int(round(df_selection["Review"].sum()))
column1, column2, column3,column4 = st.columns(4)
with column1:
    st.subheader("Total Sales in North America:")
    st.subheader(f"US $ {total_sales_north_america:,}")
with column2:
    st.subheader("Total Sales in Europe:")
    st.subheader(f"US $ {total_sales_europe:,}")
with column3:
    st.subheader("Total Sales in Japan:")
    st.subheader(f"US $ {total_sales_japan:,}")
with column4:
    st.subheader("Score:")
    st.subheader(f"{review}")      

st.markdown("""---""")

# # SALES BY GAME[BAR CHART]
sales_by_game_north_america = (
    df_selection.groupby(by=["Game_Title"]).sum()[["North_America"]].sort_values(by="North_America")
)
fig_game_sales_north_america = px.bar(
    sales_by_game_north_america,
    x="North_America",
    y=sales_by_game_north_america.index,
    orientation="h",
    title="<b>Sales in North America by Game Title</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_game_north_america),
    template="plotly_white",
)
fig_game_sales_north_america.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

sales_by_game_europe = (
    df_selection.groupby(by=["Game_Title"]).sum()[["Europe"]].sort_values(by="Europe")
)
fig_game_sales_europe = px.bar(
    sales_by_game_europe,
    x="Europe",
    y=sales_by_game_north_america.index,
    orientation="h",
    title="<b>Sales in Europe by Game Title</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_game_europe),
    template="plotly_white",
)
fig_game_sales_europe.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

sales_by_game_japan = (
    df_selection.groupby(by=["Game_Title"]).sum()[["Japan"]].sort_values(by="Japan")
)
fig_game_sales_japan = px.bar(
    sales_by_game_japan,
    x="Japan",
    y=sales_by_game_japan.index,
    orientation="h",
    title="<b>Sales in Japan by Game Title</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_game_japan),
    template="plotly_white",
)
fig_game_sales_japan.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)


column1, column2,column3 = st.columns(3)
column1.plotly_chart(fig_game_sales_north_america, use_container_width=True)
column2.plotly_chart(fig_game_sales_europe, use_container_width=True)
column3.plotly_chart(fig_game_sales_japan, use_container_width=True)


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)