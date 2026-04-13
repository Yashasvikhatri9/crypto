# Crypto AI API Documentation

This document describes the inputs, outputs, and functionality of all endpoints in the Crypto AI API, as well as the supported coins.

## Supported Coins

There are **15** supported cryptocurrencies in the system. Use the **Coin ID** when passing parameters to the API endpoints.

| Coin Name | Coin ID (Use in API) | Ticker |
| :--- | :--- | :--- |
| Bitcoin | `bitcoin` | BTC |
| Ethereum | `ethereum` | ETH |
| Binance Coin | `binancecoin` | BNB |
| Solana | `solana` | SOL |
| Cardano | `cardano` | ADA |
| Ripple | `ripple` | XRP |
| Dogecoin | `dogecoin` | DOGE |
| Polkadot | `polkadot` | DOT |
| Avalanche | `avalanche-2` | AVAX |
| Chainlink | `chainlink` | LINK |
| Polygon | `polygon` | MATIC |
| Litecoin | `litecoin` | LTC |
| Tron | `tron` | TRX |
| Shiba Inu | `shiba-inu` | SHIB |
| Uniswap | `uniswap` | UNI |

---

## API Endpoints Overview

The API is built using FastAPI and runs on port `7860`. By default, you can access the interactive Swagger documentation at `/docs` or ReDoc at `/redoc` when the server is running.

### 1. Root / Health Status
Check if the API is online and see basic metadata.

* **Endpoint:** `GET /`
* **Input Parameters:** None
* **Output (JSON):** Service status, API version, supported endpoints, timestamp.

* **Endpoint:** `GET /health`
* **Input Parameters:** None
* **Output (JSON):** `{"status": "ok", "timestamp": "..."}`

---

### 2. Price Prediction (`/predict`)
Provides an LSTM/Ensemble-based price prediction for the next N days.

* **Endpoint:** `GET /predict/{coin_id}`
* **Input Parameters:**
  * `coin_id` (Path, String): The ID of the coin (e.g., `bitcoin`)
  * `days` (Query, Integer, Optional): Forecast horizon between 1–30 days. Default is 7.
* **Output (JSON):**
  * `coin_id`: Coin identifier.
  * `current_price_usd`: Most recent close price.
  * `forecast_days`: The requested forecast horizon.
  * `predicted_prices`: List of predicted price values.
  * `predicted_change_pct`: Percentage change expected.
  * `direction`: Expected trend (e.g., up, down).
  * `confidence`: Model confidence score (0-1).
  * `ensemble_data`: Raw LSTM vs XGBoost agreement scores.

---

### 3. Risk Analysis (`/risk`)
Computes multi-factor risk analysis including volatility, RSI extremes, volume spikes, and drawdown.

* **Endpoint:** `GET /risk/{coin_id}`
* **Input Parameters:**
  * `coin_id` (Path, String): The ID of the coin.
* **Output (JSON):**
  * `coin_id`: Coin identifier.
  * `risk_level`: Evaluated state (e.g., `LOW`, `MEDIUM`, `HIGH`).
  * `risk_score`: Score estimating the severity of risk on a 0-100 scale.

---

### 4. Action Recommendation (`/recommendation`)
Uses a weighted array of technical indicators (RSI, MACD crossover, Bollinger Bands, EMAs) to suggest an action.

* **Endpoint:** `GET /recommendation/{coin_id}`
* **Input Parameters:**
  * `coin_id` (Path, String): The ID of the coin.
* **Output (JSON):**
  * `coin_id`: Coin identifier.
  * `action`: Action to take (e.g., `BUY`, `SELL`, `HOLD`).
  * Details inside the response payload backing up the signal.

---

### 5. News Sentiment (`/sentiment`)
Retrieves news headlines and analyzes sentiment via VADER. 

* **Endpoint:** `GET /sentiment/{coin_id}`
* **Input Parameters:**
  * `coin_id` (Path, String): The ID of the coin.
* **Output (JSON):**
  * `coin_id`: Coin identifier.
  * `sentiment`: Overall mood (e.g., `POSITIVE`, `NEGATIVE`, `NEUTRAL`).
  * `compound_score`: Overall composite sentiment score.

---

### 6. Master Insights (`/insights`)
Retrieves combined metadata calling prediction, risk, recommendation, and sentiment in a single master request. 

* **Endpoint:** `GET /insights/{coin_id}`
* **Input Parameters:**
  * `coin_id` (Path, String): The ID of the coin.
  * `forecast_days` (Query, Integer, Optional): Horizon limit. Default 7.
* **Output (JSON):**
  * `coin_id`: Coin identifier.
  * `current_price_usd`: Most recent close price.
  * `prediction`: Full prediction object.
  * `risk`: Full risk assessment payload.
  * `recommendation`: Full recommendation assessment.
  * `sentiment`: Sentiment details.
  * `ai_insight`: Human-readable summary string merging all factors together.

---

### 7. Utility Endpoints
Fetch supplementary market data or enumerations.

* **Endpoint:** `GET /coins`
  * **Output (JSON):** List of all allowed `buy/predict/{coin_id}` parameters.
* **Endpoint:** `GET /price/{coin_id}`
  * **Input Parameters:** `coin_id`
  * **Output (JSON):** Basic coin info like `price_usd`, `market_cap_usd`, `volume_24h_usd`, `change_24h_pct`. 

---
