import pandas as pd
pd.options.display.float_format = '{:,.2f}'.format
import plotly.express as px
import streamlit as st
import numpy as np
import locale
import calendar
#locale.setlocale(locale.LC_ALL, 'it_IT')

## ---- READ EXCEL ----
@st.cache
def get_data_from_excel(name):
    df = pd.read_excel(
        io=name,
        engine="openpyxl",
        sheet_name="Sheet1",
        usecols="B:S",
        parse_dates=['Data'],
    )
    return df

df = get_data_from_excel("ProdottiUsciti.xlsx")

# ---- MAINPAGE ----
st.title(":bar_chart: Emporio Dashboard")
st.markdown("##")

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

fornitori = st.sidebar.multiselect(
    "Seleziona Fornitore:",
    options=df["Fornitori"].unique(),
    default=df["Fornitori"].unique()
)

articolo = st.multiselect(
    "Seleziona Articolo:",
    options=df["Articolo"].unique(),
#    default=df["Articolo"].unique()
)

df_selection = df.query(
    "Anno == @anno & Mese == @mese & UM==@um & Articolo==@articolo & Fornitori==@fornitori"
)


#um = st.radio(
#     "Seleziona Unità di misura",
#     ('Kg', 'Lt', 'Pz'))

# TOP KPI's
totale_pezzi = int(df_selection["Pezzi"].sum())
totale_punti = int(df_selection["Punti"].sum())
totale_quantita = int(df_selection["Quantita"].sum())


left_column, left1_column, right_column, right1_column  = st.columns(4)
with left_column:
    st.subheader("Totale Quantità:")
with left1_column:
    st.subheader(f"{totale_quantita:,}")

with right_column:
    st.subheader("Totale Punti:")
with right1_column:
    st.subheader(f"{totale_punti:,}")


# SALES BY PRODUCT LINE [BAR CHART]
Lista_Gruppo1_Punti= (
    df_selection.groupby(by=["Articolo"]).sum()[["Punti"]].sort_values(by="Articolo")
)

Lista_Gruppo1_Qta= (
    df_selection.groupby(by=["Articolo"]).sum()[["Quantita"]].sort_values(by="Articolo")
)

#Lista_Gruppo1_QTa['Quantita'].round()

st.markdown("""---""")

# SALES( BY PRODUCT LINE [BAR CHART]

fig_Gruppo1_qta = px.bar(
    Lista_Gruppo1_Qta,
    y="Quantita",
    x=Lista_Gruppo1_Qta.index,
    orientation="v",
    title="<b>Articoli </b>",
    color_discrete_sequence=["#0083B8"] * len(Lista_Gruppo1_Qta),
    template="plotly_white",
    labels={'Articoli': 'Numero'}, height=400
)
fig_Gruppo1_qta.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

#left_column, right_column = st.columns(2)
left_column, right_column = st.columns([400,150])
right_column.write(Lista_Gruppo1_Qta)
left_column.plotly_chart(fig_Gruppo1_qta, use_container_width=True)

st.markdown("""---""")


fig_Gruppo1_punti = px.bar(
    Lista_Gruppo1_Punti,
    y="Punti",
    x=Lista_Gruppo1_Punti.index,
    orientation="v",
    title="<b>Articoli</b>",
    color_discrete_sequence=["#0083B8"] * len(Lista_Gruppo1_Punti),
    template="plotly_white",
    labels={'Articoli': 'Numero'}, height=400, width=1600,

)
fig_Gruppo1_punti.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

left_column, right_column = st.columns([400,150])
right_column.write(Lista_Gruppo1_Punti)
left_column.plotly_chart(fig_Gruppo1_punti, use_container_width=True)

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
