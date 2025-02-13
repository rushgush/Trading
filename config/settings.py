"""
Configuration settings for the trading bot.
Includes signal parameters, risk management settings, and trading rules.
"""
from typing import Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
API_CONFIG = {
    'QUIVER_API_KEY': os.getenv('AUTHORISATION_TOKEN'),
    'QUIVER_BASE_URL': 'https://api.quiverquant.com/beta',
}

# Signal Generation Parameters
SIGNAL_SETTINGS = {
    'STRONG_BUY': {
        'conditions': {
            'congress_buy': True,           # Must have recent congress purchase
            'wsb_sentiment_min': 0.6,       # Minimum WSB sentiment score
            'wsb_mentions_percentile': 75,  # Minimum percentile for mentions
            'insider_buying': True,         # Must have recent insider purchases
            'gov_contracts_min': 1000000    # Minimum govt contract value
        },
        'position_size': 0.10,             # 10% position size
        'stop_loss': 0.15,                 # 15% stop loss
        'take_profit': 0.30                # 30% take profit
    },
    
    'MOMENTUM_BUY': {
        'conditions': {
            'wsb_mentions_growth': 1.0,     # 100% growth in mentions
            'wsb_sentiment_min': 0.5,       # Minimum sentiment score
            'dark_pool_buying': True        # Must have institutional buying
        },
        'position_size': 0.075,            # 7.5% position size
        'stop_loss': 0.20,                 # 20% stop loss
        'take_profit': 0.40                # 40% take profit
    }
}

# Risk Management Settings
RISK_SETTINGS = {
    'max_position_size': 0.10,          # Maximum 10% per position
    'max_portfolio_risk': 0.40,         # Maximum 40% portfolio at risk
    'stop_loss': {
        'default': 0.15,                # 15% default stop loss
        'momentum_play': 0.20           # 20% for momentum trades
    },
    'take_profit': {
        'default': 0.30,                # 30% default take profit
        'momentum_play': 0.40           # 40% for momentum trades
    },
    'max_open_positions': 5,            # Maximum number of concurrent positions
    'min_liquidity': 1000000,           # Minimum daily trading volume
}

# Trading Schedule Settings
TRADING_SCHEDULE = {
    'market_open': '09:30',             # Market open time (EST)
    'market_close': '16:00',            # Market close time (EST)
    'signal_refresh_interval': 300,      # Refresh signals every 5 minutes
    'min_time_between_trades': 900      # Minimum 15 minutes between trades
}

# Data Collection Settings
DATA_SETTINGS = {
    'wsb_sentiment_window': 24,         # Hours to look back for WSB data
    'congress_trade_window': 7,         # Days to look back for Congress trades
    'insider_trade_window': 30,         # Days to look back for insider trades
    'min_wsb_mentions': 10,             # Minimum mentions to consider WSB signal
    'min_congress_trade_value': 50000   # Minimum Congress trade value to consider
}

# Backtesting Settings
BACKTEST_SETTINGS = {
    'initial_capital': 10000,           # Starting capital for backtests
    'commission_rate': 0.001,           # 0.1% commission per trade
    'slippage_rate': 0.001,            # 0.1% slippage assumption
    'test_start_date': '2023-01-01',   # Backtest start date
    'test_end_date': '2023-12-31'      # Backtest end date
}

def get_all_settings() -> Dict[str, Any]:
    """
    Returns all settings in a single dictionary.
    Useful for logging or debugging configuration.
    """
    return {
        'api_config': API_CONFIG,
        'signal_settings': SIGNAL_SETTINGS,
        'risk_settings': RISK_SETTINGS,
        'trading_schedule': TRADING_SCHEDULE,
        'data_settings': DATA_SETTINGS,
        'backtest_settings': BACKTEST_SETTINGS
    }

def validate_settings() -> bool:
    """
    Validates critical settings to ensure they're within acceptable ranges.
    Returns True if all validations pass, raises ValueError otherwise.
    """
    # Check position size limits
    if RISK_SETTINGS['max_position_size'] > 0.20:
        raise ValueError("Maximum position size cannot exceed 20%")
    
    # Check portfolio risk limits
    if RISK_SETTINGS['max_portfolio_risk'] > 0.50:
        raise ValueError("Maximum portfolio risk cannot exceed 50%")
    
    # Validate trading schedule times
    try:
        from datetime import datetime
        datetime.strptime(TRADING_SCHEDULE['market_open'], '%H:%M')
        datetime.strptime(TRADING_SCHEDULE['market_close'], '%H:%M')
    except ValueError:
        raise ValueError("Invalid trading schedule times")
    
    return True

# Validate settings on import
validate_settings()