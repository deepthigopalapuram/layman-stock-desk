import streamlit as st
import yfinance as yf
from google import genai

# Streamlit Page Setup
st.set_page_config(
    page_title="Layman Stock Research Desk", page_icon="📈", layout="centered"
)

st.title("📈 Layman Stock Analysis Desk")
st.markdown(
    "Enter an Indian stock ticker (e.g., `GICRE.NS`, `RELIANCE.NS`, `TCS.NS`) to"
    " run a fundamental value check and get a jargon-free investment verdict."
)

# Input for Ticker Symbol
ticker_symbol = st.text_input(
    "Stock Ticker Symbol (Yahoo Finance format)", value="GICRE.NS"
)

if st.button("Analyze Stock"):
  with st.spinner(
      f"Fetching data and running AI evaluation for {ticker_symbol}..."
  ):
    try:
      # Fetch Data from yfinance
      stock = yf.Ticker(ticker_symbol)
      info = stock.info

      # Extract basic metrics safely
      company_name = info.get("longName", ticker_symbol)
      sector = info.get("sector", "N/A")
      pe_ratio = info.get("trailingPE", "N/A")
      roe = info.get("returnOnEquity", "N/A")
      if roe != "N/A":
        roe = f"{roe * 100:.2f}%"
      debt_to_equity = info.get("debtToEquity", "N/A")
      market_cap = info.get("marketCap", "N/A")
      if market_cap != "N/A":
        market_cap = f"₹{market_cap / 1e7:,.2f} Crore"

      # Display Raw Metrics Summary
      st.subheader(f"📊 Quick Metrics: {company_name}")
      col1, col2, col3, col4 = st.columns(4)
      col1.metric("Market Cap", market_cap)
      col2.metric("P/E Ratio", str(pe_ratio))
      col3.metric("ROE", str(roe))
      col4.metric("Debt/Equity", str(debt_to_equity))

      # Prepare context payload for the AI model
      prompt_payload = f"""
            Analyze the following stock for a conservative, layman retail investor using fundamental value principles:
            - Company Name: {company_name}
            - Sector: {sector}
            - Market Cap: {market_cap}
            - Trailing P/E: {pe_ratio}
            - Return on Equity (ROE): {roe}
            - Debt to Equity: {debt_to_equity}

            Provide your response in 3 structured sections:
            1. **The Core Business:** (1 simple sentence explaining what they do in plain English).
            2. **The Good & The Bad:** (2 concise bullet points covering financial health, valuation risks, or strengths).
            3. **The Final Verdict:** (Choose strictly one: **Green Light / Buy for Long Term**, **Watch / Wait for Better Price**, or **Red Light / Avoid**, followed by a 1-sentence justification).
            """

      # Call Google GenAI API
      client = genai.Client()
      response = client.models.generate_content(
          model="gemini-2.5-flash",
          contents=prompt_payload,
      )

      # Display AI Output
      st.markdown("---")
      st.subheader("💡 Layman Investment Memo")
      st.markdown(response.text)

    except Exception as e:
      st.error(
          f"Error fetching data or generating analysis: {e}. Please check if"
          " the ticker symbol is correct."
      )
