import yfinance as yf
import pandas as pd
import pandas_ta as ta

def download_data(symbols, period= '2d', interval= '5m', group_by= None):
    if isinstance(symbols, list):
        symbols = " ".join(symbols)
    if isinstance(symbols, str):
        pass
    df = yf.download(symbols, period= period, interval= interval, group_by= group_by, auto_adjust= True, progress= False, threads= True)
    if interval in ['1m', '2m', '5m', '15m', '30m', '60m', '90m']:
        df.index = df.index.tz_convert('Asia/Kolkata')
    return df

def breakthrough_detect(symbols):
    df = download_data(symbols, group_by= 'ticker')
    breakthrough= {
        'Symbol': [],
        'Close': [],
        'Previous High': [],
        'Previous Low': [],
        'Percentage Difference': [],
        'Breakthrough Type':[]
    }

    for symbol in df.columns.levels[0]:
        breakthrough['Symbol'].append(symbol)
        data = df[symbol]
        data = data[data['Close'] != 0]
        current = data["Close"].iloc[-1]
        breakthrough['Close'].append(current)
        prev_day = data[data.index.normalize() == data.index.normalize().unique()[-2]]
        prev_high = prev_day["High"].max()
        prev_low  = prev_day["Low"].min()

        if current > prev_high:
            per_diff = (f"+{(((current - prev_high) / prev_high) * 100):.2f}%")
            breakthrough['Breakthrough Type'].append(f"BreakOut ({per_diff} above previous high)")

        elif current < prev_low:
            per_diff = (f"-{(((current - prev_low) / prev_low) * 100):.2f}%")
            breakthrough['Breakthrough Type'].append(f"BreakDown ({per_diff} below previous low)")

        else:   
            breakthrough['Breakthrough Type'].append("Neutral")
            per_diff = 'N/A'
        
        breakthrough['Percentage Difference'].append(per_diff)
        breakthrough['Previous High'].append(prev_high)
        breakthrough['Previous Low'].append(prev_low)
    break_df = pd.DataFrame(breakthrough)
    return break_df

symbols = ['TMPV.NS', 'SHRIRAMFIN.NS', 'TATASTEEL.NS', 'CANBK.NS', 'HDFCBANK.NS', 'MOTHERSON.NS', 'ETERNAL.NS', 'VEDL.NS', 'POWERGRID.NS', 'IOC.NS', 'ICICIBANK.NS', 'RELIANCE.NS', 'INFY.NS', 'WIPRO.NS', 'BEL.NS', 'NTPC.NS', 'ITC.NS', 'BHARTIARTL.NS', 'PNB.NS']

def ma(df, length= 40):
    close= df['Close']
    ma = ta.sma(close, length= length)
    return ma

def ema(df, length= 40):
    close = df['Close']
    ema = ta.ema(close, length= length)
    return ema

def bb(df, length= 20, std= 2):
    close= df['Close']
    bb_df = ta.bbands(close, length, std)
    bb_df.columns= ["BBL", "BBM", "BBU", "BBB", "BBP"]
    return bb_df

def colorize_row(row):
    if 'BreakOut' in row['Breakthrough Type']:
        return ['background-color: green; color: white'] * len(row)
    elif 'BreakDown' in row['Breakthrough Type']:
        return ['background-color: red; color: white'] * len(row)
    else:
        return ['background-color: grey; color: white'] * len(row)

    