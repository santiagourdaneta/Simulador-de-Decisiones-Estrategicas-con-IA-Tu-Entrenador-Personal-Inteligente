import streamlit as st
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import datetime
import os
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor # Importar el regresor
import sqlite3

# --- Configuración Inicial de la Aplicación ---
st.set_page_config(layout="wide", page_title="Simulador de Decisiones Estratégicas")

st.title("💡 Simulador de Toma de Decisiones Estratégicas con IA 🧠")
st.write("---") # Separador visual

# --- Constantes y Configuración ---
HISTORIAL_DB_FILE = 'historial_decisiones.db' # Archivo de base de datos SQLite
DATA_ENTRENAMIENTO_FILE = 'datos_entrenamiento.csv'

# --- Función para Inicializar la Base de Datos ---
def init_db():
    conn = sqlite3.connect(HISTORIAL_DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS decisiones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Fecha TEXT,
            Escenario TEXT,
            "Decision Tomada" TEXT,
            "Ganancia Estimada IA" INTEGER,
            "Clientes Felices Estimados IA" INTEGER,
            "Resultado IA" TEXT,
            "Feedback IA" TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Llamar a la función para asegurar que la DB existe al inicio
init_db()

@st.cache_data # Carga los datos una sola vez para mejorar el rendimiento
def load_and_train_models():
    try:
        df_entrenamiento = pd.read_csv(DATA_ENTRENAMIENTO_FILE)
    except FileNotFoundError:
        st.error(f"¡Error! No se encontró el archivo '{DATA_ENTRENAMIENTO_FILE}'. Asegúrate de que esté en la misma carpeta.")
        st.stop()

    # Columnas que la IA usará para aprender
    features = ['escenario', 'decision']
    
    # Objetivos numéricos para regresores
    numeric_targets = ['ganancia_estimada', 'clientes_felices_estimados', 'dificultad_ejecucion']
    # Objetivos categóricos para clasificadores
    categorical_targets = ['resultado_final', 'feedback_ia_ejemplo']

    X = df_entrenamiento[features]
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), features)
        ])

    models = {}


# Entrenar regresores para valores numéricos
    for target in numeric_targets:
        model_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                                         ('regressor', DecisionTreeRegressor(random_state=42))])
        model_pipeline.fit(X, df_entrenamiento[target])
        models[target] = model_pipeline

    # Entrenar clasificadores para valores categóricos
    for target in categorical_targets:
        model_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                                         ('classifier', DecisionTreeClassifier(random_state=42))])
        model_pipeline.fit(X, df_entrenamiento[target])
        models[target] = model_pipeline
    
    return models, df_entrenamiento

models, df_entrenamiento = load_and_train_models()

# --- Funciones Auxiliares ---

