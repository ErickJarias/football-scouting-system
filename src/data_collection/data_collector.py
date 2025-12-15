import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
import re

class PlayerDataCollector:
    """
    Recolecta datos de jugadores desde fuentes públicas
    """
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.base_url = "https://fbref.com"
    
    def get_league_player_stats(self, league_url, stat_type='standard'):
        """
        Obtiene estadísticas de jugadores de una liga
        
        Args:
            league_url: URL de la liga en FBref
            stat_type: Tipo de estadísticas ('standard', 'shooting', 'passing', etc.)
        
        Returns:
            DataFrame con estadísticas de jugadores
        """
        try:
            print(f"Obteniendo datos de {league_url}...")
            response = requests.get(league_url, headers=self.headers)
            response.raise_for_status()
            
            # Parsear HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Buscar tabla de estadísticas
            table = soup.find('table', {'id': f'stats_{stat_type}'})
            
            if not table:
                print(f"No se encontró tabla de tipo {stat_type}")
                return None
            
            # Convertir a DataFrame
            df = pd.read_html(str(table))[0]
            
            # Limpiar columnas multi-nivel si existen
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = ['_'.join(col).strip() for col in df.columns.values]
            
            # Limpiar nombres de columnas
            df.columns = df.columns.str.replace(r'[^\w\s]', '', regex=True)
            
            print(f"✓ Datos obtenidos: {len(df)} jugadores")
            return df
            
        except Exception as e:
            print(f"Error al obtener datos: {e}")
            return None
    
    def clean_player_data(self, df):
        """
        Limpia y prepara los datos de jugadores
        """
        if df is None:
            return None
        
        # Eliminar filas duplicadas de encabezados
        df = df[df['Player'] != 'Player']
        
        # Convertir columnas numéricas
        numeric_columns = df.select_dtypes(include=['object']).columns
        for col in numeric_columns:
            if col not in ['Player', 'Nation', 'Pos', 'Squad', 'Born']:
                try:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                except:
                    pass
        
        # Eliminar filas con todos valores nulos
        df = df.dropna(how='all')
        
        return df
    
    def get_sample_data(self):
        """
        Obtiene datos de muestra de una liga popular
        (La Liga 2023-2024)
        """
        # URL de ejemplo - La Liga 2023-2024
        league_url = "https://fbref.com/en/comps/12/stats/La-Liga-Stats"
        
        df = self.get_league_player_stats(league_url)
        df = self.clean_player_data(df)
        
        # Esperar para no sobrecargar el servidor
        time.sleep(3)
        
        return df
    
    def save_data(self, df, filename):
        """
        Guarda los datos en formato CSV
        """
        if df is not None:
            df.to_csv(f'data/raw/{filename}', index=False)
            print(f"✓ Datos guardados en data/raw/{filename}")


# Ejemplo de uso
if __name__ == "__main__":
    collector = PlayerDataCollector()
    
    # Obtener datos de muestra
    print("Recolectando datos de jugadores...")
    player_data = collector.get_sample_data()
    
    if player_data is not None:
        print(f"\nColumnas disponibles:")
        print(player_data.columns.tolist())
        print(f"\nPrimeras filas:")
        print(player_data.head())
        
        # Guardar datos
        collector.save_data(player_data, 'players_stats.csv')