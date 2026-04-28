import pandas as pd
import yfinance as yf
import streamlit as st
import altair as alt
import Brocker as BROCKER
import Activo as ACTIVO
import Portafolio as PORTAFOLIO

@st.cache_data
def cargar_datos(ticker, periodo):
    return yf.Ticker(ticker).history(period=periodo)

st.set_page_config(layout="wide")
st.title("Brocker -- Estructura de Datos 2026-1")

cols = st.columns([1, 3])

STOCKS = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA", "JPM", "BND", "JEPQ"]

with cols[0]:
    tickers = st.multiselect("Selecciona activos", STOCKS, default=["AAPL"])

    horizon_map = {
        "1 Mes": "1mo",
        "6 Meses": "6mo",
        "1 Año": "1y"
    }

    horizon = st.selectbox("Horizonte", list(horizon_map.keys()))
    periodo = horizon_map[horizon]

    cantidad = st.number_input("Cantidad", 1, 100, 10)

activos = []
for t in tickers:
    data = cargar_datos(t, periodo)
    if not data.empty:
        activos.append(ACTIVO.Activo(t, data))

if not activos:
    st.stop()

if "portafolio" not in st.session_state:
    st.session_state.portafolio = PORTAFOLIO.Portafolio(100000)

portafolio = st.session_state.portafolio

with cols[0]:
    if st.button("Comprar"):
        for a in activos:
            st.success(portafolio.comprar(cantidad, a))

    ticker_vender = st.selectbox("Vender activo", tickers)
    cantidad_vender = st.number_input("Cantidad a vender", 1, 100, 1)

    if st.button("Vender"):
        st.warning(portafolio.vender(ticker_vender, cantidad_vender))

df_total = pd.concat([
    a.data_actual.assign(Stock=a.nombre)
    for a in activos
]).reset_index()

with cols[1]:
    st.altair_chart(
        alt.Chart(df_total)
        .mark_line()
        .encode(
            x="Date:T",
            y="Close:Q",
            color="Stock:N"
        ),
        use_container_width=True
    )

with cols[1]:
    c1, c2, c3 = st.columns(3)

    c1.metric("Valor Portafolio", f"${portafolio.valor():.2f}")
    c2.metric("Rentabilidad", f"{portafolio.rentabilidad()*100:.2f}%")
    c3.metric("Capital", f"${portafolio.capital:.2f}")

with cols[0]:
    for a in activos:
        st.subheader(a.nombre)

        st.metric("Precio", f"${a.precio_actual:,.2f}")

        st.markdown(
            f"<div style='font-size:15px; color:green;'>"
            f"Mín: ${a.minimo():,.2f} &nbsp;&nbsp;|&nbsp;&nbsp; "
            f"Máx: ${a.maximo():,.2f}"
            f"</div>",
            unsafe_allow_html=True
        )