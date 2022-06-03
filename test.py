
import pandas as pd
import locale
#locale.setlocale(locale.LC_ALL, 'it_IT')
# import calendar
import plotly.graph_objects as go
import streamlit as st
# import plotly.express as px
from plotly.subplots import make_subplots

st.title("Prodotti")  # add title
uploaded_file = st.file_uploader(label="Scegli i file in formato csv", accept_multiple_files=False, type="csv")

if uploaded_file:
    df=pd.read_csv(uploaded_file, delimiter=',', decimal=".", encoding="ISO-8859-1")
    df.fillna(0)
    Prodotti = df.columns.tolist()
    st.sidebar.title("Lista Prodotti")
    Prodotti.remove("Mese")
    prodotti_selezionati = st.sidebar.multiselect(label="", options=Prodotti)
    if prodotti_selezionati:
        check_box = st.checkbox("Crea grafico")
        if check_box:
            rows = len(prodotti_selezionati)
            fig = make_subplots(rows=rows, cols=1, shared_xaxes=True, subplot_titles=prodotti_selezionati)
            for prodotto in prodotti_selezionati:
                fig.add_trace(go.Bar(x=df["Mese"], y=df[prodotto], name=prodotto),
                row=prodotti_selezionati.index(prodotto) + 1, col=1)
            fig.update_layout(showlegend=True, plot_bgcolor='rgb(255,255,255)')
            fig.update_xaxes(showgrid=True, gridwidth=0.05, gridcolor="LightPink",
            zeroline=True, zerolinewidth=2, zerolinecolor='Black')
            fig.update_yaxes(showgrid=True, gridwidth=0.05, gridcolor="LightPink",
            zeroline=True, zerolinewidth=2, zerolinecolor='Black')
            

            st.plotly_chart(fig)
