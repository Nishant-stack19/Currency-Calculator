import streamlit as st
import pandas as pd
import pymysql
pymysql.install_as_MySQLdb()
from sqlalchemy import create_engine
import os
from datetime import datetime
import uuid
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

# Cached DB connection
@st.cache_resource
def init_database():
    """Initialize database connection from .env or fallback"""
    database_url = os.getenv('DATABASE_URL')

    if not database_url:
        st.warning("DATABASE_URL not found in .env. Using fallback localhost:3307.")
        database_url = "mysql+pymysql://root:Nishu#1234@localhost:3307/currency_converter_app_db"

    try:
        return create_engine(database_url)
    except Exception as e:
        st.error(f"Failed to connect to database: {e}")
        return None

# Cached exchange rates from Frankfurter API
@st.cache_data(ttl=3600)
def get_exchange_rates():
    """Fetch live exchange rates from Frankfurter API (base: USD)"""
    try:
        response = requests.get("https://api.frankfurter.app/latest?from=USD")
        data = response.json()

        if 'rates' not in data:
            raise ValueError("No 'rates' in API response")

        rates = data['rates']
        rates['USD'] = 1.0  # Add base currency

        currency_names = {
            'USD': 'US Dollar', 'EUR': 'Euro', 'GBP': 'British Pound', 'JPY': 'Japanese Yen',
            'CAD': 'Canadian Dollar', 'AUD': 'Australian Dollar', 'CHF': 'Swiss Franc',
            'CNY': 'Chinese Yuan', 'INR': 'Indian Rupee', 'KRW': 'South Korean Won'
        }

        # Filter supported currencies
        filtered_rates = {code: rates[code] for code in currency_names if code in rates}
        return filtered_rates, currency_names

    except Exception as e:
        st.error(f"Error fetching exchange rates: {e}")
        return {}, {}

def convert_currency(amount, from_currency, to_currency, exchange_rates):
    usd_amount = amount / exchange_rates[from_currency]
    return usd_amount * exchange_rates[to_currency]

def format_currency(amount, currency_code):
    if currency_code in ['JPY', 'KRW']:
        return f"{amount:,.0f} {currency_code}"
    return f"{amount:,.2f} {currency_code}"

def save_conversion_history(amount, from_currency, to_currency, converted_amount, exchange_rate, session_id):
    engine = init_database()
    if engine is None:
        return
    try:
        query = """
        INSERT INTO conversion_history 
        (amount, from_currency, to_currency, converted_amount, exchange_rate, user_session)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        conn = engine.raw_connection()
        cursor = conn.cursor()
        cursor.execute(query, (amount, from_currency, to_currency, converted_amount, exchange_rate, session_id))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        st.warning(f"Failed to save conversion history: {e}")

def get_conversion_history(session_id, limit=10):
    engine = init_database()
    if engine is None:
        return pd.DataFrame()
    try:
        query = """
        SELECT amount, from_currency, to_currency, converted_amount, 
               exchange_rate, conversion_date
        FROM conversion_history 
        WHERE user_session = %s
        ORDER BY conversion_date DESC
        LIMIT %s
        """
        return pd.read_sql(query, engine, params=(session_id, limit))
    except Exception:
        return pd.DataFrame()

def main():
    st.set_page_config(
        page_title="Currency Converter",
        page_icon="💱",
        layout="centered"
    )

    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

    EXCHANGE_RATES, CURRENCY_NAMES = get_exchange_rates()

    st.title("💱 Currency Converter")
    st.markdown("Convert between major world currencies using **real-time exchange rates**.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("From")
        amount = st.number_input("Amount", min_value=0.0, value=100.0, step=1.0, format="%.2f")
        from_currency = st.selectbox(
            "Source Currency",
            options=list(EXCHANGE_RATES.keys()),
            index=list(EXCHANGE_RATES.keys()).index('USD') if 'USD' in EXCHANGE_RATES else 0,
            format_func=lambda x: f"{x} - {CURRENCY_NAMES.get(x, x)}"
        )

    with col2:
        st.subheader("To")
        to_currency = st.selectbox(
            "Target Currency",
            options=list(EXCHANGE_RATES.keys()),
            index=list(EXCHANGE_RATES.keys()).index('EUR') if 'EUR' in EXCHANGE_RATES else 0,
            format_func=lambda x: f"{x} - {CURRENCY_NAMES.get(x, x)}"
        )

    if amount >= 0:
        try:
            converted_amount = convert_currency(amount, from_currency, to_currency, EXCHANGE_RATES)

            if from_currency != to_currency:
                rate = EXCHANGE_RATES[to_currency] / EXCHANGE_RATES[from_currency]
                save_conversion_history(
                    amount, from_currency, to_currency,
                    converted_amount, rate, st.session_state.session_id
                )

            st.markdown("---")
            st.subheader("Conversion Result")

            result_col1, result_col2, result_col3 = st.columns([1, 1, 1])
            with result_col1:
                st.metric("From", format_currency(amount, from_currency))
            with result_col2:
                st.markdown("**→**", unsafe_allow_html=True)
            with result_col3:
                st.metric("To", format_currency(converted_amount, to_currency))

            if from_currency != to_currency:
                st.info(f"Exchange Rate: 1 {from_currency} = {rate:.4f} {to_currency}")
            else:
                st.info("Same currency selected - no conversion needed")
        except Exception as e:
            st.error(f"Error during conversion: {str(e)}")
    else:
        st.warning("Enter a valid amount.")

    st.markdown("---")
    st.markdown("### 📊 Conversion History")

    history_df = get_conversion_history(st.session_state.session_id)
    if not history_df.empty:
        display_df = history_df.copy()
        display_df['conversion_date'] = pd.to_datetime(display_df['conversion_date']).dt.strftime('%Y-%m-%d %H:%M')
        display_df = display_df.rename(columns={
            'amount': 'Amount',
            'from_currency': 'From',
            'to_currency': 'To',
            'converted_amount': 'Result',
            'exchange_rate': 'Rate',
            'conversion_date': 'Date'
        })
        display_df['Amount'] = display_df['Amount'].round(2)
        display_df['Result'] = display_df['Result'].round(2)
        display_df['Rate'] = display_df['Rate'].round(4)
        st.dataframe(display_df, use_container_width=True)
    else:
        st.info("No conversion history yet.")

    st.markdown("---")
    st.markdown("### 📚 Educational Notes")

    with st.expander("About Exchange Rates"):
        st.markdown("""
        These rates are fetched from the **Frankfurter API**, updated hourly.

        **Base Currency:** USD  
        **Formula:**
        - Convert A to USD → `USD = amount / rate_A`
        - Convert USD to B → `B = USD × rate_B`
        """)

    with st.expander("Supported Currencies"):
        for code, name in CURRENCY_NAMES.items():
            rate = EXCHANGE_RATES.get(code)
            if rate:
                st.markdown(f"• **{code}** - {name} (Rate: {rate:.4f})")
            else:
                st.markdown(f"• **{code}** - {name} (Rate: N/A)")

    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>💡 Built with Streamlit, Python, and real-time APIs & MySQL.</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
