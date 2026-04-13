import json
import requests
import streamlit as st


st.set_page_config(page_title="Crypto AI API Tester", page_icon="🪙", layout="wide")
st.title("🪙 Crypto AI API - Hugging Face Tester")
st.caption("Use this UI to test your deployed Hugging Face Space API.")

DEFAULT_BASE_URL = "https://yashasvi-01-02-crypto-ai-api.hf.space"

base_url = st.text_input("Hugging Face Base URL", value=DEFAULT_BASE_URL).strip().rstrip("/")

COIN_MAPPING = {
    "Bitcoin (BTC)": "bitcoin",
    "Ethereum (ETH)": "ethereum",
    "Binance Coin (BNB)": "binancecoin",
    "Solana (SOL)": "solana",
    "Cardano (ADA)": "cardano",
    "Ripple (XRP)": "ripple",
    "Dogecoin (DOGE)": "dogecoin",
    "Polkadot (DOT)": "polkadot",
    "Avalanche (AVAX)": "avalanche-2",
    "Chainlink (LINK)": "chainlink",
    "Polygon (MATIC)": "polygon",
    "Litecoin (LTC)": "litecoin",
    "Tron (TRX)": "tron",
    "Shiba Inu (SHIB)": "shiba-inu",
    "Uniswap (UNI)": "uniswap",
}

col1, col2 = st.columns(2)
with col1:
    selected_coin_name = st.selectbox("Coin", list(COIN_MAPPING.keys()), index=0)
    coin_id = COIN_MAPPING[selected_coin_name]
with col2:
    forecast_days = st.slider("Forecast Days", min_value=1, max_value=30, value=7)

timeout = st.slider("Request Timeout (sec)", min_value=5, max_value=120, value=40)


def call_api(path: str):
    url = f"{base_url}{path}"
    try:
        response = requests.get(url, timeout=timeout)
        payload = response.json() if response.content else {}
        return response.status_code, payload, url
    except requests.RequestException as exc:
        return None, {"error": str(exc)}, url
    except json.JSONDecodeError:
        return None, {"error": "Invalid JSON response from API."}, url


def render_response(title: str, path: str):
    st.subheader(title)
    status_code, payload, url = call_api(path)
    st.code(url)

    if status_code is None:
        st.error(payload.get("error", "Request failed."))
        return

    if 200 <= status_code < 300:
        st.success(f"Status: {status_code}")
        st.json(payload)
    else:
        st.error(f"Status: {status_code}")
        st.json(payload)


tab1, tab2, tab3, tab4 = st.tabs(["Insights", "Predict", "Risk", "Price"])

with tab1:
    if st.button("Run Insights", use_container_width=True):
        render_response("Insights Response", f"/insights/{coin_id}?forecast_days={forecast_days}")

with tab2:
    if st.button("Run Predict", use_container_width=True):
        render_response("Predict Response", f"/predict/{coin_id}?days={forecast_days}")

with tab3:
    if st.button("Run Risk", use_container_width=True):
        render_response("Risk Response", f"/risk/{coin_id}")

with tab4:
    if st.button("Run Price", use_container_width=True):
        render_response("Price Response", f"/price/{coin_id}")
