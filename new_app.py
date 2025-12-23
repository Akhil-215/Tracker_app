import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.graph_objects as go
import time
from index_by_volume import main
from functions import*

if "period_list" not in st.session_state:
    st.session_state.period_list = ['1d', '3d', '5d', '1mo']
intervals = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1d', '5d', '1wk', '1mo', '3mo']


index_list= ['NIFTY 50', 'NIFTY FINANCIAL SERVICES', 'NIFTY MIDCAP SELECT', 'NIFTY NEXT 50', 'NIFTY 100', 'NIFTY 200', 'NIFTY 500', 'NIFTY INDIA FPI 150', 'NIFTY LARGEMIDCAP 250', 'NIFTY MICROCAP 250', 'NIFTY MIDCAP 100', 'NIFTY MIDCAP 150', 'NIFTY MIDCAP 50', 'NIFTY MIDSMALLCAP 400', 'NIFTY SMALLCAP 100', 'NIFTY SMALLCAP 250', 'NIFTY SMALLCAP 50', 'NIFTY TOTAL MARKET', 'NIFTY500 LARGEMIDSMALL EQUAL-CAP WEIGHTED', 'NIFTY500 MULTICAP 50:25:25', 'NIFTY AUTO', 'NIFTY CHEMICALS', 'NIFTY CONSUMER DURABLES', 'NIFTY FINANCIAL SERVICES EX-BANK', 'NIFTY FINANCIAL SERVICES 25/50', 'NIFTY FMCG', 'NIFTY HEALTHCARE INDEX', 'NIFTY IT', 'NIFTY MEDIA', 'NIFTY METAL', 'NIFTY MIDSMALL HEALTHCARE', 'NIFTY MIDSMALL FINANCIAL SERVICES', 'NIFTY MIDSMALL IT & TELECOM', 'NIFTY OIL & GAS', 'NIFTY PHARMA', 'NIFTY PSU BANK', 'NIFTY PRIVATE BANK', 'NIFTY REALTY', 'NIFTY500 HEALTHCARE', 'NIFTY CAPITAL MARKETS', 'NIFTY COMMODITIES', 'NIFTY INDIA CONSUMPTION', 'NIFTY CORE HOUSING', 'NIFTY INDIA SELECT 5 CORPORATE GROUPS (MAATR)', 'NIFTY CPSE', 'NIFTY ENERGY', 'NIFTY EV & NEW AGE AUTOMOTIVE', 'NIFTY HOUSING', 'NIFTY INDIA DEFENCE', 'NIFTY INDIA DIGITAL', 'NIFTY INDIA TOURISM', 'NIFTY INDIA MANUFACTURING', 'NIFTY INFRASTRUCTURE', 'NIFTY INDIA INFRASTRUCTURE & LOGISTICS', 'NIFTY INDIA INTERNET', 'NIFTY IPO', 'NIFTY MIDCAP LIQUID 15', 'NIFTY MNC', 'NIFTY MOBILITY', 'NIFTY MIDSMALL INDIA CONSUMPTION', 'NIFTY500 MULTICAP INFRASTRUCTURE 50:30:20', 'NIFTY500 MULTICAP INDIA MANUFACTURING 50:30:20', 'NIFTY INDIA NEW AGE CONSUMPTION', 'NIFTY NON-CYCLICAL CONSUMER', 'NIFTY PSE', 'NIFTY RURAL', 'NIFTY SERVICES SECTOR', 'NIFTY SHARIAH 25', 'NIFTY SME EMERGE', 'NIFTY INDIA CORPORATE GROUP INDEX - TATA GROUP 25% CAP', 'NIFTY TRANSPORTATION & LOGISTICS', 'NIFTY WAVES', 'NIFTY100 ENHANCED ESG', 'NIFTY100 ESG', 'NIFTY100 LIQUID 15', 'NIFTY50 SHARIAH', 'NIFTY500 SHARIAH', 'NIFTY ALPHA 50', 'NIFTY ALPHA LOW-VOLATILITY 30', 'NIFTY ALPHA QUALITY LOW-VOLATILITY 30', 'NIFTY ALPHA QUALITY VALUE LOW-VOLATILITY 30', 'NIFTY DIVIDEND OPPORTUNITIES 50', 'NIFTY GROWTH SECTORS 15', 'NIFTY HIGH BETA 50', 'NIFTY LOW VOLATILITY 50', 'NIFTY MIDCAP150 QUALITY 50', 'NIFTY500 MULTICAP MOMENTUM QUALITY 50', 'NIFTY QUALITY LOW-VOLATILITY 30', 'NIFTY SMALLCAP250 QUALITY 50', 'NIFTY TOTAL MARKET MOMENTUM QUALITY 50', 'NIFTY TOP 10 EQUAL WEIGHT', 'NIFTY TOP 15 EQUAL WEIGHT', 'NIFTY TOP 20 EQUAL WEIGHT', 'NIFTY100 ALPHA 30', 'NIFTY100 EQUAL WEIGHT', 'NIFTY100 LOW VOLATILITY 30', 'NIFTY100 QUALITY 30', 'NIFTY200 ALPHA 30', 'NIFTY200 QUALITY 30', 'NIFTY200 VALUE 30', 'NIFTY200 MOMENTUM 30', 'NIFTY50 EQUAL WEIGHT', 'NIFTY50 VALUE 20', 'NIFTY500 EQUAL WEIGHT', 'NIFTY500 FLEXICAP QUALITY 30', 'NIFTY500 LOW VOLATILITY 50', 'NIFTY500 MULTIFACTOR MQVLV 50', 'NIFTY500 QUALITY 50', 'NIFTY500 VALUE 50', 'NIFTY500 MOMENTUM 50', 'NIFTY MIDCAP150 MOMENTUM 50', 'NIFTY MIDSMALLCAP400 MOMENTUM QUALITY 100', 'NIFTY SMALLCAP250 MOMENTUM QUALITY 100', 'PERMITTED TO TRADE', 'SECURITIES IN F&O']

