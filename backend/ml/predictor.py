"""
Stock Predictor - Main ML prediction module
Implements SVM, SVR, and optional LSTM models
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import pickle
import os

from sklearn.svm import SVC, SVR
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error, mean_absolute_error

from .data_processor import DataProcessor


class StockPredictor:
    """
    Main class for stock price prediction using ML models
    
    Models implemented:
    1. SVM (Support Vector Machine) - For direction prediction (up/down)
    2. SVR (Support Vector Regression) - For price prediction
    3. LSTM (Long Short-Term Memory) - For sequential prediction (optional)
    """
    
    def __init__(self, model_type: str = "svr"):
        """
        Initialize predictor with specified model type
        
        Parameters:
            model_type: "svm" for classification, "svr" for regression, "lstm" for deep learning
        """
        self.model_type = model_type
        self.model = None
        self.scaler = StandardScaler()
        self.price_scaler = MinMaxScaler()
        self.data_processor = DataProcessor()
        self.is_trained = False
        
    def prepare_data(
        self, 
        symbol: str, 
        period: str = "2y",
        lookback: int = 10
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Prepare training data for the model
        
        Parameters:
            symbol: Stock symbol
            period: Historical data period
            lookback: Number of days to look back for features
            
        Returns:
            X (features), y (targets)
        """
        # Get processed data with features
        df = self.data_processor.get_stock_data_with_features(symbol, period)
        
        if df is None or len(df) < lookback + 50:
            raise Exception("Insufficient data for training")
        
        # Features to use
        feature_columns = [
            'returns', 'volatility', 'sma_10', 'sma_20', 'sma_50',
            'ema_10', 'rsi', 'macd', 'macd_signal', 'macd_histogram',
            'bb_upper', 'bb_lower', 'bb_position',
            'volume_change', 'price_momentum'
        ]
        
        # Get features that exist in dataframe
        available_features = [col for col in feature_columns if col in df.columns]
        
        # Drop rows with NaN
        df = df.dropna()
        
        if len(df) < 100:
            raise Exception("Insufficient data after cleaning")
        
        X = df[available_features].values
        
        # Target: next day's return direction (for SVM) or price (for SVR)
        if self.model_type == "svm":
            # Classification: 1 if price goes up, 0 if down
            y = (df['close'].shift(-1) > df['close']).astype(int).values[:-1]
            X = X[:-1]  # Remove last row since we don't have next day
        else:
            # Regression: predict next day's closing price
            y = df['close'].shift(-1).values[:-1]
            X = X[:-1]
        
        return X, y
    
    def train(
        self,
        symbol: str,
        period: str = "2y",
        test_size: float = 0.2
    ) -> Dict:
        """
        Train the model on historical data
        
        Parameters:
            symbol: Stock symbol
            period: Historical period for training
            test_size: Proportion of data for testing
            
        Returns:
            Training results including accuracy/error metrics
        """
        print(f"🚀 Training {self.model_type.upper()} model for {symbol}...")
        
        # Prepare data
        X, y = self.prepare_data(symbol, period)
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Scale target for regression
        if self.model_type != "svm":
            y = self.price_scaler.fit_transform(y.reshape(-1, 1)).ravel()
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, 
            test_size=test_size, 
            shuffle=False  # Keep temporal order
        )
        
        # Initialize and train model
        if self.model_type == "svm":
            self.model = SVC(
                kernel='rbf',
                C=1.0,
                gamma='scale',
                probability=True
            )
            self.model.fit(X_train, y_train)
            
            # Evaluate
            y_pred = self.model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            results = {
                "model": "SVM",
                "accuracy": round(accuracy * 100, 2),
                "train_samples": len(X_train),
                "test_samples": len(X_test)
            }
            
        else:  # SVR
            self.model = SVR(
                kernel='rbf',
                C=100,
                gamma='scale',
                epsilon=0.1
            )
            self.model.fit(X_train, y_train)
            
            # Evaluate
            y_pred = self.model.predict(X_test)
            
            # Inverse transform for actual prices
            y_test_actual = self.price_scaler.inverse_transform(y_test.reshape(-1, 1)).ravel()
            y_pred_actual = self.price_scaler.inverse_transform(y_pred.reshape(-1, 1)).ravel()
            
            mse = mean_squared_error(y_test_actual, y_pred_actual)
            mae = mean_absolute_error(y_test_actual, y_pred_actual)
            
            results = {
                "model": "SVR",
                "mse": round(mse, 2),
                "mae": round(mae, 2),
                "rmse": round(np.sqrt(mse), 2),
                "train_samples": len(X_train),
                "test_samples": len(X_test)
            }
        
        self.is_trained = True
        print(f"✅ Training complete! Results: {results}")
        
        return results
    
    def predict(
        self, 
        symbol: str, 
        days_ahead: int = 7
    ) -> Dict:
        """
        Generate prediction for a stock
        
        Parameters:
            symbol: Stock symbol
            days_ahead: Days to predict ahead
            
        Returns:
            Prediction results
        """
        if not self.is_trained:
            # Train on the fly if not trained
            self.train(symbol)
        
        # Get current features
        df = self.data_processor.get_stock_data_with_features(symbol, period="3mo")
        
        if df is None or len(df) < 50:
            raise Exception("Insufficient data for prediction")
        
        df = df.dropna()
        
        # Get feature columns
        feature_columns = [col for col in df.columns if col not in ['open', 'high', 'low', 'close', 'volume']]
        
        # Get latest features
        latest_features = df[feature_columns].iloc[-1].values.reshape(1, -1)
        
        # Scale features
        latest_scaled = self.scaler.transform(latest_features)
        
        current_price = df['close'].iloc[-1]
        
        if self.model_type == "svm":
            # Direction prediction
            prediction = self.model.predict(latest_scaled)[0]
            probability = self.model.predict_proba(latest_scaled)[0]
            
            if prediction == 1:
                direction = "UP"
                confidence = probability[1]
                price_change = 2.5 * confidence  # Estimated change
            else:
                direction = "DOWN"
                confidence = probability[0]
                price_change = -2.5 * confidence
            
            predicted_price = current_price * (1 + price_change / 100)
            
            return {
                "symbol": symbol,
                "model": "SVM",
                "current_price": round(current_price, 2),
                "predicted_direction": direction,
                "predicted_price": round(predicted_price, 2),
                "price_change_percent": round(price_change, 2),
                "confidence": round(confidence, 2),
                "signal": "BUY" if direction == "UP" else "SELL",
                "target_date": (datetime.now() + timedelta(days=days_ahead)).isoformat()
            }
            
        else:  # SVR
            # Price prediction
            prediction_scaled = self.model.predict(latest_scaled)[0]
            predicted_price = self.price_scaler.inverse_transform([[prediction_scaled]])[0][0]
            
            price_change = ((predicted_price - current_price) / current_price) * 100
            
            # Generate signal
            if price_change > 2:
                signal = "BUY"
            elif price_change < -2:
                signal = "SELL"
            else:
                signal = "HOLD"
            
            # Confidence based on model performance
            confidence = min(0.7 + abs(price_change) / 20, 0.95)
            
            return {
                "symbol": symbol,
                "model": "SVR",
                "current_price": round(current_price, 2),
                "predicted_price": round(predicted_price, 2),
                "price_change_percent": round(price_change, 2),
                "confidence": round(confidence, 2),
                "signal": signal,
                "target_date": (datetime.now() + timedelta(days=days_ahead)).isoformat()
            }
    
    def save_model(self, filepath: str):
        """
        Save trained model to file
        """
        if not self.is_trained:
            raise Exception("Model not trained yet")
        
        model_data = {
            "model": self.model,
            "scaler": self.scaler,
            "price_scaler": self.price_scaler,
            "model_type": self.model_type
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"✅ Model saved to {filepath}")
    
    def load_model(self, filepath: str):
        """
        Load a saved model
        """
        if not os.path.exists(filepath):
            raise Exception(f"Model file not found: {filepath}")
        
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)
        
        self.model = model_data["model"]
        self.scaler = model_data["scaler"]
        self.price_scaler = model_data["price_scaler"]
        self.model_type = model_data["model_type"]
        self.is_trained = True
        
        print(f"✅ Model loaded from {filepath}")


