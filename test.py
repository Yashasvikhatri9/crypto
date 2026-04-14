```python
import json
import requests
import streamlit as st

# ── Page Config ─────────────────────────────────────────────
st.set_page_config(
    page_title="Crypto AI API Tester",
    page_icon="🪙",
    layout="wide"
)

st.title("🪙 Crypto AI API - Hugging Face Tester")
st.caption("Test your FastAPI endpoints deployed on Hugging Face Spaces")

# ── Base URL ────────────────────────────────────────────────
DEFAULT_BASE_URL = "https://yashasvi-01-02-crypto-ai-api.hf.space"

base_url = st.text_input(
    "🔗 Hugging Face Base URL",
    value=DEFAULT_BASE_URL
).strip().rstrip("/")

# ── Inputs ─────────────────────────────────────────────────
coins = [
    "bitcoin", "ethereum", "binancecoin", "solana", "cardano",
    "ripple", "dogecoin", "polkadot", "avalanche-2", "chainlink",
    "polygon", "litecoin", "tron", "shiba-inu", "uniswap",
]

col1, col2 = st.columns(2)

with col1:
    coin_id = st.selectbox("🪙 Select Coin", coins)

with col2:
    forecast_days = st.slider("📅 Forecast Days", 1, 30, 7)

timeout = st.slider("⏱ Request Timeout (sec)", 5, 120, 40)

# ── API Caller ─────────────────────────────────────────────
def call_api(path: str):
    url = f"{base_url}{path}"

    try:
        response = requests.get(
            url,
            timeout=timeout,
            headers={"Accept": "application/json"}
        )

        try:
            payload = response.json()
        except:
            payload = {"raw_response": response.text}

        return response.status_code, payload, url

    except requests.RequestException as exc:
        return None, {"error": str(exc)}, url


# ── Response Renderer ──────────────────────────────────────
def render_response(title: str, path: str):
    st.subheader(title)

    with st.spinner("🚀 Calling API..."):
        status_code, payload, url = call_api(path)

    st.code(url)

    if status_code is None:
        st.error(payload.get("error", "Request failed"))
        return

    if 200 <= status_code < 300:
        st.success(f"✅ Status: {status_code}")
        st.json(payload)
    elif status_code == 404:
        st.warning("⚠️ Coin not found or unsupported")
        st.json(payload)
    else:
        st.error(f"❌ Status: {status_code}")
        st.json(payload)


# ── Tabs ───────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["🧠 Insights", "📈 Predict", "⚠️ Risk", "💰 Price", "🪙 Coins"]
)

# ── Insights ───────────────────────────────────────────────
with tab1:
    if st.button("Run Insights", use_container_width=True):
        render_response(
            "🧠 Insights Response",
            f"/insights/{coin_id}?forecast_days={forecast_days}"
        )

# ── Predict ────────────────────────────────────────────────
with tab2:
    if st.button("Run Prediction", use_container_width=True):
        render_response(
            "📈 Prediction Response",
            f"/predict/{coin_id}?days={forecast_days}"
        )

# ── Risk ───────────────────────────────────────────────────
with tab3:
    if st.button("Run Risk Analysis", use_container_width=True):
        render_response(
            "⚠️ Risk Response",
            f"/risk/{coin_id}"
        )

# ── Price ──────────────────────────────────────────────────
with tab4:
    if st.button("Get Live Price", use_container_width=True):
        render_response(
            "💰 Price Response",
            f"/price/{coin_id}"
        )

# ── Coins ──────────────────────────────────────────────────
with tab5:
    if st.button("List Supported Coins", use_container_width=True):
        render_response(
            "🪙 Coins List",
            "/coins"
        )

# ── Footer ─────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "Built with ❤️ using FastAPI + Streamlit | Deployed on Hugging Face Spaces"
)