# Function to change periods to only available periods for the interval
def av_period():
    if st.session_state.interval in ['1m', '2m']:
        st.session_state.period_list = ['1d', '2d', '3d', '5d', '7d']
    elif st.session_state.interval in ['5m', '15m', '30m']:
        st.session_state.period_list = ['1d', '2d', '3d', '5d', '7d', '15d', '1mo']
    elif st.session_state.interval in ['60m', '90m']:
        st.session_state.period_list = ['1d', '3d', '5d', '1mo', '2mo']
    elif st.session_state.interval in ['1d', '5d', '1wk', '1mo', '3mo']:
        st.session_state.period_list = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y']

# Function to update session state values for plot
def change_plot_values():
    st.session_state.symbol_selected = selected_symbol
    st.session_state.interval = selected_interval
    st.session_state.period = selected_period

# Function to update bollinger bands parameters
def change_bb_values():
    st.session_state.bb_length= bb_length
    st.session_state.bb_std= bb_std

# Cache for data functions
@st.cache_data(show_spinner= False)
def download_symbol_data(symbol, period, interval):
    s_data = download_data(symbol, period= period, interval= interval)
    return s_data

@st.cache_data(show_spinner= False)
def fetch_index_data(index):
    indices = main(index)
    return indices

# Function to reset plot indicators
def reset_indicators():
    st.session_state.ta_list = []

# Function to get symbol data if values of symbol, period, interval changed
def get_symbol_data():
    key = (st.session_state.symbol_selected, st.session_state.period, st.session_state.interval)

    if st.session_state.get("data_key") != key:
        s_data = download_symbol_data(*key)
        st.session_state.symbol_data = s_data[st.session_state.symbol_selected]
        st.session_state.last_fetch = 0
        st.session_state.data_key = key

    return st.session_state.symbol_data if st.session_state.symbol_data is not None else None





# Initialize session states
if "last_fetch" not in st.session_state:
    st.session_state.last_fetch = 0
if "ta_list" not in st.session_state:
    st.session_state.ta_list = []
if "symbol_data" not in st.session_state:
    st.session_state.symbol_data = None
if "data_key" not in st.session_state:
    st.session_state.data_key = None
if "selected_index" not in st.session_state:
    st.session_state.selected_index= None
if "symbol_list" not in st.session_state:
    st.session_state.symbol_list= None
if "show_plot" not in st.session_state:
    st.session_state.show_plot = False

# Page Initial State

st.title("NSE Index and Stock Tracker")

# Select box for Index
index_selected = st.selectbox("Select a NSE Index", options= [None] + index_list, index=0)
fetch_button = st.button("Fetch")

if fetch_button and index_selected:
    st.session_state.selected_index= index_selected

