def SMA (df, period=21):
    df[f'{period}_SMA'] = df.Close.rolling(period).mean()
    
    return df

def Stochastic_Oscillator(df,period=14, mm_d1=3,mm_d2=3):
    df[f'Low {period}'] = df.Low.rolling(period).min()
    df[f'High {period}'] = df.High.rolling(period).max()
    df['%K'] = (df['Close'] - df[f'Low {period}'])*100 / (df[f'High {period}'] - df[f'Low {period}'])
    df['%D(Rapido)'] = df['%K'].rolling(mm_d1).mean()
    
    return df

def Stochastic_Oscillator_v2(df,period=14,tipo='rapido', mm_d1=3,mm_d2=3):
    df[f'Low {period}'] = df.Low.rolling(period).min()
    df[f'High {period}'] = df.High.rolling(period).max()
    df['%K'] = (df['Close'] - df[f'Low {period}'])*100 / (df[f'High {period}'] - df[f'Low {period}'])

    if tipo == 'rapido':
        df['%D(Rapido)'] = df['%K'].rolling(mm_d1).mean()
        return df
    elif tipo =='lento':
        df['%D(Rapido)'] = df['%K'].rolling(mm_d1).mean()
        df['%D(Lento)'] = df['%D(Rapido)'].rolling(mm_d2).mean()
        df.drop('%K',inplace=True,axis=1)
        
        return df


def RSI(df,ema_decay=13, adjust=False):
    df['Delta'] = delta = df['Close'].diff() 
    df['Positivo'] = positivo = delta.clip(lower=0) 
    df['Negativo'] = negativo = abs(delta.clip(upper=0)) 
    df['EMA_Positiva'] = ema_positivo = positivo.ewm(com=ema_decay, adjust=adjust).mean() 
    df['EMA_Negativa'] = ema_negativo = negativo.ewm(com=ema_decay,adjust=adjust).mean()
    df['RS'] = RS = ema_positivo/ema_negativo
    df['RSI'] = RSI = (100/(1 + RS))

    return df