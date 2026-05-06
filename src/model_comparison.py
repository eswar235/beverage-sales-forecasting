"""Model comparison and evaluation module."""
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelComparator:
    """Compare and evaluate multiple forecasting models."""
    
    def __init__(self):
        self.results = {}
    
    def calculate_metrics(self, y_true, y_pred, model_name):
        """Calculate evaluation metrics."""
        mae = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
        r2 = r2_score(y_true, y_pred)
        
        metrics = {
            'model': model_name,
            'MAE': mae,
            'RMSE': rmse,
            'MAPE': mape,
            'R2': r2
        }
        
        self.results[model_name] = metrics
        
        logger.info(f"\n{model_name} Metrics:")
        logger.info(f"  MAE:  {mae:,.2f}")
        logger.info(f"  RMSE: {rmse:,.2f}")
        logger.info(f"  MAPE: {mape:.2f}%")
        logger.info(f"  R²:   {r2:.4f}")
        
        return metrics
    
    def get_comparison_table(self):
        """Get comparison table of all models."""
        if not self.results:
            return None
        
        df = pd.DataFrame(self.results).T
        df = df.sort_values('RMSE')
        
        return df
    
    def get_best_model(self, metric='RMSE'):
        """Get best model based on specified metric."""
        if not self.results:
            return None
        
        df = self.get_comparison_table()
        
        if metric in ['MAE', 'RMSE', 'MAPE']:
            best_model = df[metric].idxmin()
        else:  # R2
            best_model = df[metric].idxmax()
        
        logger.info(f"\nBest model based on {metric}: {best_model}")
        
        return best_model
    
    def save_results(self, filepath):
        """Save comparison results to CSV."""
        df = self.get_comparison_table()
        if df is not None:
            df.to_csv(filepath)
            logger.info(f"Results saved to {filepath}")