# --- Función para Guardar la Decisión (Modificada para SQLite) ---
def guardar_decision(escenario, decision_tomada, ganancia_ia, clientes_ia, resultado_ia, feedback_ia):
    conn = sqlite3.connect(HISTORIAL_DB_FILE)
    c = conn.cursor()
    c.execute('''
        INSERT INTO decisiones (Fecha, Escenario, "Decision Tomada", "Ganancia Estimada IA", "Clientes Felices Estimados IA", "Resultado IA", "Feedback IA")
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        escenario,
        decision_tomada,
        ganancia_ia,
        clientes_ia,
        resultado_ia,
        feedback_ia
    ))
    conn.commit()
    conn.close()

# --- Sección Principal del Simulador ---

st.header("🤔 Escenario Actual")

# Obtener escenarios únicos del archivo de entrenamiento
escenarios_disponibles = df_entrenamiento['escenario'].unique().tolist()
selected_escenario = st.selectbox("Elige un escenario para practicar:", escenarios_disponibles)

# Filtrar decisiones disponibles para el escenario seleccionado
decisiones_disponibles = df_entrenamiento[df_entrenamiento['escenario'] == selected_escenario]['decision'].unique().tolist()

if not decisiones_disponibles:
    st.warning("No hay decisiones disponibles para este escenario en los datos de entrenamiento.")
    st.stop()

st.write(f"**Escenario:** {selected_escenario}")
# Puedes añadir una descripción más detallada del escenario si la tuvieras en tus datos
if selected_escenario == "Tienda de Helados":
    st.write("¡Hoy hace mucho calor! Tienes que decidir qué tipo de helados preparar en mayor cantidad para vender más y tener clientes felices.")
elif selected_escenario == "Lanzamiento de Producto":
    st.write("Eres el CEO de una empresa. Tienes un nuevo producto innovador y debes decidir la mejor estrategia de lanzamiento al mercado.")
elif selected_escenario == "Inversión Personal":
    st.write("Tienes un dinero extra y quieres invertirlo. ¿Cómo lo harías para maximizar tu beneficio o asegurar tu futuro?")

decision_usuario = st.radio(
    "¿Qué decisión tomas?",
    decisiones_disponibles,
    key="decision_radio"
)

if st.button("🚀 Tomar Decisión y Obtener Retroalimentación"):
    if decision_usuario:
        st.success(f"¡Has decidido: **{decision_usuario}**!")
        st.info("La Inteligencia Artificial está analizando tu decisión...")

        # Preparar los datos de entrada para la predicción de la IA
        input_data_ia = pd.DataFrame({'escenario': [selected_escenario], 'decision': [decision_usuario]})

        # Realizar predicciones con los modelos entrenados
        pred_ganancia = models['ganancia_estimada'].predict(input_data_ia)[0]
        pred_clientes = models['clientes_felices_estimados'].predict(input_data_ia)[0]
        pred_resultado = models['resultado_final'].predict(input_data_ia)[0]
        pred_feedback = models['feedback_ia_ejemplo'].predict(input_data_ia)[0] # La IA predice el feedback

        st.write("---")
        st.subheader("🔮 Predicciones de la IA:")
        st.write(f"📈 **Ganancia Estimada:** {pred_ganancia} de 100")
        st.write(f"😊 **Clientes Felices Estimados:** {pred_clientes} de 100")
        st.write(f"💡 **Resultado General:** **{pred_resultado}**")

        st.subheader("💬 Retroalimentación de la IA sobre tu Lógica:")
        st.info(pred_feedback) # Usamos el feedback predicho por la IA

        # Guardar la decisión en el historial
        guardar_decision(selected_escenario, decision_usuario, pred_ganancia, pred_clientes, pred_resultado, pred_feedback)
        st.success("¡Tu decisión y las predicciones de la IA han sido guardadas en tu historial!")
    else:
        st.warning("Por favor, selecciona una decisión antes de continuar.")

### Paso 4: El Dashboard de Rendimiento (¡Tus Estadísticas de Superhéroe!)

# app.py (continuación, al final del archivo)

st.write("---")
st.header("📊 Tu Historial y Dashboard de Rendimiento")

conn = sqlite3.connect(HISTORIAL_DB_FILE)
df_historial = pd.read_sql_query("SELECT * FROM decisiones", conn)
conn.close()

if not df_historial.empty: # Cambiado de os.path.exists a verificar si el DataFrame está vacío
    st.subheader("Todas tus Decisiones:")
    # Asegúrate de que los nombres de las columnas coincidan con los de la base de datos

    st.subheader("Todas tus Decisiones:")
    st.dataframe(df_historial.style.highlight_max(axis=0, subset=['Ganancia Estimada IA', 'Clientes Felices Estimados IA']), use_container_width=True)

    st.subheader("Resumen de Rendimiento General:")
    col1, col2, col3 = st.columns(3)
    with col1:
        avg_ganancia = df_historial['Ganancia Estimada IA'].mean()
        st.metric(label="Ganancia Promedio", value=f"{avg_ganancia:.2f} / 100")
    with col2:
        avg_clientes = df_historial['Clientes Felices Estimados IA'].mean()
        st.metric(label="Clientes Felices Promedio", value=f"{avg_clientes:.2f} / 100")
    with col3:
        total_decisiones = len(df_historial)
        st.metric(label="Total de Decisiones", value=total_decisiones)

    st.write("---")
    st.subheader("Análisis Visual de Resultados:")

     # Gráfico de barras de resultados generales
    st.write("#### Frecuencia de Resultados Generales:")

    # Obtener el conteo de valores de 'Resultado IA'
    counts = df_historial['Resultado IA'].value_counts()

    # Crear un nuevo DataFrame directamente con los nombres de columna deseados
    # Esto evita cualquier ambigüedad con .reset_index() y .rename()
    df_chart_data = pd.DataFrame({'Resultado': counts.index, 'Count': counts.values})

    # Opcional: para depuración, puedes imprimir las columnas justo aquí
    # st.write("Columnas en df_chart_data ANTES de Plotly:", df_chart_data.columns.tolist())

    fig_resultados = px.bar(
        df_chart_data, # Ahora pasamos este DataFrame explícitamente construido
        x='Resultado',        # La columna 'Resultado' existe en df_chart_data
        y='Count',
        labels={'Resultado': 'Resultado', 'Count': 'Número de Decisiones'},
        title='Distribución de Resultados',
        color='Resultado', # Colorea las barras por el tipo de resultado
        color_discrete_map={"Éxito moderado": "green", "Fracaso parcial": "red", "Éxito decente": "blue",
                            "Gran éxito": "darkgreen", "Éxito de nicho": "purple", "Éxito masivo": "orange",
                            "Oportunidad perdida": "gray", "Recuperación rápida": "lightblue",
                            "Desastre de reputación": "darkred", "Empeoramiento de crisis": "black",
                            "Alto riesgo, alta recompensa": "gold", "Baja recompensa, alta seguridad": "lightgreen",
                            "Crecimiento mínimo": "brown"}
    )
    st.plotly_chart(fig_resultados, use_container_width=True)

    # Gráfico de línea para ver la evolución de la ganancia y clientes
    st.write("#### Evolución de Ganancia y Clientes Felices por Decisión:")
    df_historial['Decision_Num'] = range(1, len(df_historial) + 1)
    fig_evolucion = px.line(df_historial, x='Decision_Num', y=['Ganancia Estimada IA', 'Clientes Felices Estimados IA'],
                            title='Evolución de Ganancia y Clientes Felices',
                            labels={'Decision_Num': 'Número de Decisión'})
    st.plotly_chart(fig_evolucion, use_container_width=True)

    # Gráfico por escenario
    if len(df_historial['Escenario'].unique()) > 1:
        st.write("#### Rendimiento por Escenario:")
        df_escenario_avg = df_historial.groupby('Escenario')[['Ganancia Estimada IA', 'Clientes Felices Estimados IA']].mean().reset_index()
        fig_escenario = px.bar(df_escenario_avg, x='Escenario', y=['Ganancia Estimada IA', 'Clientes Felices Estimados IA'],
                               barmode='group', title='Ganancia y Clientes Promedio por Escenario')
        st.plotly_chart(fig_escenario, use_container_width=True)

else:
    st.info("Aún no has tomado ninguna decisión. ¡Anímate a empezar tu entrenamiento!")

st.write("---")
st.markdown("Desarrollado con Python, Streamlit, Scikit-learn y SQLite.")