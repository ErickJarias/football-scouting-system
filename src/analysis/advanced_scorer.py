import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

class AdvancedPlayerScorer:
    """
    Sistema avanzado de scoring con Machine Learning
    """
    
    def __init__(self):
        # Pesos mejorados con más granularidad
        self.position_weights = {
            'FW': {
                'goals': 0.28,
                'assists': 0.18,
                'shots': 0.12,
                'shot_on_target': 0.12,
                'key_passes': 0.10,
                'dribbles_successful': 0.08,
                'aerial_duels_won': 0.06,
                'offsides': -0.06
            },
            'MF': {
                'assists': 0.22,
                'key_passes': 0.18,
                'pass_accuracy': 0.15,
                'progressive_passes': 0.12,
                'tackles': 0.12,
                'interceptions': 0.10,
                'goals': 0.11
            },
            'DF': {
                'tackles': 0.22,
                'interceptions': 0.22,
                'clearances': 0.18,
                'blocks': 0.13,
                'aerial_duels_won': 0.13,
                'errors_leading_to_shot': -0.12
            },
            'GK': {
                'saves': 0.28,
                'clean_sheets': 0.22,
                'save_percentage': 0.22,
                'goals_against': -0.15,
                'distribution_accuracy': 0.13
            }
        }
        
        self.scaler = MinMaxScaler(feature_range=(0, 100))
    
    def identify_position(self, pos_string):
        """Identificación mejorada de posición"""
        if pd.isna(pos_string):
            return 'Unknown'
        
        pos_string = str(pos_string).upper()
        
        if 'GK' in pos_string:
            return 'GK'
        
        forward_keywords = ['FW', 'CF', 'ST', 'LW', 'RW', 'SS']
        if any(kw in pos_string for kw in forward_keywords):
            return 'FW'
        
        defense_keywords = ['DF', 'CB', 'LB', 'RB', 'WB', 'SW']
        if any(kw in pos_string for kw in defense_keywords):
            return 'DF'
        
        midfield_keywords = ['MF', 'CM', 'DM', 'AM', 'LM', 'RM', 'CDM', 'CAM']
        if any(kw in pos_string for kw in midfield_keywords):
            return 'MF'
        
        return 'Unknown'
    
    def calculate_per_90_stats(self, df):
        """Calcula estadísticas por 90 minutos jugados"""
        df_per90 = df.copy()
        
        minutes_col = None
        for col in ['Min', 'Minutes', '90s', 'MP']:
            if col in df.columns:
                minutes_col = col
                break
        
        if minutes_col:
            df_per90['Minutes_Played'] = pd.to_numeric(df[minutes_col], errors='coerce')
            df_per90['90s_Played'] = df_per90['Minutes_Played'] / 90
            
            numeric_cols = df_per90.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                if col not in ['Age', 'Minutes_Played', '90s_Played', 'Born']:
                    try:
                        df_per90[f'{col}_per90'] = (
                            df_per90[col] / df_per90['90s_Played']
                        ).replace([np.inf, -np.inf], 0)
                    except:
                        pass
        
        return df_per90
    
    def normalize_stats(self, df, columns):
        """Normalización mejorada"""
        df_normalized = df.copy()
        
        for col in columns:
            if col in df.columns:
                values = df[col].fillna(0).values.reshape(-1, 1)
                mean = np.mean(values)
                std = np.std(values)
                values_clipped = np.clip(values, mean - 3*std, mean + 3*std)
                
                if values_clipped.max() > values_clipped.min():
                    df_normalized[f'{col}_normalized'] = self.scaler.fit_transform(values_clipped)
                else:
                    df_normalized[f'{col}_normalized'] = 50
        
        return df_normalized
    
    def calculate_position_score(self, row, position):
        """Cálculo mejorado con penalizaciones"""
        if position not in self.position_weights or position == 'Unknown':
            return 0
        
        weights = self.position_weights[position]
        score = 0
        total_weight = 0
        
        for metric, weight in weights.items():
            metric_col = f'{metric}_normalized'
            
            if metric_col in row.index:
                score += row[metric_col] * weight
                total_weight += abs(weight)
        
        if total_weight > 0:
            score = ((score / total_weight) * 100) + 50
            score = np.clip(score, 0, 100)
        
        return score
    
    def score_players(self, df):
        """Pipeline completo de scoring"""
        print("🔄 Iniciando análisis avanzado...")
        
        df['Position_Category'] = df['Pos'].apply(self.identify_position)
        print(f"✓ Posiciones identificadas")
        
        df = self.calculate_per_90_stats(df)
        print(f"✓ Estadísticas normalizadas por tiempo")
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        df = self.normalize_stats(df, numeric_cols)
        print(f"✓ Normalización completada")
        
        df['Overall_Score'] = df.apply(
            lambda row: self.calculate_position_score(row, row['Position_Category']),
            axis=1
        )
        print(f"✓ Scores calculados")
        
        df['Rank'] = df['Overall_Score'].rank(ascending=False, method='min')
        
        print(f"\n✅ Análisis completado: {len(df)} jugadores procesados")
        
        return df


# Ejemplo de uso
if __name__ == "__main__":
    try:
        df = pd.read_csv('data/raw/players_stats.csv')
        scorer = AdvancedPlayerScorer()
        df_scored = scorer.score_players(df)
        
        print("\n" + "="*70)
        print("📊 RESULTADOS DEL ANÁLISIS AVANZADO")
        print("="*70)
        
        print("\n🏆 TOP 10 GENERAL:")
        top_10 = df_scored.nlargest(10, 'Overall_Score')
        print(top_10[['Player', 'Pos', 'Squad', 'Overall_Score', 'Rank']])
        
        df_scored.to_csv('data/processed/players_advanced_scored.csv', index=False)
        print("\n✓ Resultados guardados en data/processed/players_advanced_scored.csv")
    except FileNotFoundError:
        print("❌ No se encontró data/raw/players_stats.csv")
        print("   Ejecuta primero: python src/data_collection/data_collector.py")