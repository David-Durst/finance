import yfinance as yf

def print_key_values():
    #print(yf.__version__)
    micron = yf.Ticker('MU')
    info = micron.info
    financials = micron.financials
    #print(microsoft.get_earnings_forecast())
    print([k for k in info.keys() if 'eps' in k.lower()])
    print([k for k in info.keys() if 'revenue' in k.lower()])
    print([k for k in info.keys() if 'margin' in k.lower()])
    print([k for k in info.keys() if 'target' in k.lower()])
    print([k for k in info.keys() if 'income' in k.lower()])
    print(financials)

if __name__ == '__main__':
    print_key_values()
