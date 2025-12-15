import streamlit as st
import pandas as pd
from datetime import datetime
import os

class AmateurPlayerDatabase:
    """Sistema de gestión de datos para jugadores de ligas amateur"""
    
    def __init__(self, db_path='data/amateur/'):
        self.db_path = db_path
        self.players_file = os.path.join(db_path, 'players.csv')
        self.matches_file = os.path.join(db_path, 'match_stats.csv')
        os.makedirs(db_path, exist_ok=True)
        self._initialize_database()
    
    def _initialize_database(self):
        """Crea archivos CSV iniciales"""
        if not os.path.exists(self.players_file):
            players_df = pd.DataFrame(columns=[
                'player_id', 'name', 'birth_date', 'position', 'team',
                'league', 'height_cm', 'weight_kg', 'preferred_foot',
                'nationality', 'contact', 'notes', 'created_date'
            ])
            players_df.to_csv(self.players_file, index=False)
        
        if not os.path.exists(self.matches_file):
            matches_df = pd.DataFrame(columns=[
                'match_id', 'player_id', 'player_name', 'match_date', 'opponent',
                'minutes_played', 'goals', 'assists', 'shots', 'shots_on_target',
                'key_passes', 'successful_dribbles', 'attempted_dribbles',
                'tackles', 'interceptions', 'clearances', 'fouls_committed',
                'fouls_received', 'yellow_cards', 'red_cards', 'rating_1_10',
                'scout_notes', 'video_url'
            ])
            matches_df.to_csv(self.matches_file, index=False)
    
    def add_player(self, player_data):
        """Agrega un nuevo jugador"""
        df = pd.read_csv(self.players_file)
        if len(df) == 0:
            player_id = 'P001'
        else:
            last_id = df['player_id'].max()
            num = int(last_id[1:]) + 1
            player_id = f'P{num:03d}'
        
        player_data['player_id'] = player_id
        player_data['created_date'] = datetime.now().strftime('%Y-%m-%d')
        df = pd.concat([df, pd.DataFrame([player_data])], ignore_index=True)
        df.to_csv(self.players_file, index=False)
        return player_id
    
    def add_match_stats(self, match_data):
        """Agrega estadísticas de un partido"""
        df = pd.read_csv(self.matches_file)
        if len(df) == 0:
            match_id = 'M001'
        else:
            last_id = df['match_id'].max()
            num = int(last_id[1:]) + 1
            match_id = f'M{num:03d}'
        
        match_data