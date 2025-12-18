import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Scouting Amateur", page_icon="⚽", layout="wide")

os.makedirs('data/amateur', exist_ok=True)

PLAYERS_FILE = 'data/amateur/players.csv'
MATCHES_FILE = 'data/amateur/match_stats.csv'

def init_files():
    if not os.path.exists(PLAYERS_FILE):
        pd.DataFrame(columns=['player_id', 'name', 'birth_date', 'position', 'team', 'league', 'height_cm', 'weight_kg', 'preferred_foot', 'nationality', 'contact', 'notes', 'created_date']).to_csv(PLAYERS_FILE, index=False)
    if not os.path.exists(MATCHES_FILE):
        pd.DataFrame(columns=['match_id', 'player_id', 'player_name', 'match_date', 'opponent', 'minutes_played', 'goals', 'assists', 'shots', 'shots_on_target', 'key_passes', 'successful_dribbles', 'tackles', 'interceptions', 'clearances', 'fouls_committed', 'fouls_received', 'yellow_cards', 'red_cards', 'rating_1_10', 'scout_notes', 'video_url']).to_csv(MATCHES_FILE, index=False)

init_files()

st.title("⚽ Sistema de Scouting - Ligas Amateur")
st.markdown("---")

st.sidebar.title("📋 Menú")
menu = st.sidebar.radio("Navegación:", ["🏠 Inicio", "➕ Registrar Jugador", "📊 Registrar Partido", "👥 Ver Jugadores", "📈 Estadísticas", "🎯 Rankings"])

if menu == "🏠 Inicio":
    col1, col2, col3 = st.columns(3)
    players_df = pd.read_csv(PLAYERS_FILE)
    matches_df = pd.read_csv(MATCHES_FILE)
    with col1:
        st.metric("👥 Jugadores", len(players_df))
    with col2:
        st.metric("⚽ Partidos", len(matches_df))
    with col3:
        total_goals = int(matches_df['goals'].sum()) if len(matches_df) > 0 else 0
        st.metric("🥅 Goles", total_goals)
    st.markdown("---")
    st.info("### Bienvenido\n\n**Comienza por:**\n1. Registrar jugadores\n2. Agregar estadísticas\n3. Ver análisis")

elif menu == "➕ Registrar Jugador":
    st.subheader("Registrar Nuevo Jugador")
    with st.form("player_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Nombre Completo *")
            birth_date = st.date_input("Fecha de Nacimiento *")
            position = st.selectbox("Posición *", ["Portero", "Defensa Central", "Lateral Derecho", "Lateral Izquierdo", "Mediocampista Defensivo", "Mediocampista Central", "Mediocampista Ofensivo", "Extremo Derecho", "Extremo Izquierdo", "Delantero Centro"])
            team = st.text_input("Equipo *")
            league = st.text_input("Liga *")
        with col2:
            height_cm = st.number_input("Altura (cm)", 150, 220, 175)
            weight_kg = st.number_input("Peso (kg)", 50, 120, 70)
            preferred_foot = st.selectbox("Pie Preferido", ["Derecho", "Izquierdo", "Ambidiestro"])
            nationality = st.text_input("Nacionalidad", value="Colombia")
            contact = st.text_input("Contacto")
        notes = st.text_area("Notas")
        submitted = st.form_submit_button("💾 Registrar")
        if submitted and name and team and league:
            players_df = pd.read_csv(PLAYERS_FILE)
            if len(players_df) == 0:
                player_id = 'P001'
            else:
                last_num = int(players_df['player_id'].iloc[-1][1:])
                player_id = f'P{last_num + 1:03d}'
            new_player = pd.DataFrame([{'player_id': player_id, 'name': name, 'birth_date': birth_date.strftime('%Y-%m-%d'), 'position': position, 'team': team, 'league': league, 'height_cm': height_cm, 'weight_kg': weight_kg, 'preferred_foot': preferred_foot, 'nationality': nationality, 'contact': contact, 'notes': notes, 'created_date': datetime.now().strftime('%Y-%m-%d')}])
            players_df = pd.concat([players_df, new_player], ignore_index=True)
            players_df.to_csv(PLAYERS_FILE, index=False)
            st.success(f"✅ Jugador registrado: {player_id}")
            st.balloons()