# If selected, move controls to sidebar
if st.session_state.selected_index:
    

    selected_tab = option_menu(menu_title= "View Options", options= ["Data View", "Plot View"], default_index= 0, orientation= "vertical")

    # Tabs
    if selected_tab == "Data View":
        try:
            indices = fetch_index_data(st.session_state.selected_index)

            st.subheader(f"Breakthrough Data for {st.session_state.selected_index}")
            if not indices:
                st.write('Error Loading Top 20 Stocks.')
            if indices:
                df= pd.DataFrame(indices)
                symbols = (df['SYMBOL'] + '.NS').to_list()
                st.session_state.symbol_list= symbols

                breakthrough = breakthrough_detect(st.session_state.symbol_list)
                breakthrough_filtered = breakthrough[breakthrough['Breakthrough Type'] != 'Neutral']
                df_reset = breakthrough_filtered.reset_index(drop= True)
                if not breakthrough.empty:
                    st.write("### Stock Movement Overview")
                    st.dataframe(df_reset[['Symbol', 'Close', 'Breakthrough Type']].style.apply(colorize_row, axis= 1))
        
        except Exception as e:
            st.warning(f"Error: {e}")

    if selected_tab == "Plot View":
        st.subheader(f"Plot Controls for {st.session_state.selected_index}")

        col1,col2, col3 = st.columns([2,1,1])
        with col1:
            selected_symbol= st.selectbox("Select a Symbol", options=st.session_state.symbol_list, index=None, on_change= reset_indicators)
        with col2:
            selected_interval = st.selectbox("Interval", options= intervals, index= 2, key= "interval", on_change= av_period)
        with col3:
            selected_period = st.selectbox("Period", options= st.session_state.period_list, index=0)
        plot_button = st.button("Plot", on_click= change_plot_values)
        if plot_button:
            st.session_state.show_plot = True

        if st.session_state.show_plot:
                if (
                    st.session_state.symbol_selected is None
                    or st.session_state.period is None
                    or st.session_state.interval is None
                ):
                    st.warning("Please select Symbol, Period and Interval")
                    st.stop()

                symbol_data = get_symbol_data()
                    
                fig = go.Figure()
                # CandleStick Plot
                fig.add_trace(go.Candlestick(x= symbol_data.index, open=symbol_data['Open'], high=symbol_data['High'], low=symbol_data['Low'], close=symbol_data['Close'], name= 'Candlestick'))


                # Hide non-trading time for intervals less than day
                if st.session_state.interval in ['1m', '2m', '5m', '15m', '30m', '60m', '90m']:
                    fig.update_xaxes(
                        rangebreaks=[
                            dict(bounds=["sat", "mon"]),
                            dict(bounds=[15.15, 9.15], pattern="hour")
                        ]
                    )
                else:
                    fig.update_xaxes(tickformat='%Y-%m-%d', rangebreaks=[dict(bounds=["sat", "mon"])]) # Format ticks as dates

                # -------- Indicators Addition -----------

                ind_clo1, ind_col2= st.columns(2)

                with ind_clo1:
                    add_ta = st.checkbox("Add Indicators", key="add_ta", on_change= reset_indicators)
                    ta_list= st.session_state.get("ta_list", [])

                    if add_ta:
                        ta_type = st.selectbox("Indicator Type", ["MA", "EMA"])
                        length = st.number_input("Length", min_value=1, max_value=200, value=14)

                        button1, button2= st.columns(2)
                        with button1:
                            if st.button("Add Indicator"):
                                ta_list.append((ta_type, length))
                                st.session_state.ta_list = ta_list
                        with button2:
                            if st.button("Reset"):
                                st.session_state.ta_list= []

                    ta_list= st.session_state.ta_list
                    for ta_type, length in ta_list:
                        if ta_type == "MA":
                            fig.add_trace(go.Scatter(
                                x=symbol_data.index,
                                y=ma(symbol_data, length),
                                mode='lines',
                                name=f"MA {length}"
                            ))
                        elif ta_type == "EMA":
                            fig.add_trace(go.Scatter(
                                x=symbol_data.index,
                                y=ema(symbol_data, length),
                                mode='lines',
                                name=f"EMA {length}"
                            ))
                
                with ind_col2:
                    add_bb = st.checkbox("Add Bollinger Bands")
                    if add_bb:
                        if "bb_length" or "bb_std" not in st.session_state:
                            st.session_state.bb_length= 20
                            st.session_state.bb_std= 2.0

                        bb_length= st.number_input("Length", min_value= 1, max_value= 100, value= st.session_state.bb_length)
                        bb_std= st.slider("Standard Deviation", min_value=1.0, max_value=3.0, value=st.session_state.bb_std, step=0.1)

                        if st.button("Update"):
                            st.session_state.bb_length= bb_length
                            st.session_state.bb_std= bb_std

                        bb_df= bb(symbol_data, st.session_state.bb_length, st.session_state.bb_std)
                        print(bb_df)
                        # Plot Bollinger Bands
                        fig.add_trace(go.Scatter(
                            x=bb_df.index,
                            y=bb_df['BBU'],
                            mode='lines',
                            name='Upper Band',
                            line=dict(color='red', width=2, dash='dash')
                        ))

                        fig.add_trace(go.Scatter(
                            x=bb_df.index,
                            y=bb_df['BBM'],
                            mode='lines',
                            name='Middle Band (SMA)',
                            line=dict(color='blue', width=2)
                        ))

                        fig.add_trace(go.Scatter(
                            x=bb_df.index,
                            y=bb_df['BBL'],
                            mode='lines',
                            name='Lower Band',
                            line=dict(color='green', width=2, dash='dash')
                        ))

                        

                # Layout and Title
                fig.update_layout(
                    title=f'{selected_symbol}',
                    xaxis_title='Date',
                    yaxis_title='Price',
                    xaxis_rangeslider_visible=False,  # Hide range slider
                    template='plotly_dark'  # Optional: Choose a template
                )

                st.plotly_chart(fig, use_container_width= True)
