import pandas as pd
from tqdm import tqdm
import ta
# from talib import abstract
import json

import psycopg2
import psycopg2.extras as extras



# -------------------technical indicators -------------------#
def indicators_calculation(DF):
    DF["AwesomeOscilator"] = ta.momentum.awesome_oscillator(
        high=DF["High"], low=DF["Low"], window1=5, window2=34, fillna=False
    )
    DF["KAMA"] = ta.momentum.kama(close=DF["Close"], window=10, fillna=False)
    DF["PercentagePriceOscillator"] = ta.momentum.ppo_signal(
        close=DF["Close"], window_slow=26, window_fast=12, window_sign=9, fillna=False
    )
    DF["PercentagePriceOscillator_hist"] = ta.momentum.ppo_hist(
        close=DF["Close"], window_slow=26, window_fast=12, window_sign=9, fillna=False
    )
    DF["PercentagePriceOscillator_signal"] = ta.momentum.ppo_signal(
        close=DF["Close"], window_slow=26, window_fast=12, window_sign=9, fillna=False
    )
    DF["PercentageVolumeOscillator"] = ta.momentum.pvo(
        volume=DF["Volume"], window_slow=26, window_fast=12, window_sign=9, fillna=False
    )
    DF["PercentageVolumeOscillator_hist"] = ta.momentum.pvo_hist(
        volume=DF["Volume"], window_slow=26, window_fast=12, window_sign=9, fillna=False
    )
    DF["PercentageVolumeOscillator_signal"] = ta.momentum.pvo_signal(
        volume=DF["Volume"], window_slow=26, window_fast=12, window_sign=9, fillna=False
    )
    DF["ROC"] = ta.momentum.roc(close=DF["Close"], window=12, fillna=False)
    DF["RSI"] = ta.momentum.rsi(close=DF["Close"], window=12, fillna=False)
    DF["SotchasticRSI"] = ta.momentum.stochrsi(
        close=DF["Close"], window=12, smooth1=3, smooth2=3, fillna=False
    )
    DF["SotchasticRSI_d"] = ta.momentum.stochrsi_d(
        close=DF["Close"], window=12, smooth1=3, smooth2=3, fillna=False
    )
    DF["SotchasticRSI_k"] = ta.momentum.stochrsi_k(
        close=DF["Close"], window=12, smooth1=3, smooth2=3, fillna=False
    )
    DF["Stochastic_OSC"] = ta.momentum.stoch(
        close=DF["Close"],
        high=DF["High"],
        low=DF["Low"],
        window=14,
        smooth_window=3,
        fillna=False,
    )
    DF["Stochastic_OSC_Signal"] = ta.momentum.stoch_signal(
        close=DF["Close"],
        high=DF["High"],
        low=DF["Low"],
        window=14,
        smooth_window=3,
        fillna=False,
    )
    DF["TSI"] = ta.momentum.tsi(
        close=DF["Close"], window_slow=25, window_fast=13, fillna=False
    )
    DF["Ultimate_OSC"] = ta.momentum.ultimate_oscillator(
        close=DF["Close"],
        high=DF["High"],
        low=DF["Low"],
        window1=7,
        window2=14,
        window3=28,
        weight1=4.0,
        weight2=2.0,
        weight3=1.0,
        fillna=False,
    )
    DF["williams_r"] = ta.momentum.williams_r(
        close=DF["Close"], high=DF["High"], low=DF["Low"], lbp=14, fillna=False
    )
    DF["Acc/Dist_index"] = ta.volume.acc_dist_index(
        high=DF["High"],
        low=DF["Low"],
        close=DF["Close"],
        volume=DF["Volume"],
        fillna=False,
    )
    DF["CMF"] = ta.volume.chaikin_money_flow(
        high=DF["High"],
        low=DF["Low"],
        close=DF["Close"],
        volume=DF["Volume"],
        window=20,
        fillna=False,
    )
    DF["easeOfMovement"] = ta.volume.ease_of_movement(
        high=DF["High"], low=DF["Low"], volume=DF["Volume"], window=14, fillna=False
    )
    DF["sma_ease_of_movement"] = ta.volume.sma_ease_of_movement(
        high=DF["High"], low=DF["Low"], volume=DF["Volume"], window=14, fillna=False
    )
    DF["ForceIndexIndicator"] = ta.volume.force_index(
        close=DF["Close"], volume=DF["Volume"], window=14, fillna=False
    )
    DF["MFI"] = ta.volume.money_flow_index(
        high=DF["High"],
        low=DF["Low"],
        close=DF["Close"],
        volume=DF["Volume"],
        window=14,
        fillna=False,
    )
    DF["NegativeVolumeIndexIndicator"] = ta.volume.negative_volume_index(
        close=DF["Close"], volume=DF["Volume"], fillna=False
    )
    DF["OnBalanceVolumeIndicator"] = ta.volume.on_balance_volume(
        close=DF["Close"], volume=DF["Volume"], fillna=False
    )
    DF["VolumePriceTrendIndicator"] = ta.volume.volume_price_trend(
        close=DF["Close"], volume=DF["Volume"], fillna=False
    )
    DF["VolumeWeightedAveragePrice"] = ta.volume.volume_weighted_average_price(
        high=DF["High"],
        low=DF["Low"],
        close=DF["Close"],
        volume=DF["Volume"],
        window=14,
        fillna=False,
    )
    DF["AverageTrueRange"] = ta.volatility.average_true_range(
        high=DF["High"], low=DF["Low"], close=DF["Close"], window=14, fillna=False
    )
    DF["bollinger_hband"] = ta.volatility.bollinger_hband(
        close=DF["Close"], window=20, window_dev=2, fillna=False
    )
    DF["bollinger_hband_indicator"] = ta.volatility.bollinger_hband_indicator(
        close=DF["Close"], window=20, window_dev=2, fillna=False
    )
    DF["bollinger_lband"] = ta.volatility.bollinger_lband(
        close=DF["Close"], window=20, window_dev=2, fillna=False
    )
    DF["bollinger_lband_indicator"] = ta.volatility.bollinger_lband_indicator(
        close=DF["Close"], window=20, window_dev=2, fillna=False
    )
    DF["bollinger_mavg"] = ta.volatility.bollinger_mavg(
        close=DF["Close"], window=20, fillna=False
    )
    DF["bollinger_pband"] = ta.volatility.bollinger_pband(
        close=DF["Close"], window=20, window_dev=2, fillna=False
    )
    DF["bollinger_wband"] = ta.volatility.bollinger_wband(
        close=DF["Close"], window=20, window_dev=2, fillna=False
    )
    DF["donchian_channel_hband"] = ta.volatility.donchian_channel_hband(
        high=DF["High"],
        low=DF["Low"],
        close=DF["Close"],
        window=20,
        offset=0,
        fillna=False,
    )
    DF["donchian_channel_lband"] = ta.volatility.donchian_channel_lband(
        high=DF["High"],
        low=DF["Low"],
        close=DF["Close"],
        window=20,
        offset=0,
        fillna=False,
    )
    DF["donchian_channel_mband"] = ta.volatility.donchian_channel_mband(
        high=DF["High"],
        low=DF["Low"],
        close=DF["Close"],
        window=20,
        offset=0,
        fillna=False,
    )
    DF["donchian_channel_pband"] = ta.volatility.donchian_channel_pband(
        high=DF["High"],
        low=DF["Low"],
        close=DF["Close"],
        window=20,
        offset=0,
        fillna=False,
    )
    DF["donchian_channel_wband"] = ta.volatility.donchian_channel_wband(
        high=DF["High"],
        low=DF["Low"],
        close=DF["Close"],
        window=20,
        offset=0,
        fillna=False,
    )
    DF["keltner_channel_hband"] = ta.volatility.keltner_channel_hband(
        high=DF["High"],
        low=DF["Low"],
        close=DF["Close"],
        window=20,
        window_atr=10,
        original_version=True,
        fillna=False,
    )
    DF[
        "keltner_channel_hband_indicator"
    ] = ta.volatility.keltner_channel_hband_indicator(
        high=DF["High"],
        low=DF["Low"],
        close=DF["Close"],
        window=20,
        window_atr=10,
        original_version=True,
        fillna=False,
    )
    DF["keltner_channel_lband"] = ta.volatility.keltner_channel_lband(
        high=DF["High"],
        low=DF["Low"],
        close=DF["Close"],
        window=20,
        window_atr=10,
        original_version=True,
        fillna=False,
    )
    DF[
        "keltner_channel_lband_indicator"
    ] = ta.volatility.keltner_channel_lband_indicator(
        high=DF["High"],
        low=DF["Low"],
        close=DF["Close"],
        window=20,
        window_atr=10,
        original_version=True,
        fillna=False,
    )
    DF["keltner_channel_mband"] = ta.volatility.keltner_channel_mband(
        high=DF["High"],
        low=DF["Low"],
        close=DF["Close"],
        window=20,
        window_atr=10,
        original_version=True,
        fillna=False,
    )
    DF["keltner_channel_pband"] = ta.volatility.keltner_channel_pband(
        high=DF["High"],
        low=DF["Low"],
        close=DF["Close"],
        window=20,
        window_atr=10,
        original_version=True,
        fillna=False,
    )
    DF["keltner_channel_wband"] = ta.volatility.keltner_channel_wband(
        high=DF["High"],
        low=DF["Low"],
        close=DF["Close"],
        window=20,
        window_atr=10,
        original_version=True,
        fillna=False,
    )
    DF["ulcer_index"] = ta.volatility.ulcer_index(
        close=DF["Close"], window=14, fillna=False
    )
    DF["adx"] = ta.trend.adx(
        high=DF["High"], low=DF["Low"], close=DF["Close"], window=20, fillna=False
    )
    DF["adx_neg"] = ta.trend.adx_neg(
        high=DF["High"], low=DF["Low"], close=DF["Close"], window=20, fillna=False
    )
    DF["adx_pos"] = ta.trend.adx_pos(
        high=DF["High"], low=DF["Low"], close=DF["Close"], window=20, fillna=False
    )
    DF["aroon_down"] = ta.trend.aroon_down(DF["High"],DF['Low'], window=25, fillna=False)
    DF["aroon_up"] = ta.trend.aroon_up(DF["High"],DF['Low'], window=25, fillna=False)
    DF["cci"] = ta.trend.cci(
        high=DF["High"],
        low=DF["Low"],
        close=DF["Close"],
        window=20,
        constant=0.015,
        fillna=False,
    )
    DF["dpo"] = ta.trend.dpo(close=DF["Close"], window=20, fillna=False)
    DF["ema_indicator"] = ta.trend.ema_indicator(
        close=DF["Close"], window=14, fillna=False
    )
    DF["ichimoku_a"] = ta.trend.ichimoku_a(
        high=DF["High"], low=DF["Low"], window1=9, window2=26, fillna=False
    )
    DF["ichimoku_b"] = ta.trend.ichimoku_b(
        high=DF["High"], low=DF["Low"], window2=26, window3=52, fillna=False
    )
    DF["ichimoku_base_line"] = ta.trend.ichimoku_base_line(
        high=DF["High"], low=DF["Low"], window1=9, window2=26, fillna=False
    )
    DF["ichimoku_conversion_line"] = ta.trend.ichimoku_conversion_line(
        high=DF["High"], low=DF["Low"], window1=9, window2=26, fillna=False
    )
    DF["kst"] = ta.trend.kst(
        close=DF["Close"],
        roc1=10,
        roc2=15,
        roc3=20,
        roc4=30,
        window1=10,
        window2=10,
        window3=10,
        window4=15,
        fillna=False,
    )
    DF["kst_sig"] = ta.trend.kst_sig(
        close=DF["Close"],
        roc1=10,
        roc2=15,
        roc3=20,
        roc4=30,
        window1=10,
        window2=10,
        window3=10,
        window4=15,
        nsig=9,
        fillna=False,
    )
    DF["macd"] = ta.trend.macd(
        close=DF["Close"], window_slow=26, window_fast=12, fillna=False
    )
    DF["macd_diff"] = ta.trend.macd_diff(
        close=DF["Close"], window_sign=9, window_slow=26, window_fast=12, fillna=False
    )
    DF["macd_signal"] = ta.trend.macd_signal(
        close=DF["Close"], window_sign=9, window_slow=26, window_fast=12, fillna=False
    )
    DF["mass_index"] = ta.trend.mass_index(
        high=DF["High"], low=DF["Low"], window_fast=9, window_slow=25, fillna=False
    )
    DF["psar_down"] = ta.trend.psar_down(
        high=DF["High"],
        low=DF["Low"],
        close=DF["Close"],
        step=0.02,
        max_step=0.2,
        fillna=False,
    )
    DF["psar_down_indicator"] = ta.trend.psar_down_indicator(
        high=DF["High"],
        low=DF["Low"],
        close=DF["Close"],
        step=0.02,
        max_step=0.2,
        fillna=False,
    )
    DF["psar_up"] = ta.trend.psar_up(
        high=DF["High"],
        low=DF["Low"],
        close=DF["Close"],
        step=0.02,
        max_step=0.2,
        fillna=False,
    )
    DF["psar_up_indicator"] = ta.trend.psar_up_indicator(
        high=DF["High"],
        low=DF["Low"],
        close=DF["Close"],
        step=0.02,
        max_step=0.2,
        fillna=False,
    )
    DF["sma_indicator_5"] = ta.trend.sma_indicator(
        close=DF["Close"], window=5, fillna=False
    )
    DF["sma_indicator_12"] = ta.trend.sma_indicator(
        close=DF["Close"], window=12, fillna=False
    )
    DF["sma_indicator_26"] = ta.trend.sma_indicator(
        close=DF["Close"], window=26, fillna=False
    )
    DF["sma_indicator_52"] = ta.trend.sma_indicator(
        close=DF["Close"], window=52, fillna=False
    )
    DF["sma_indicator_150"] = ta.trend.sma_indicator(
        close=DF["Close"], window=150, fillna=False
    )
    DF["stc"] = ta.trend.stc(
        close=DF["Close"],
        window_slow=50,
        window_fast=23,
        cycle=10,
        smooth1=3,
        smooth2=3,
        fillna=False,
    )
    DF["trix"] = ta.trend.trix(close=DF["Close"], window=15, fillna=False)
    DF["vortex_indicator_neg"] = ta.trend.vortex_indicator_neg(
        high=DF["High"], low=DF["Low"], close=DF["Close"], window=14, fillna=False
    )
    DF["vortex_indicator_pos"] = ta.trend.vortex_indicator_pos(
        high=DF["High"], low=DF["Low"], close=DF["Close"], window=14, fillna=False
    )
    DF["wma"] = ta.trend.WMAIndicator(close=DF["Close"], window=9, fillna=False).wma()
    DF["cumulative_return"] = ta.others.cumulative_return(
        close=DF["Close"], fillna=False
    )
    DF["daily_log_return"] = ta.others.daily_log_return(close=DF["Close"], fillna=False)
    DF["daily_return"] = ta.others.daily_return(close=DF["Close"], fillna=False)
    return DF

def technial_indicators(DF):
    New_DF=indicators_calculation(DF)
    New_DF = New_DF.set_index(New_DF["CloseTime"], drop=True)
    New_DF=New_DF.drop(columns=['Opentime','CloseTime', 'Open', 'High', 'Low', 'Close', 'Volume',
       'QuoteAssetVolume', 'NumberOfTrades', 'TakerBuyBaseAssetVolume',
       'TakerBuyQuoteAssetVolume', 'Un'])

    return New_DF


