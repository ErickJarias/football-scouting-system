"""
Script de configuración inicial del proyecto
"""
import os
import sys

def create_directory_structure():
    """
    Crea la estructura de directorios del proyecto
    """
    directories = [
        'data/raw',
        'data/processed',
        'data/amateur',
        'src/data_collection',
        'src/analysis',
        'src/scoring',
        'src/visualization',
        'notebooks',
        'reports',
        'templates',
        'video_analysis'
    ]
    
    print("📁 Creando estructura de directorios...")
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"  ✓ {directory}")
    
    # Crear archivos __init__.py
    init_dirs = ['src', 'src/data_collection', 'src/analysis', 'src/scoring', 'src/visualization']
    for directory in init_dirs:
        init_file = os.path.join(directory, '__init__.py')
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write('# Package initialization\n')
    
    print("\n✓ Estructura de directorios creada exitosamente")

def create_readme():
    """
    Crea el archivo README.md
    """
    readme_content = """# ⚽ Sistema de Scouting Automatizado

Sistema de análisis y scouting de jugadores de fútbol basado en datos estadísticos.

## 🚀 Inicio Rápido

### 1. Instalación
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\\Scripts\\activate
# En Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Sistema Amateur
```bash
streamlit run amateur_data_entry.py
```

### 3. Análisis de Video
```bash
python video_analyzer.py
```

### 4. Generar Plantillas Excel
```bash
python excel_template_generator.py
```

## 📊 Características

- ✅ Sistema de entrada de datos para ligas amateur
- ✅ Análisis de video semi-automático
- ✅ Plantillas Excel para recolección offline
- ✅ Dashboard interactivo
- ✅ Generación de reportes profesionales

## 🛠️ Tecnologías

- Python 3.8+
- Pandas & NumPy
- Streamlit
- OpenCV
- Plotly
- Scikit-learn

## 📧 Contacto

Desarrollado con ❤️ para el análisis de fútbol amateur
"""
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("\n✓ README.md creado")

def create_gitignore():
    """
    Crea el archivo .gitignore
    """
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Data
data/raw/*.csv
data/processed/*.csv
data/amateur/*.csv
*.xlsx
*.mp4
*.avi
*.mov

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Streamlit
.streamlit/

# Jupyter
.ipynb_checkpoints/

# Logs
*.log
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)
    
    print("✓ .gitignore creado")

def main():
    """
    Ejecuta la configuración completa
    """
    print("=" * 60)
    print("⚽ CONFIGURACIÓN DEL SISTEMA DE SCOUTING AUTOMATIZADO")
    print("=" * 60)
    print()
    
    # Crear estructura
    create_directory_structure()
    
    # Crear archivos de documentación
    create_readme()
    create_gitignore()
    
    print("\n" + "=" * 60)
    print("✅ CONFIGURACIÓN COMPLETADA")
    print("=" * 60)
    print("\n📋 Próximos pasos:")
    print("1. Instalar dependencias: pip install -r requirements.txt")
    print("2. Sistema amateur: streamlit run amateur_data_entry.py")
    print("3. Generar plantillas: python excel_template_generator.py")
    print("\n🎉 ¡Listo para comenzar!")

if __name__ == "__main__":
    main()