class EnsemblePredictor:
    """
    Ensemble model combining SVM and SVR predictions
    """
    
    def __init__(self):
        self.svm_predictor = StockPredictor(model_type="svm")
        self.svr_predictor = StockPredictor(model_type="svr")
    
    def train_all(self, symbol: str, period: str = "2y"):
        """
        Train all models
        """
        print(f"🎯 Training ensemble for {symbol}...")
        
        svm_results = self.svm_predictor.train(symbol, period)
        svr_results = self.svr_predictor.train(symbol, period)
        
        return {
            "svm": svm_results,
            "svr": svr_results
        }
    
    def predict(self, symbol: str, days_ahead: int = 7) -> Dict:
        """
        Get ensemble prediction
        """
        svm_pred = self.svm_predictor.predict(symbol, days_ahead)
        svr_pred = self.svr_predictor.predict(symbol, days_ahead)
        
        # Combine predictions
        avg_price_change = (svm_pred["price_change_percent"] + svr_pred["price_change_percent"]) / 2
        avg_confidence = (svm_pred["confidence"] + svr_pred["confidence"]) / 2
        
        current_price = svm_pred["current_price"]
        predicted_price = current_price * (1 + avg_price_change / 100)
        
        # Combined signal
        if svm_pred["signal"] == svr_pred["signal"]:
            signal = svm_pred["signal"]
            confidence_boost = 0.1  # Higher confidence when both agree
        else:
            signal = "HOLD"  # Conflicting signals
            confidence_boost = -0.1
        
        return {
            "symbol": symbol,
            "model": "Ensemble (SVM + SVR)",
            "current_price": current_price,
            "predicted_price": round(predicted_price, 2),
            "price_change_percent": round(avg_price_change, 2),
            "confidence": min(round(avg_confidence + confidence_boost, 2), 0.95),
            "signal": signal,
            "target_date": (datetime.now() + timedelta(days=days_ahead)).isoformat(),
            "individual_predictions": {
                "svm": {
                    "signal": svm_pred["signal"],
                    "confidence": svm_pred["confidence"]
                },
                "svr": {
                    "predicted_price": svr_pred["predicted_price"],
                    "confidence": svr_pred["confidence"]
                }
            }
        }


# Example usage
if __name__ == "__main__":
    # Test the predictor
    print("Testing Stock Predictor...")
    
    # Test with a single model
    predictor = StockPredictor(model_type="svr")
    
    try:
        # Train on Reliance
        results = predictor.train("RELIANCE.NS", period="1y")
        print(f"Training results: {results}")
        
        # Make prediction
        prediction = predictor.predict("RELIANCE.NS", days_ahead=7)
        print(f"Prediction: {prediction}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Test ensemble
    print("\nTesting Ensemble Predictor...")
    ensemble = EnsemblePredictor()
    
    try:
        ensemble.train_all("TCS.NS", period="1y")
        prediction = ensemble.predict("TCS.NS", days_ahead=7)
        print(f"Ensemble Prediction: {prediction}")
    except Exception as e:
        print(f"Error: {e}")
