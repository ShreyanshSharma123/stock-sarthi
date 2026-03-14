"""
Data Processor - Data preprocessing and feature engineering for ML
"""

import numpy as np
import pandas as pd
import yfinance as yf
from typing import Optional, List
from datetime import datetime


class DataProcessor:
    """
    Handles data fetching, cleaning, and feature engineering for stock data
    """
    
    def __init__(self):
        self.cache = {}
        
    def get_stock_data(self, symbol: str, period: str = "1y") -> Optional[pd.DataFrame]:
        """
        Fetch raw stock data from Yahoo Finance
        
        Parameters:
            symbol: Stock symbol (e.g., "RELIANCE.NS")
            period: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y)
            
        Returns:
            DataFrame with OHLCV data
        """
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period)
            
            if df.empty:
                return None
            
            # Standardize column names
            df.columns = [col.lower() for col in df.columns]
            
            # Reset index to have date as column
            df.reset_index(inplace=True)
            df.rename(columns={'index': 'date'}, inplace=True)
            
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'])
                df.set_index('date', inplace=True)
            
            return df
            
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None
    
    def get_stock_data_with_features(
        self, 
        symbol: str, 
        period: str = "1y"
    ) -> Optional[pd.DataFrame]:
        """
        Get stock data with calculated technical features
        
        This is the main method used for ML training
        """
        df = self.get_stock_data(symbol, period)
        
        if df is None or len(df) < 50:
            return None
        
        # Calculate all features
        df = self.add_technical_features(df)
        
        return df
    
    def add_technical_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add technical indicators as features
        
        Features added:
        - Returns and volatility
        - Moving averages (SMA, EMA)
        - RSI
        - MACD
        - Bollinger Bands
        - Volume features
        - Price momentum
        """
        # Make a copy
        df = df.copy()
        
        # =============
        # Price Features
        # =============
        
        # Daily returns
        df['returns'] = df['close'].pct_change()
        
        # Volatility (rolling standard deviation of returns)
        df['volatility'] = df['returns'].rolling(window=10).std()
        
        # Price momentum (rate of price change)
        df['price_momentum'] = df['close'].pct_change(periods=5)
        
        # =============
        # Moving Averages
        # =============
        
        # Simple Moving Averages
        df['sma_5'] = df['close'].rolling(window=5).mean()
        df['sma_10'] = df['close'].rolling(window=10).mean()
        df['sma_20'] = df['close'].rolling(window=20).mean()
        df['sma_50'] = df['close'].rolling(window=50).mean()
        
        # Exponential Moving Averages
        df['ema_10'] = df['close'].ewm(span=10, adjust=False).mean()
        df['ema_20'] = df['close'].ewm(span=20, adjust=False).mean()
        
        # Moving average ratios (trend indicators)
        df['sma_ratio_5_20'] = df['sma_5'] / df['sma_20']
        df['sma_ratio_10_50'] = df['sma_10'] / df['sma_50']
        
        # =============
        # RSI (Relative Strength Index)
        # =============
        df['rsi'] = self._calculate_rsi(df['close'])
        
        # RSI zones
        df['rsi_oversold'] = (df['rsi'] < 30).astype(int)
        df['rsi_overbought'] = (df['rsi'] > 70).astype(int)
        
        # =============
        # MACD
        # =============
        macd_data = self._calculate_macd(df['close'])
        df['macd'] = macd_data['macd']
        df['macd_signal'] = macd_data['signal']
        df['macd_histogram'] = macd_data['histogram']
        
        # MACD crossover signals
        df['macd_crossover'] = (df['macd'] > df['macd_signal']).astype(int)
        
        # =============
        # Bollinger Bands
        # =============
        bb_data = self._calculate_bollinger_bands(df['close'])
        df['bb_upper'] = bb_data['upper']
        df['bb_lower'] = bb_data['lower']
        df['bb_middle'] = bb_data['middle']
        df['bb_width'] = (df['bb_upper'] - df['bb_lower']) / df['bb_middle']
        
        # Position within bands (-1 to 1)
        df['bb_position'] = (df['close'] - df['bb_lower']) / (df['bb_upper'] - df['bb_lower']) * 2 - 1
        
        # =============
        # Volume Features
        # =============
        
        # Volume change
        df['volume_change'] = df['volume'].pct_change()
        
        # Volume moving average
        df['volume_sma_10'] = df['volume'].rolling(window=10).mean()
        
        # Volume ratio (relative volume)
        df['volume_ratio'] = df['volume'] / df['volume_sma_10']
        
        # =============
        # High/Low Features
        # =============
        
        # Daily range
        df['daily_range'] = (df['high'] - df['low']) / df['close']
        
        # Distance from high/low
        df['distance_from_high'] = (df['high'] - df['close']) / df['high']
        df['distance_from_low'] = (df['close'] - df['low']) / df['low']
        
        # =============
        # Lag Features
        # =============
        
        # Price lags
        for lag in [1, 2, 3, 5]:
            df[f'close_lag_{lag}'] = df['close'].shift(lag)
            df[f'returns_lag_{lag}'] = df['returns'].shift(lag)
        
        # =============
        # Target Variable
        # =============
        
        # Next day return (for prediction)
        df['next_day_return'] = df['close'].shift(-1) / df['close'] - 1
        
        # Binary target: 1 if price goes up, 0 otherwise
        df['target_direction'] = (df['next_day_return'] > 0).astype(int)
        
        return df
    
    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """
        Calculate RSI (Relative Strength Index)
        
        RSI = 100 - (100 / (1 + RS))
        RS = Average Gain / Average Loss
        """
        delta = prices.diff()
        
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        
        avg_gain = gain.rolling(window=period, min_periods=1).mean()
        avg_loss = loss.rolling(window=period, min_periods=1).mean()
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def _calculate_macd(
        self, 
        prices: pd.Series,
        fast_period: int = 12,
        slow_period: int = 26,
        signal_period: int = 9
    ) -> dict:
        """
        Calculate MACD (Moving Average Convergence Divergence)
        
        MACD Line = EMA(12) - EMA(26)
        Signal Line = EMA(9) of MACD Line
        Histogram = MACD Line - Signal Line
        """
        ema_fast = prices.ewm(span=fast_period, adjust=False).mean()
        ema_slow = prices.ewm(span=slow_period, adjust=False).mean()
        
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
        histogram = macd_line - signal_line
        
        return {
            'macd': macd_line,
            'signal': signal_line,
            'histogram': histogram
        }
    
    def _calculate_bollinger_bands(
        self, 
        prices: pd.Series,
        period: int = 20,
        num_std: float = 2.0
    ) -> dict:
        """
        Calculate Bollinger Bands
        
        Middle Band = SMA(20)
        Upper Band = Middle Band + (2 * Standard Deviation)
        Lower Band = Middle Band - (2 * Standard Deviation)
        """
        sma = prices.rolling(window=period).mean()
        std = prices.rolling(window=period).std()
        
        return {
            'upper': sma + (std * num_std),
            'middle': sma,
            'lower': sma - (std * num_std)
        }
    
    def normalize_features(
        self, 
        df: pd.DataFrame, 
        method: str = 'standard'
    ) -> pd.DataFrame:
        """
        Normalize numerical features
        
        Parameters:
            df: DataFrame with features
            method: 'standard' (z-score) or 'minmax' (0-1 scaling)
        """
        df = df.copy()
        
        # Features to normalize (exclude binary and target)
        exclude_cols = ['target_direction', 'rsi_oversold', 'rsi_overbought', 'macd_crossover']
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        cols_to_normalize = [col for col in numeric_cols if col not in exclude_cols]
        
        if method == 'standard':
            # Z-score normalization
            for col in cols_to_normalize:
                mean = df[col].mean()
                std = df[col].std()
                if std > 0:
                    df[col] = (df[col] - mean) / std
        else:
            # Min-Max normalization
            for col in cols_to_normalize:
                min_val = df[col].min()
                max_val = df[col].max()
                if max_val > min_val:
                    df[col] = (df[col] - min_val) / (max_val - min_val)
        
        return df
    
    def handle_missing_values(
        self, 
        df: pd.DataFrame, 
        strategy: str = 'drop'
    ) -> pd.DataFrame:
        """
        Handle missing values in the dataset
        
        Parameters:
            df: DataFrame
            strategy: 'drop' to remove rows, 'fill' to fill with appropriate values
        """
        if strategy == 'drop':
            return df.dropna()
        else:
            # Forward fill for time series data
            df = df.fillna(method='ffill')
            # Backward fill for any remaining NaN at the beginning
            df = df.fillna(method='bfill')
            return df
    
    def create_sequences(
        self, 
        df: pd.DataFrame, 
        sequence_length: int = 10,
        target_col: str = 'close'
    ) -> tuple:
        """
        Create sequences for LSTM model
        
        Returns X (sequences) and y (targets)
        """
        data = df[target_col].values
        
        X, y = [], []
        
        for i in range(len(data) - sequence_length):
            X.append(data[i:i + sequence_length])
            y.append(data[i + sequence_length])
        
        return np.array(X), np.array(y)


# Example usage
if __name__ == "__main__":
    processor = DataProcessor()
    
    # Test with Reliance
    print("Testing data processor with RELIANCE.NS...")
    
    df = processor.get_stock_data_with_features("RELIANCE.NS", "6mo")
    
    if df is not None:
        print(f"Data shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print(f"\nSample data:")
        print(df[['close', 'returns', 'sma_10', 'rsi', 'macd']].tail())
    else:
        print("Failed to fetch data")
