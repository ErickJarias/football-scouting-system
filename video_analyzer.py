"""
Sistema básico de análisis de video para jugadores amateur
Requiere: opencv-python, numpy
Instalar: pip install opencv-python numpy
"""

import cv2
import numpy as np
from datetime import timedelta
import os

class VideoAnalyzer:
    """
    Analizador básico de videos de fútbol para jugadores amateur
    """
    
    def __init__(self, video_path):
        self.video_path = video_path
        self.cap = None
        self.fps = 0
        self.total_frames = 0
        self.duration = 0
        
    def load_video(self):
        """Carga el video y obtiene información básica"""
        self.cap = cv2.VideoCapture(self.video_path)
        
        if not self.cap.isOpened():
            raise Exception(f"No se pudo abrir el video: {self.video_path}")
        
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.duration = self.total_frames / self.fps
        
        print(f"✓ Video cargado:")
        print(f"  - FPS: {self.fps}")
        print(f"  - Total frames: {self.total_frames}")
        print(f"  - Duración: {timedelta(seconds=int(self.duration))}")
        
        return True
    
    def extract_frames(self, output_dir, interval_seconds=5):
        """
        Extrae frames del video cada X segundos
        Útil para análisis manual posterior
        """
        if not self.cap:
            self.load_video()
        
        os.makedirs(output_dir, exist_ok=True)
        
        frame_interval = int(self.fps * interval_seconds)
        frame_count = 0
        saved_count = 0
        
        print(f"\n📸 Extrayendo frames cada {interval_seconds} segundos...")
        
        while True:
            ret, frame = self.cap.read()
            
            if not ret:
                break
            
            if frame_count % frame_interval == 0:
                timestamp = frame_count / self.fps
                filename = f"frame_{saved_count:04d}_t{int(timestamp)}s.jpg"
                filepath = os.path.join(output_dir, filename)
                
                cv2.imwrite(filepath, frame)
                saved_count += 1
                
                if saved_count % 10 == 0:
                    print(f"  Extraídos {saved_count} frames...")
            
            frame_count += 1
        
        print(f"✓ Extracción completada: {saved_count} frames guardados en {output_dir}")
        
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reset video
        return saved_count
    
    def detect_motion(self, threshold=25):
        """
        Detecta momentos de alta actividad en el video
        Útil para identificar jugadas importantes
        """
        if not self.cap:
            self.load_video()
        
        print("\n🎬 Detectando momentos de alta actividad...")
        
        ret, prev_frame = self.cap.read()
        if not ret:
            return []
        
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        prev_gray = cv2.GaussianBlur(prev_gray, (21, 21), 0)
        
        high_activity_moments = []
        frame_count = 1
        
        while True:
            ret, frame = self.cap.read()
            
            if not ret:
                break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)
            
            # Calcular diferencia entre frames
            frame_diff = cv2.absdiff(prev_gray, gray)
            thresh = cv2.threshold(frame_diff, threshold, 255, cv2.THRESH_BINARY)[1]
            
            # Calcular porcentaje de movimiento
            motion_percent = (np.sum(thresh) / 255) / thresh.size * 100
            
            # Si hay mucho movimiento (>5%), es un momento importante
            if motion_percent > 5:
                timestamp = frame_count / self.fps
                high_activity_moments.append({
                    'timestamp': timestamp,
                    'frame': frame_count,
                    'motion_intensity': motion_percent
                })
            
            prev_gray = gray
            frame_count += 1
            
            if frame_count % 500 == 0:
                print(f"  Procesados {frame_count}/{self.total_frames} frames...")
        
        print(f"✓ Detectados {len(high_activity_moments)} momentos de alta actividad")
        
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reset video
        return high_activity_moments
    
    def create_highlights(self, activity_moments, output_path, 
                         seconds_before=3, seconds_after=3):
        """
        Crea un video de highlights con los momentos más activos
        """
        if not activity_moments:
            print("No hay momentos de actividad para crear highlights")
            return False
        
        print(f"\n✂️ Creando video de highlights...")
        
        # Ordenar por intensidad y tomar top 10
        top_moments = sorted(activity_moments, 
                           key=lambda x: x['motion_intensity'], 
                           reverse=True)[:10]
        
        # Configurar video de salida
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, self.fps, 
                             (int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                              int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
        
        for i, moment in enumerate(top_moments):
            timestamp = moment['timestamp']
            start_frame = max(0, int((timestamp - seconds_before) * self.fps))
            end_frame = min(self.total_frames, 
                          int((timestamp + seconds_after) * self.fps))
            
            # Posicionar video en el frame inicial
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
            
            # Extraer clip
            for _ in range(end_frame - start_frame):
                ret, frame = self.cap.read()
                if ret:
                    # Agregar texto con el timestamp
                    cv2.putText(frame, f"Momento {i+1} - {timedelta(seconds=int(timestamp))}", 
                              (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    out.write(frame)
            
            print(f"  Agregado momento {i+1}/{len(top_moments)}")
        
        out.release()
        print(f"✓ Video de highlights creado: {output_path}")
        
        return True
    
    def generate_report(self, output_file='video_analysis_report.txt'):
        """
        Genera un reporte básico del análisis
        """
        report = f"""
╔════════════════════════════════════════════════════════════╗
║           REPORTE DE ANÁLISIS DE VIDEO                     ║
╚════════════════════════════════════════════════════════════╝

📹 INFORMACIÓN DEL VIDEO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Archivo: {os.path.basename(self.video_path)}
Duración: {timedelta(seconds=int(self.duration))}
FPS: {self.fps}
Total de frames: {self.total_frames}

📊 INSTRUCCIONES DE USO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Revisa los frames extraídos para identificar jugadas clave
2. Usa el video de highlights para análisis rápido
3. Registra manualmente las estadísticas observadas en el sistema

💡 MÉTRICAS RECOMENDADAS PARA OBSERVAR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Ofensivas:
  - Goles y asistencias
  - Tiros (dentro y fuera del área)
  - Regates exitosos
  - Pases clave
  - Posicionamiento sin balón

Defensivas:
  - Tackles
  - Intercepciones
  - Despejes
  - Duelos aéreos ganados

Físicas:
  - Sprints de alta intensidad
  - Distancia recorrida aproximada
  - Recuperación entre esfuerzos

🎯 RECOMENDACIONES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Graba los partidos desde una posición elevada para mejor visión
- Mantén la cámara estable (usar trípode si es posible)
- Asegúrate de capturar todo el campo de juego
- Registra las estadísticas inmediatamente después del análisis

"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✓ Reporte guardado en: {output_file}")
        return report
    
    def close(self):
        """Libera recursos"""
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()


def analyze_match_video(video_path, player_name, output_dir='video_analysis'):
    """
    Función principal para analizar un video de partido
    """
    print("="*60)
    print(f"🎥 ANÁLISIS DE VIDEO - {player_name}")
    print("="*60)
    
    # Crear directorios
    player_dir = os.path.join(output_dir, player_name.replace(" ", "_"))
    frames_dir = os.path.join(player_dir, 'frames')
    
    os.makedirs(player_dir, exist_ok=True)
    
    # Inicializar analizador
    analyzer = VideoAnalyzer(video_path)
    analyzer.load_video()
    
    # 1. Extraer frames clave
    print("\n" + "="*60)
    analyzer.extract_frames(frames_dir, interval_seconds=10)
    
    # 2. Detectar momentos de alta actividad
    print("\n" + "="*60)
    activity_moments = analyzer.detect_motion(threshold=25)
    
    # 3. Crear video de highlights
    print("\n" + "="*60)
    highlights_path = os.path.join(player_dir, f'{player_name}_highlights.mp4')
    analyzer.create_highlights(activity_moments, highlights_path)
    
    # 4. Generar reporte
    print("\n" + "="*60)
    report_path = os.path.join(player_dir, 'analysis_report.txt')
    analyzer.generate_report(report_path)
    
    # Cerrar
    analyzer.close()
    
    print("\n" + "="*60)
    print("✅ ANÁLISIS COMPLETADO")
    print("="*60)
    print(f"\n📁 Resultados guardados en: {player_dir}")
    print(f"  - Frames extraídos: {frames_dir}")
    print(f"  - Video highlights: {highlights_path}")
    print(f"  - Reporte: {report_path}")
    
    return {
        'frames_dir': frames_dir,
        'highlights_path': highlights_path,
        'report_path': report_path,
        'activity_moments': len(activity_moments)
    }


# Ejemplo de uso
if __name__ == "__main__":
    # Configuración
    VIDEO_PATH = "partido_ejemplo.mp4"  # Cambiar por tu video
    PLAYER_NAME = "Juan Perez"
    
    print("""
╔════════════════════════════════════════════════════════════╗
║     SISTEMA DE ANÁLISIS DE VIDEO PARA SCOUTING            ║
║              Ligas Amateur / Departamentales              ║
╚════════════════════════════════════════════════════════════╝

INSTRUCCIONES:
1. Coloca tu video de partido en la carpeta del proyecto
2. Actualiza la variable VIDEO_PATH con el nombre del archivo
3. Ejecuta este script: python video_analyzer.py

NOTA: Este análisis es semi-automático. Aún necesitarás:
  - Revisar los frames extraídos manualmente
  - Contar las estadísticas observadas
  - Registrarlas en el sistema amateur_data_entry.py
""")
    
    # Verificar si existe el video
    if not os.path.exists(VIDEO_PATH):
        print(f"\n❌ ERROR: No se encontró el video: {VIDEO_PATH}")
        print("\nColoca tu video en la carpeta del proyecto y actualiza VIDEO_PATH")
    else:
        # Analizar video
        results = analyze_match_video(VIDEO_PATH, PLAYER_NAME)
        
        print("\n💡 SIGUIENTES PASOS:")
        print("1. Revisa los frames extraídos para identificar jugadas")
        print("2. Mira el video de highlights para análisis rápido")
        print("3. Registra las estadísticas en el sistema de entrada de datos")
        print("\nEjecuta: streamlit run amateur_data_entry.py")