elif menu == "📊 Registrar Partido":
    st.subheader("Registrar Estadísticas de Partido")
    players_df = pd.read_csv(PLAYERS_FILE)
    if len(players_df) == 0:
        st.warning("⚠️ No hay jugadores registrados")
    else:
        with st.form("match_form"):
            player_options = {f"{row['name']} ({row['team']})": row['player_id'] for _, row in players_df.iterrows()}
            selected = st.selectbox("Jugador *", list(player_options.keys()))
            player_id = player_options[selected]
            player_name = selected.split(" (")[0]
            col1, col2, col3 = st.columns(3)
            with col1:
                match_date = st.date_input("Fecha *")
            with col2:
                opponent = st.text_input("Rival *")
            with col3:
                minutes = st.number_input("Minutos", 0, 120, 90)
            rating = st.slider("Rating (1-10)", 1, 10, 7)
            st.markdown("### Estadísticas")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                goals = st.number_input("Goles", 0, 10, 0)
                assists = st.number_input("Asistencias", 0, 10, 0)
            with col2:
                shots = st.number_input("Tiros", 0, 20, 0)
                shots_target = st.number_input("Al arco", 0, 20, 0)
            with col3:
                key_passes = st.number_input("Pases clave", 0, 20, 0)
                dribbles = st.number_input("Regates", 0, 20, 0)
            with col4:
                tackles = st.number_input("Tackles", 0, 20, 0)
                interceptions = st.number_input("Intercepciones", 0, 20, 0)
            notes = st.text_area("Observaciones")
            submitted = st.form_submit_button("💾 Guardar")
            if submitted and opponent:
                matches_df = pd.read_csv(MATCHES_FILE)
                if len(matches_df) == 0:
                    match_id = 'M001'
                else:
                    last_num = int(matches_df['match_id'].iloc[-1][1:])
                    match_id = f'M{last_num + 1:03d}'
                new_match = pd.DataFrame([{'match_id': match_id, 'player_id': player_id, 'player_name': player_name, 'match_date': match_date.strftime('%Y-%m-%d'), 'opponent': opponent, 'minutes_played': minutes, 'goals': goals, 'assists': assists, 'shots': shots, 'shots_on_target': shots_target, 'key_passes': key_passes, 'successful_dribbles': dribbles, 'tackles': tackles, 'interceptions': interceptions, 'clearances': 0, 'fouls_committed': 0, 'fouls_received': 0, 'yellow_cards': 0, 'red_cards': 0, 'rating_1_10': rating, 'scout_notes': notes, 'video_url': ''}])
                matches_df = pd.concat([matches_df, new_match], ignore_index=True)
                matches_df.to_csv(MATCHES_FILE, index=False)
                st.success(f"✅ Estadísticas guardadas: {match_id}")
                st.balloons()

elif menu == "👥 Ver Jugadores":
    st.subheader("Base de Datos de Jugadores")
    players_df = pd.read_csv(PLAYERS_FILE)
    if len(players_df) == 0:
        st.info("No hay jugadores registrados")
    else:
        st.dataframe(players_df[['player_id', 'name', 'position', 'team', 'league']], use_container_width=True)
        csv = players_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Exportar CSV", csv, "jugadores.csv", "text/csv")

elif menu == "📈 Estadísticas":
    st.subheader("Estadísticas Agregadas")
    matches_df = pd.read_csv(MATCHES_FILE)
    if len(matches_df) == 0:
        st.info("No hay estadísticas disponibles")
    else:
        numeric_cols = ['goals', 'assists', 'shots', 'rating_1_10', 'minutes_played']
        for col in numeric_cols:
            matches_df[col] = pd.to_numeric(matches_df[col], errors='coerce').fillna(0)
        stats = matches_df.groupby('player_id').agg({'match_date': 'count', 'goals': 'sum', 'assists': 'sum', 'shots': 'sum', 'minutes_played': 'sum', 'rating_1_10': 'mean'}).reset_index()
        stats.columns = ['player_id', 'partidos', 'goles', 'asistencias', 'tiros', 'minutos', 'rating_promedio']
        players_df = pd.read_csv(PLAYERS_FILE)
        stats = stats.merge(players_df[['player_id', 'name', 'team']], on='player_id')
        st.dataframe(stats[['name', 'team', 'partidos', 'goles', 'asistencias', 'rating_promedio']].round(2), use_container_width=True)
        csv = stats.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Exportar CSV", csv, "estadisticas.csv", "text/csv")

elif menu == "🎯 Rankings":
    st.subheader("Rankings")
    matches_df = pd.read_csv(MATCHES_FILE)
    if len(matches_df) == 0:
        st.info("No hay datos para rankings")
    else:
        numeric_cols = ['goals', 'assists', 'rating_1_10']
        for col in numeric_cols:
            matches_df[col] = pd.to_numeric(matches_df[col], errors='coerce').fillna(0)
        stats = matches_df.groupby('player_id').agg({'match_date': 'count', 'goals': 'sum', 'assists': 'sum', 'rating_1_10': 'mean'}).reset_index()
        stats.columns = ['player_id', 'partidos', 'goles', 'asistencias', 'rating']
        players_df = pd.read_csv(PLAYERS_FILE)
        stats = stats.merge(players_df[['player_id', 'name', 'team']], on='player_id')
        tab1, tab2, tab3 = st.tabs(["⚽ Goleadores", "🎯 Asistentes", "⭐ Rating"])
        with tab1:
            st.markdown("### Top 10 Goleadores")
            top_scorers = stats.nlargest(10, 'goles')
            st.dataframe(top_scorers[['name', 'team', 'goles', 'partidos']], use_container_width=True)
        with tab2:
            st.markdown("### Top 10 Asistentes")
            top_assists = stats.nlargest(10, 'asistencias')
            st.dataframe(top_assists[['name', 'team', 'asistencias', 'partidos']], use_container_width=True)
        with tab3:
            st.markdown("### Top 10 Mejor Rating")
            top_rated = stats.nlargest(10, 'rating')
            st.dataframe(top_rated[['name', 'team', 'rating', 'partidos']].round(2), use_container_width=True)

st.markdown("---")
st.markdown("⚽ **Sistema de Scouting Amateur**")