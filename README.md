# Chavote-Project
Hand Tracking
# 🚀 Teclado Virtual ARNI-MODE v1.0

Teclado controlado por gestos del pulgar con diseño cyberpunk y predicción de palabras.

## 📦 Requisitos
- Python 3.11+
- Cámara web
- Windows/macOS/Linux

## 🛠 Instalación
```bash
git clone (https://github.com/arnimoreno/Chavote-Project/tree/main)
cd teclado-arni
pip install opencv-python mediapipe pygame nltk numpy
python -m nltk.downloader cess_esp

▶️ Uso
python main.py

🎮Controles:

Mueve el pulgar para navegar

Mantén 1.5s sobre tecla para seleccionar

2s sobre sugerencias para autocompletar

🎨 Personalización
Edita:

config.py → Colores y tamaños

KeyboardLogic.py → Diccionario de palabras

main.py → Tiempos de selección

🚨 Solución de problemas
Sin detección: Verifica iluminación

Ventana grande: Ajusta FRAME_WIDTH en config.py

Sin sonido: Reinstala pygame

📄 Licencia
MIT License © 2023 [Arni Moreno Geronimo]

📧 Contacto: arnimoreno21@gmail.com
🔗 GitHub: @arnimoreno
