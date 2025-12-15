import pandas as pd
import json
from datetime import datetime
import os

class ScoutingReportGenerator:
    """
    Genera reportes profesionales de scouting
    """
    
    def __init__(self, df_scored):
        self.df = df_scored
        self.report_date = datetime.now().strftime("%Y-%m-%d")
    
    def generate_player_profile(self, player_name):
        """Genera perfil completo de un jugador"""
        player = self.df[self.df['Player'] == player_name]
        
        if len(player) == 0:
            return f"Jugador '{player_name}' no encontrado"
        
        player = player.iloc[0]
        
        profile = {
            'basic_info': {
                'name': player['Player'],
                'position': player['Pos'],
                'team': player['Squad'],
                'age': player.get('Age', 'N/A'),
            },
            'scores': {
                'overall_score': round(player.get('Overall_Score', 0), 2),
                'rank': int(player.get('Rank', 0)),
            }
        }
        
        return profile
    
    def generate_markdown_report(self, player_name, filename=None):
        """Genera reporte en formato Markdown"""
        profile = self.generate_player_profile(player_name)
        
        if isinstance(profile, str):
            return profile
        
        markdown = f"""# 📋 Reporte de Scouting

## 🎯 Perfil del Jugador

**Nombre:** {profile['basic_info']['name']}  
**Posición:** {profile['basic_info']['position']}  
**Equipo:** {profile['basic_info']['team']}  
**Edad:** {profile['basic_info']['age']}

---

## 📊 Evaluación

**Score General:** {profile['scores']['overall_score']}/100  
**Ranking General:** #{profile['scores']['rank']}

---

*Reporte generado el {self.report_date}*
"""
        
        if filename:
            os.makedirs('reports', exist_ok=True)
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(markdown)
            print(f"✓ Reporte guardado en {filename}")
        
        return markdown


# Ejemplo de uso
if __name__ == "__main__":
    try:
        df = pd.read_csv('data/processed/players_advanced_scored.csv')
        reporter = ScoutingReportGenerator(df)
        
        top_player = df.nlargest(1, 'Overall_Score').iloc[0]['Player']
        report_md = reporter.generate_markdown_report(
            top_player, 
            f'reports/player_{top_player.replace(" ", "_")}.md'
        )
        
        print("\n✅ Reportes generados exitosamente")
    except FileNotFoundError:
        print("❌ No se encontró data/processed/players_advanced_scored.csv")
        print("   Ejecuta primero: python src/analysis/advanced_scorer.py")