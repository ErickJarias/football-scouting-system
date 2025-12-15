"""
Generador de plantillas Excel para recolección offline de datos
Útil cuando no hay internet disponible en el estadio
"""

import pandas as pd
from datetime import datetime
import os

class ExcelTemplateGenerator:
    """
    Crea plantillas Excel para entrada de datos offline
    """
    
    def __init__(self, output_dir='templates/'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def create_players_template(self):
        """
        Plantilla para registrar nuevos jugadores
        """
        # Estructura básica
        template_data = {
            'Nombre_Completo': ['', '', ''],
            'Fecha_Nacimiento': ['YYYY-MM-DD', '', ''],
            'Posicion': ['Ej: Delantero Centro', '', ''],
            'Equipo': ['', '', ''],
            'Liga': ['', '', ''],
            'Altura_cm': ['175', '', ''],
            'Peso_kg': ['70', '', ''],
            'Pie_Preferido': ['Derecho/Izquierdo/Ambidiestro', '', ''],
            'Nacionalidad': ['Colombia', '', ''],
            'Telefono': ['+57 300 123 4567', '', ''],
            'Email': ['', '', ''],
            'Notas': ['', '', '']
        }
        
        df = pd.DataFrame(template_data)
        
        filename = os.path.join(self.output_dir, 'plantilla_jugadores.xlsx')
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Jugadores', index=False)
            
            # Instrucciones
            instructions = pd.DataFrame({
                'INSTRUCCIONES': [
                    '1. Completa una fila por cada jugador',
                    '2. NO modifiques los nombres de las columnas',
                    '3. Respeta los formatos indicados en la primera fila',
                    '4. Fecha en formato: YYYY-MM-DD (Ej: 2000-05-15)',
                    '5. Pie Preferido: Escribe exactamente "Derecho", "Izquierdo" o "Ambidiestro"',
                    '6. Guarda el archivo cuando termines',
                    '7. Importa usando el sistema amateur_data_entry.py',
                    '',
                    'CAMPOS OBLIGATORIOS:',
                    '- Nombre_Completo',
                    '- Fecha_Nacimiento',
                    '- Posicion',
                    '- Equipo',
                    '- Liga',
                ]
            })
            instructions.to_excel(writer, sheet_name='Instrucciones', index=False)
        
        print(f"✓ Plantilla de jugadores creada: {filename}")
        return filename
    
    def create_match_stats_template(self):
        """
        Plantilla para estadísticas de partido
        """
        template_data = {
            'Nombre_Jugador': ['Juan Pérez', '', ''],
            'Fecha_Partido': ['2024-05-15', '', ''],
            'Rival': ['CD Cúcuta', '', ''],
            'Minutos_Jugados': [90, '', ''],
            'Goles': [1, '', ''],
            'Asistencias': [0, '', ''],
            'Tiros': [5, '', ''],
            'Tiros_al_Arco': [3, '', ''],
            'Pases_Clave': [4, '', ''],
            'Regates_Exitosos': [6, '', ''],
            'Tackles': [2, '', ''],
            'Intercepciones': [3, '', ''],
            'Despejes': [0, '', ''],
            'Faltas_Cometidas': [1, '', ''],
            'Faltas_Recibidas': [2, '', ''],
            'Amarillas': [0, '', ''],
            'Rojas': [0, '', ''],
            'Rating_1_10': [8, '', ''],
            'Observaciones': ['Excelente partido, dominó el mediocampo', '', ''],
            'URL_Video': ['', '', '']
        }
        
        df = pd.DataFrame(template_data)
        
        filename = os.path.join(self.output_dir, 'plantilla_partidos.xlsx')
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Estadisticas', index=False)
            
            # Instrucciones
            instructions = pd.DataFrame({
                'INSTRUCCIONES': [
                    '1. Una fila = un jugador en un partido',
                    '2. Si varios jugadores jugaron el mismo partido, crea una fila para cada uno',
                    '3. Fecha formato: YYYY-MM-DD',
                    '4. Minutos: entre 0 y 120',
                    '5. Rating: número del 1 al 10',
                    '6. Las tarjetas rojas y amarillas son números (0, 1, 2...)',
                    '7. Guarda cuando termines',
                    '',
                    'CAMPOS OBLIGATORIOS:',
                    '- Nombre_Jugador (debe existir en el sistema)',
                    '- Fecha_Partido',
                    '- Rival',
                    '- Minutos_Jugados',
                    '',
                    'TIPS:',
                    '- Si no observaste una estadística, deja en 0',
                    '- Sé lo más preciso posible con los números',
                    '- Las observaciones son muy valiosas para el análisis cualitativo'
                ]
            })
            instructions.to_excel(writer, sheet_name='Instrucciones', index=False)
        
        print(f"✓ Plantilla de partidos creada: {filename}")
        return filename
    
    def create_quick_notes_template(self):
        """
        Plantilla para notas rápidas durante el partido
        """
        template_data = {
            'Timestamp': ['0:00', '15:30', '45:00', '60:00', '90:00'],
            'Jugador': ['', '', '', '', ''],
            'Accion': ['Ej: Gol de cabeza', '', '', '', ''],
            'Calidad': ['Excelente/Buena/Regular/Mala', '', '', '', ''],
            'Notas': ['', '', '', '', '']
        }
        
        df = pd.DataFrame(template_data)
        
        filename = os.path.join(self.output_dir, 'plantilla_notas_rapidas.xlsx')
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Notas', index=False)
            
            instructions = pd.DataFrame({
                'USO': [
                    'Plantilla para tomar notas DURANTE el partido',
                    '',
                    'FORMATO:',
                    '- Timestamp: Minuto del partido (Ej: 23:45 = minuto 23)',
                    '- Jugador: Nombre del jugador observado',
                    '- Accion: Qué hizo (gol, asistencia, error, etc.)',
                    '- Calidad: Tu evaluación de la acción',
                    '- Notas: Contexto adicional',
                    '',
                    'EJEMPLOS:',
                    '12:30 | Juan Pérez | Gol de tiro libre | Excelente | Curva perfecta',
                    '35:00 | Carlos López | Pase clave | Buena | Habilito al delantero',
                    '67:15 | Luis Mora | Tackle | Excelente | Recuperó cerca del área',
                    '',
                    'Después del partido, usa estas notas para completar',
                    'la plantilla de estadísticas completas'
                ]
            })
            instructions.to_excel(writer, sheet_name='Instrucciones', index=False)
        
        print(f"✓ Plantilla de notas rápidas creada: {filename}")
        return filename
    
    def create_evaluation_template(self):
        """
        Plantilla de evaluación cualitativa detallada
        """
        template_data = {
            'Criterio': [
                'TÉCNICA - Control de balón',
                'TÉCNICA - Pase corto',
                'TÉCNICA - Pase largo',
                'TÉCNICA - Disparo',
                'TÉCNICA - Regate',
                'TÉCNICA - Cabezazo',
                'FÍSICO - Velocidad',
                'FÍSICO - Resistencia',
                'FÍSICO - Fuerza',
                'FÍSICO - Salto',
                'TÁCTICO - Posicionamiento',
                'TÁCTICO - Visión de juego',
                'TÁCTICO - Marca',
                'TÁCTICO - Coberturas',
                'MENTAL - Concentración',
                'MENTAL - Decisiones bajo presión',
                'MENTAL - Liderazgo',
                'MENTAL - Actitud',
            ],
            'Rating_1_10': ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            'Observaciones': ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
        }
        
        df = pd.DataFrame(template_data)
        
        filename = os.path.join(self.output_dir, 'plantilla_evaluacion_detallada.xlsx')
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Evaluacion', index=False)
            
            # Header con datos del jugador
            header = pd.DataFrame({
                'Campo': ['Jugador', 'Fecha', 'Partido', 'Posición', 'Evaluador'],
                'Valor': ['', '', '', '', '']
            })
            header.to_excel(writer, sheet_name='Datos', index=False)
            
            instructions = pd.DataFrame({
                'SISTEMA DE CALIFICACIÓN': [
                    '10 - Élite mundial',
                    '9 - Sobresaliente',
                    '8 - Muy bueno',
                    '7 - Bueno',
                    '6 - Por encima del promedio',
                    '5 - Promedio',
                    '4 - Por debajo del promedio',
                    '3 - Deficiente',
                    '2 - Muy deficiente',
                    '1 - Extremadamente deficiente',
                    '',
                    'TIPS:',
                    '- Sé honesto y objetivo',
                    '- Compara con jugadores del mismo nivel (no profesionales)',
                    '- Considera el potencial de mejora',
                    '- Las observaciones son tan importantes como los números'
                ]
            })
            instructions.to_excel(writer, sheet_name='Instrucciones', index=False)
        
        print(f"✓ Plantilla de evaluación creada: {filename}")
        return filename
    
    def create_all_templates(self):
        """
        Crea todas las plantillas de una vez
        """
        print("="*60)
        print("📝 GENERANDO PLANTILLAS EXCEL")
        print("="*60)
        print()
        
        templates = []
        
        templates.append(self.create_players_template())
        templates.append(self.create_match_stats_template())
        templates.append(self.create_quick_notes_template())
        templates.append(self.create_evaluation_template())
        
        print()
        print("="*60)
        print("✅ PLANTILLAS GENERADAS EXITOSAMENTE")
        print("="*60)
        print(f"\n📁 Ubicación: {self.output_dir}")
        print("\n📋 Archivos creados:")
        for i, template in enumerate(templates, 1):
            print(f"  {i}. {os.path.basename(template)}")
        
        print("\n💡 PRÓXIMOS PASOS:")
        print("1. Abre las plantillas en Excel/Google Sheets")
        print("2. Lee las instrucciones en cada archivo")
        print("3. Completa los datos")
        print("4. Importa los datos al sistema usando amateur_data_entry.py")
        
        return templates


def import_from_excel(players_file=None, matches_file=None):
    """
    Función helper para importar datos desde Excel al sistema
    """
    try:
        from amateur_data_entry import AmateurPlayerDatabase
    except ImportError:
        print("❌ Error: No se encuentra amateur_data_entry.py")
        print("   Asegúrate de tener todos los archivos del sistema")
        return
    
    db = AmateurPlayerDatabase()
    
    print("="*60)
    print("📥 IMPORTANDO DATOS DESDE EXCEL")
    print("="*60)
    
    # Importar jugadores
    if players_file and os.path.exists(players_file):
        print(f"\n📊 Importando jugadores desde: {players_file}")
        df_players = pd.read_excel(players_file, sheet_name='Jugadores')
        
        # Filtrar filas vacías
        df_players = df_players[df_players['Nombre_Completo'].notna()]
        
        imported = 0
        for _, row in df_players.iterrows():
            try:
                player_data = {
                    'name': row['Nombre_Completo'],
                    'birth_date': str(row['Fecha_Nacimiento']),
                    'position': row['Posicion'],
                    'team': row['Equipo'],
                    'league': row['Liga'],
                    'height_cm': row.get('Altura_cm', 175),
                    'weight_kg': row.get('Peso_kg', 70),
                    'preferred_foot': row.get('Pie_Preferido', 'Derecho'),
                    'nationality': row.get('Nacionalidad', 'Colombia'),
                    'contact': str(row.get('Telefono', '')) + ' ' + str(row.get('Email', '')),
                    'notes': row.get('Notas', '')
                }
                
                player_id = db.add_player(player_data)
                imported += 1
                print(f"  ✓ {player_data['name']} → {player_id}")
            except Exception as e:
                print(f"  ✗ Error con {row.get('Nombre_Completo', 'jugador')}: {e}")
        
        print(f"\n✅ Jugadores importados: {imported}")
    
    # Importar estadísticas de partidos
    if matches_file and os.path.exists(matches_file):
        print(f"\n📊 Importando partidos desde: {matches_file}")
        df_matches = pd.read_excel(matches_file, sheet_name='Estadisticas')
        
        # Filtrar filas vacías
        df_matches = df_matches[df_matches['Nombre_Jugador'].notna()]
        
        # Obtener jugadores para mapeo
        players_df = db.get_players()
        player_map = {row['name']: row['player_id'] 
                     for _, row in players_df.iterrows()}
        
        imported = 0
        for _, row in df_matches.iterrows():
            try:
                player_name = row['Nombre_Jugador']
                
                if player_name not in player_map:
                    print(f"  ⚠️ Jugador no encontrado: {player_name}")
                    continue
                
                match_data = {
                    'player_id': player_map[player_name],
                    'player_name': player_name,
                    'match_date': str(row['Fecha_Partido']),
                    'opponent': row['Rival'],
                    'minutes_played': int(row.get('Minutos_Jugados', 0)),
                    'goals': int(row.get('Goles', 0)),
                    'assists': int(row.get('Asistencias', 0)),
                    'shots': int(row.get('Tiros', 0)),
                    'shots_on_target': int(row.get('Tiros_al_Arco', 0)),
                    'key_passes': int(row.get('Pases_Clave', 0)),
                    'successful_dribbles': int(row.get('Regates_Exitosos', 0)),
                    'attempted_dribbles': int(row.get('Regates_Exitosos', 0)),
                    'tackles': int(row.get('Tackles', 0)),
                    'interceptions': int(row.get('Intercepciones', 0)),
                    'clearances': int(row.get('Despejes', 0)),
                    'fouls_committed': int(row.get('Faltas_Cometidas', 0)),
                    'fouls_received': int(row.get('Faltas_Recibidas', 0)),
                    'yellow_cards': int(row.get('Amarillas', 0)),
                    'red_cards': int(row.get('Rojas', 0)),
                    'rating_1_10': float(row.get('Rating_1_10', 5)),
                    'scout_notes': str(row.get('Observaciones', '')),
                    'video_url': str(row.get('URL_Video', ''))
                }
                
                match_id = db.add_match_stats(match_data)
                imported += 1
                print(f"  ✓ {player_name} vs {match_data['opponent']} → {match_id}")
            except Exception as e:
                print(f"  ✗ Error: {e}")
        
        print(f"\n✅ Partidos importados: {imported}")
    
    print("\n" + "="*60)
    print("✅ IMPORTACIÓN COMPLETADA")
    print("="*60)


if __name__ == "__main__":
    # Generar todas las plantillas
    generator = ExcelTemplateGenerator()
    generator.create_all_templates()
    
    print("\n" + "="*60)
    print("📖 GUÍA DE USO")
    print("="*60)
    print("""
FLUJO DE TRABAJO OFFLINE:

1. ANTES DEL PARTIDO:
   • Imprime o lleva plantilla_notas_rapidas.xlsx
   • Ten lápiz/papel como backup

2. DURANTE EL PARTIDO:
   • Toma notas rápidas con timestamps
   • Marca acciones destacadas

3. DESPUÉS DEL PARTIDO:
   • Transcribe notas a plantilla_partidos.xlsx
   • Completa estadísticas mientras están frescas

4. IMPORTAR AL SISTEMA:
   • Ejecuta: python excel_template_generator.py
   • Usa la función import_from_excel()
   • O importa manualmente en amateur_data_entry.py

TIPS:
- Las plantillas tienen ejemplos y validaciones
- Lee las instrucciones en cada hoja
- Guarda copias de backup
- No modifiques nombres de columnas
    """)