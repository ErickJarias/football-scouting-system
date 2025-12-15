import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

class PlayerScorer:
    """
    Sistema de puntuación para jugadores según posición
    """
    
    def __init__(self):
        # Pesos por posición (ajustables)
        self.position_weights = {
            'FW': {  # Delanteros
                'goals': 0.30,
                'assists': 0.20,
                'shots': 0.15,
                'shot_accuracy': 0.15,
                'key_passes': 0.10,
                'dribbles': 0.10
            },
            'MF': {  # Mediocampistas
                'assists': 0.25,
                'key_passes': 0.20,
                'pass_accuracy': 0.15,
                'tackles': 0.15,
                'interceptions': 0.10,
                'goals': 0.15
            },
            'DF': {  # Defensas
                'tackles': 0.25,
                'interceptions': 0.25,
                'clearances': 0.20,
                'blocks': 0.15,
                'aerial_duels': 0.15
            },
            'GK': {  # Porteros
                'saves': 0.30,
                'clean_sheets': 0.25,
                'save_percentage': 0.25,
                'distribution': 0.20
            }
        }
    
    def normalize_stats(self, df, columns):
        """
        Normaliza estadísticas entre 0 y 100
        """
        scaler = MinMaxScaler(feature_range=(0, 100))
        df_normalized = df.copy()
        
        for col in columns:
            if col in df.columns:
                # Manejar valores nulos
                df_normalized[col] = df[col].fillna(0)
                # Normalizar
                values = df_normalized[col].values.reshape(-1, 1)
                df_normalized[f'{col}_normalized'] = scaler.fit_transform(values)
        
        return df_normalized
    
    def identify_position(self, pos_string):
        """
        Identifica la posición principal del jugador
        """
        if pd.isna(pos_string):
            return 'Unknown'
        
        pos_string = str(pos_string).upper()
        
        if 'GK' in pos_string:
            return 'GK'
        elif any(x in pos_string for x in ['FW', 'CF', 'ST', 'LW', 'RW']):
            return 'FW'
        elif any(x in pos_string for x in ['MF', 'CM', 'DM', 'AM', 'LM', 'RM']):
            return 'MF'
        elif any(x in pos_string for x in ['DF', 'CB', 'LB', 'RB', 'WB']):
            return 'DF'
        else:
            return 'Unknown'
    
    def calculate_position_score(self, row, position):
        """
        Calcula el score para una posición específica
        """
        if position not in self.position_weights or position == 'Unknown':
            return 0
        
        weights = self.position_weights[position]
        score = 0
        total_weight = 0
        
        for metric, weight in weights.items():
            metric_col = f'{metric}_normalized'
            
            # Buscar columna normalizada
            if metric_col in row.index:
                score += row[metric_col] * weight
                total_weight += weight
        
        # Normalizar por el peso total usado
        if total_weight > 0:
            score = (score / total_weight)
        
        return score
    
    def score_players(self, df):
        """
        Calcula scores para todos los jugadores
        """
        # Identificar posiciones
        df['Position_Category'] = df['Pos'].apply(self.identify_position)
        
        # Identificar columnas numéricas para normalizar
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        # Normalizar estadísticas
        df_scored = self.normalize_stats(df, numeric_cols)
        
        # Calcular score por posición
        df_scored['Overall_Score'] = df_scored.apply(
            lambda row: self.calculate_position_score(row, row['Position_Category']),
            axis=1
        )
        
        # Ranking
        df_scored['Rank'] = df_scored['Overall_Score'].rank(ascending=False, method='min')
        
        return df_scored
    
    def get_top_players(self, df_scored, position=None, top_n=10):
        """
        Obtiene los mejores jugadores
        """
        if position:
            df_filtered = df_scored[df_scored['Position_Category'] == position]
        else:
            df_filtered = df_scored
        
        return df_filtered.nlargest(top_n, 'Overall_Score')


# Ejemplo de uso
if __name__ == "__main__":
    # Cargar datos
    try:
        df = pd.read_csv('data/raw/players_stats.csv')
        
        # Crear scorer
        scorer = PlayerScorer()
        
        # Calcular scores
        print("Calculando scores de jugadores...")
        df_scored = scorer.score_players(df)
        
        # Top 10 general
        print("\n=== TOP 10 JUGADORES GENERAL ===")
        top_players = scorer.get_top_players(df_scored, top_n=10)
        print(top_players[['Player', 'Pos', 'Squad', 'Overall_Score', 'Rank']])
        
        # Guardar resultados
        df_scored.to_csv('data/processed/players_scored.csv', index=False)
        print("\n✓ Resultados guardados en data/processed/players_scored.csv")
    except FileNotFoundError:
        print("❌ No se encontró data/raw/players_stats.csv")
        print("   Ejecuta primero: python src/data_collection/data_collector.py")