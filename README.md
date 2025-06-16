
Un innovador simulador de toma de decisiones estratégicas que utiliza Inteligencia Artificial (IA) para ayudarte a mejorar tu lógica de negocio y resolución de problemas. Enfréntate a escenarios complejos, toma decisiones críticas y recibe retroalimentación instantánea y diagnósticos basados en modelos predictivos.

Demo: https://simulador-decisiones-ia.streamlit.app/

# 🚀 Simulador de Decisiones Estratégicas con IA: Tu Entrenador Personal Inteligente

## 🤔 ¿Qué es este proyecto?

El **Simulador de Decisiones Estratégicas con IA** es una herramienta interactiva diseñada para potenciar tus **habilidades de toma de decisiones** y tu **pensamiento estratégico**. Imagina tener un consultor de IA a tu lado que te presenta **escenarios de negocio complejos** o situaciones personales, te permite tomar decisiones y, al instante, **simula los resultados**, **diagnostica las implicaciones** y te ofrece **retroalimentación inteligente** sobre la lógica empleada.

Este proyecto es perfecto para:
* **Profesionales** que buscan afinar sus **habilidades de liderazgo** y **toma de decisiones gerenciales**.
* **Estudiantes** interesados en aplicar conceptos de **estrategia empresarial** y **resolución de problemas**.
* Cualquier persona que quiera desarrollar su **inteligencia analítica** y mejorar su **lógica de decisión**.

## ✨ Características Principales

* **Simulación de Escenarios Reales:** Enfrenta diversos desafíos (negocios, inversiones, gestión de crisis) que requieren pensamiento estratégico.
* **Inteligencia Artificial Predictiva:** Un modelo de **Machine Learning (Scikit-learn)** predice las consecuencias de tus decisiones basándose en datos históricos.
* **Diagnóstico y Feedback Inteligente:** Recibe un análisis detallado sobre el porqué de los resultados y sugerencias para mejorar tu lógica.
* **Dashboard de Rendimiento (BI):** Visualiza tu progreso a lo largo del tiempo con **gráficos interactivos (Plotly)** que muestran tus fortalezas y áreas de mejora en la toma de decisiones.
* **Persistencia de Datos (SQLite):** Todas tus decisiones y los resultados de la IA se guardan de forma segura para un seguimiento continuo.
* **Interfaz Intuitiva (Streamlit):** Una aplicación web fácil de usar, desarrollada en Python, que te permite interactuar con el simulador sin problemas.

## 🛠️ Tecnologías Utilizadas

* **Python**: El lenguaje de programación principal.
* **Streamlit**: Para construir la interfaz de usuario interactiva y responsiva.
* **Pandas**: Para la manipulación y análisis de datos.
* **Scikit-learn**: Implementación de algoritmos de Machine Learning (Árboles de Decisión para clasificación y regresión) para la IA predictiva.
* **SQLite**: Base de datos ligera para almacenar el historial de decisiones de los usuarios.
* **Plotly Express**: Para la visualización de datos y los dashboards interactivos.

## 🚀 Cómo Empezar

Sigue estos pasos para poner en marcha el simulador en tu máquina local:

1.  **Clona este repositorio:**
    ```bash
    git clone https://github.com/santiagourdaneta/Simulador-de-Decisiones-Estrategicas-con-IA-Tu-Entrenador-Personal-Inteligente/
    cd Simulador-de-Decisiones-Estrategicas-con-IA-Tu-Entrenador-Personal-Inteligente
    ```

2.  **Crea un entorno virtual (recomendado):**
    ```bash
    python -m venv venv
    # En Windows:
    .\venv\Scripts\activate
    # En macOS/Linux:
    source venv/bin/activate
    ```

3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```
    (Nota: Debes crear un archivo `requirements.txt` con `pip freeze > requirements.txt` después de instalar todas las librerías mencionadas.)

4.  **Asegúrate de tener los datos de entrenamiento:**
    El archivo `datos_entrenamiento.csv` debe estar en la raíz del proyecto. Este archivo es crucial para que la IA aprenda. Puedes modificarlo o expandirlo para incluir más escenarios.

5.  **Ejecuta la aplicación Streamlit:**
    ```bash
    streamlit run app.py
    ```

    Se abrirá automáticamente una nueva pestaña en tu navegador con la interfaz del simulador.

## 📊 Estructura de Datos (`datos_entrenamiento.csv`)

El archivo CSV de entrenamiento es el corazón de la IA. Cada fila representa una lección para el modelo. Asegúrate de que las columnas tengan el siguiente formato:

| Columna                      | Descripción                                                                 | Tipo de Datos |
| :--------------------------- | :-------------------------------------------------------------------------- | :------------ |
| `escenario`                  | Nombre del escenario (ej. "Tienda de Helados", "Lanzamiento de Producto") | Texto         |
| `decision`                   | La decisión tomada en ese escenario                                         | Texto         |
| `ganancia_estimada`          | Puntuación de ganancia (0-100)                                              | Entero        |
| `clientes_felices_estimados` | Puntuación de satisfacción del cliente (0-100)                              | Entero        |
| `dificultad_ejecucion`       | Nivel de dificultad para implementar la decisión (1-5)                      | Entero        |
| `logica_ejemplo`             | Breve descripción de la lógica detrás de esa decisión (para referencia)     | Texto         |
| `resultado_final`            | Resultado general de la decisión (ej. "Éxito moderado", "Fracaso parcial") | Texto         |
| `feedback_ia_ejemplo`        | Retroalimentación explicativa y diagnóstica de la IA para este caso        | Texto         |
| `descripcion_escenario`      | Descripción detallada del escenario para la UI                             | Texto         |
| `descripcion_decision`       | (Opcional) Descripción detallada de la decisión para la UI                  | Texto         |

## 🤝 Contribuciones

¡Tu ayuda es bienvenida! Si tienes ideas para nuevos escenarios, mejoras en la IA, o sugerencias para la interfaz de usuario, no dudes en:

1.  Hacer un "Fork" del repositorio.
2.  Crear una nueva rama (`git checkout -b feature/nueva-mejora`).
3.  Realizar tus cambios y hacer "commit" (`git commit -m 'feat: Añadir nuevo escenario de crisis'`).
4.  Hacer "push" a tu rama (`git push origin feature/nueva-mejora`).
5.  Abrir un "Pull Request".

---

¡Espero que este simulador te sea de gran utilidad para mejorar tus habilidades estratégicas! Si tienes alguna pregunta, no dudes en abrir un "Issue".
