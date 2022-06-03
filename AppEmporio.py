# @Email:  contact@pythonandvba.com
# @Website:  https://pythonandvba.com
# @YouTube:  https://youtube.com/c/CodingIsFun
# @Project:  Sales Dashboard w/ Streamlit



import pandas as pd  # pip install pandas openpyxl
pd.options.display.float_format = '{:,.2f}'.format
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import numpy as np
#import locale
#import calendar
#locale.setlocale(locale.LC_ALL, 'it_IT')


# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Emporio Dashboard", page_icon=":bar_chart:", layout="wide")

# ---- READ EXCEL ----
@st.cache
def get_data_from_excel():
    df = pd.read_excel(
        io="ProdottiUsciti.xlsx",
        engine="openpyxl",
        sheet_name="ProdottiUsciti",
#        skiprows=1,
        usecols="A:K",
        parse_dates=['Data'],
#        nrows=1000,
    )
    # Add columns to dataframe

    df['Anno'] = df['Data'].dt.year
    df['Mese'] = df['Data'].dt.month
    df["Mese"].replace(
        {1: "Gen", 2: "Feb", 3: "Mar", 4: "Apr", 5: "Mag", 6: "Giu", 7: "Lug", 8: "Ago", 9: "Set", 10: "Ott", 11: "Nov",
         12: "Dic"}, inplace=True)
    df["Agea"].replace(
        {'Y': 'Fead', 'N': "Altro"}, inplace=True)

    df['NComp'] = df['NComp'].fillna("0")
    df['NComp'] = df['NComp'].astype('category')
    NCompNew = []

    for row in df['NComp']:
        if int(row) < 3:
            NCompNew.append('Piccolo')
        elif int(row) < 5:
            NCompNew.append('Medio')
        else:
            NCompNew.append('Grande')

    df['NCompNew'] = NCompNew

    return df

df = get_data_from_excel()

# ---- SIDEBAR ----
st.sidebar.header("Selezionare il Filtro")
anno = st.sidebar.multiselect(
    "Seleziona Anno:",
    options=df["Anno"].unique(),
    default=df["Anno"].unique()
)

mese = st.sidebar.multiselect(
    "Seleziona Mese:",
    options=df["Mese"].unique(),
    default=df["Mese"].unique()
)

um = st.sidebar.multiselect(
    "Seleziona Kg/Lt/Pz:",
    options=df["UM"].unique(),
    default=df["UM"].unique()

)



df_selection = df.query(
    "Anno == @anno and Mese == @mese and UM == @um"
)

# ---- MAINPAGE ----
st.title(":bar_chart: Emporio Dashboard")
st.markdown("##")

# TOP KPI's
totale_pezzi = int(df_selection["Pezzi"].sum())
totale_punti = int(df_selection["Punti"].sum())
totale_quantita = int(df_selection["Quantita"].sum())


left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Totale Punti:")
    st.subheader(f"{totale_punti:,}")
with middle_column:
    st.subheader("Totale Pezzi:")
    st.subheader(f"{totale_pezzi:,}")
with right_column:
    st.subheader("Totale Quantita:")
    st.subheader(f"{totale_quantita:,}")

st.markdown("""---""")

# SALES BY PRODUCT LINE [BAR CHART]
Lista_Componenti = (
    df_selection.groupby(by=["NComp"]).sum()[["Punti"]].sort_values(by="Punti")
)

fig_Componenti_punti = px.bar(
    Lista_Componenti,
    x="Punti",
    y=Lista_Componenti.index,
    orientation="h",
    title="<b>Componenti</b>",
    color_discrete_sequence=["#0083B8"] * len(Lista_Componenti),
    template="plotly_white",
    labels={'NComp': 'Numero'}, height=400,
)
fig_Componenti_punti.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

Lista_Agea = (
    df_selection.groupby(by=["Agea"]).sum()[["Punti"]].sort_values(by="Punti")
)

fig_Agea_punti = px.bar(
    Lista_Agea,
    x="Punti",
    y=Lista_Agea.index,
    orientation="h",
    title="<b>Provenienza</b>",
    color_discrete_sequence=["#0083B8"] * len(Lista_Agea),
    template="plotly_white",
)
fig_Agea_punti.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)


left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_Componenti_punti, use_container_width=True)
right_column.plotly_chart(fig_Agea_punti, use_container_width=True)

st.markdown("""---""")

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
