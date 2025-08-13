import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import gspread
from google.oauth2.service_account import Credentials

# Configuración de la página
st.set_page_config(
    page_title="Dashboard de Poker",
    page_icon="🃏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Función para conectar con Google Sheets
@st.cache_data(ttl=300)  # Cache por 5 minutos
def load_data_from_sheets():
    """
    Carga datos desde tu Google Sheets publicado
    """
    try:
        # Tu URL de Google Sheets convertida a formato CSV
        sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS6eEcVMXlP__-DRkLq2btaRgOA6c5-a8Pdg0K_KaIcxxDemfGF_GquQyY6dXnav6jobGORIoAcpSgC/pub?gid=0&single=true&output=csv"
        
        # Carga los datos directamente desde Google Sheets
        df = pd.read_csv(sheet_url)
        
        # Muestra información sobre los datos cargados en el sidebar
        st.sidebar.success(f"✅ Datos cargados: {len(df)} registros")
        
        # Muestra las columnas encontradas para debugging
        st.sidebar.info(f"Columnas encontradas: {', '.join(df.columns.tolist())}")
        
        # Verifica que las columnas necesarias existan
        expected_columns = ['Jugador', 'Fecha', 'Jornada', 'Entradas', 'Poker', 'Utilidad']
        missing_columns = [col for col in expected_columns if col not in df.columns]
        
        if missing_columns:
            st.error(f"❌ Columnas faltantes en tu Google Sheet: {missing_columns}")
            st.info("💡 Verifica que los nombres de las columnas sean exactamente: Jugador, Fecha, Jornada, Entradas, Poker, Utilidad")
            return create_sample_data()
        
        # Limpia y procesa los datos
        df = df.dropna(subset=['Jugador', 'Fecha'])  # Elimina filas completamente vacías
        
        # Convierte tipos de datos
        df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
        df['Jornada'] = pd.to_numeric(df['Jornada'], errors='coerce')
        df['Entradas'] = pd.to_numeric(df['Entradas'], errors='coerce')
        df['Poker'] = pd.to_numeric(df['Poker'], errors='coerce')
        df['Utilidad'] = df['Utilidad'].str.replace(',', '.', regex=False)
        df['Utilidad'] = pd.to_numeric(df['Utilidad'], errors='coerce')
        
        # Elimina filas con fechas inválidas
        df = df.dropna(subset=['Fecha'])
        
        # Añade columna de semana para compatibilidad
        df['Semana'] = df['Fecha'].dt.strftime("%Y-W%U")
        
        # Información final en sidebar
        if len(df) > 0:
            st.sidebar.success(f"🎯 Datos procesados: {len(df)} registros válidos")
            st.sidebar.info(f"📅 Desde: {df['Fecha'].min().strftime('%Y-%m-%d')} hasta {df['Fecha'].max().strftime('%Y-%m-%d')}")
            st.sidebar.info(f"👥 Jugadores: {', '.join(df['Jugador'].unique())}")
        
        return df
        
    except Exception as e:
        st.error(f"❌ Error cargando datos de Google Sheets: {e}")
        st.info("📝 Usando datos de ejemplo. Verifica que tu Google Sheet esté publicado correctamente.")
        st.info("🔗 URL utilizada: https://docs.google.com/spreadsheets/d/e/2PACX-1vS...")
        return create_sample_data()

def create_sample_data():
    """Crea datos de ejemplo con la estructura de tu Google Sheet"""
    import random
    from datetime import datetime, timedelta
    
    jugadores = ["Ana", "Carlos", "Diana", "Eduardo", "Fernanda", "Gabriel"]
    
    data = []
    # Generar datos de las últimas 8 jornadas
    for jornada in range(1, 9):
        fecha = (datetime.now() - timedelta(weeks=8-jornada)).strftime("%Y-%m-%d")
        
        for jugador in jugadores:
            entradas = 5  # 5 euros fijos de entrada
            poker = random.randint(-30, 50)  # Ganancias/pérdidas del poker
            utilidad = poker - entradas  # Utilidad = Poker - Entradas
            
            data.append({
                "Jugador": jugador,
                "Fecha": fecha,
                "Jornada": jornada,
                "Entradas": entradas,
                "Poker": poker,
                "Utilidad": utilidad,
                "Semana": datetime.strptime(fecha, "%Y-%m-%d").strftime("%Y-W%U")
            })
    
    return pd.DataFrame(data)

def calculate_cumulative_stats(df):
    """Calcula estadísticas acumulativas por jugador"""
    df_sorted = df.sort_values(['Jugador', 'Fecha'])
    df_sorted['Utilidad_Acumulada'] = df_sorted.groupby('Jugador')['Utilidad'].cumsum()
    df_sorted['Poker_Acumulado'] = df_sorted.groupby('Jugador')['Poker'].cumsum()
    df_sorted['Entradas_Acumuladas'] = df_sorted.groupby('Jugador')['Entradas'].cumsum()
    return df_sorted

def create_ranking_table(df):
    """Crea la tabla de ranking general"""
    ranking = df.groupby('Jugador').agg({
        'Utilidad': ['sum', 'count', 'mean'],
        'Poker': 'sum',
        'Entradas': 'sum'
    }).round(2)
    
    ranking.columns = ['Utilidad_Total', 'Jornadas', 'Utilidad_Promedio', 'Poker_Total', 'Entradas_Total']
    ranking = ranking.sort_values('Utilidad_Total', ascending=False)
    ranking['Posición'] = range(1, len(ranking) + 1)
    ranking['ROI'] = ((ranking['Utilidad_Total'] / ranking['Entradas_Total']) * 100).round(1)
    
    return ranking[['Posición', 'Utilidad_Total', 'Poker_Total', 'Jornadas', 'Utilidad_Promedio', 'ROI']]

def main():
    # Título principal
    st.title("🃏 Dashboard de Poker BCN")
    st.markdown("---")
    
    # Cargar datos
    with st.spinner("Cargando datos..."):
        df = load_data_from_sheets()
    
    if df.empty:
        st.error("No se pudieron cargar los datos")
        return
    
    # Convertir fecha a datetime
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    df_cumulative = calculate_cumulative_stats(df)
    
    # Sidebar con filtros
    st.sidebar.header("Filtros")
    
    # Filtro de jugadores
    jugadores_seleccionados = st.sidebar.multiselect(
        "Seleccionar jugadores:",
        options=df['Jugador'].unique(),
        default=df['Jugador'].unique()
    )
    
    # Filtro de fechas
    fecha_min = df['Fecha'].min()
    fecha_max = df['Fecha'].max()
    
    fecha_inicio, fecha_fin = st.sidebar.date_input(
        "Rango de fechas:",
        value=(fecha_min, fecha_max),
        min_value=fecha_min,
        max_value=fecha_max
    )
    
    # Aplicar filtros
    df_filtered = df[
        (df['Jugador'].isin(jugadores_seleccionados)) &
        (df['Fecha'] >= pd.to_datetime(fecha_inicio)) &
        (df['Fecha'] <= pd.to_datetime(fecha_fin))
    ]
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_jornadas = len(df_filtered['Jornada'].unique())
        st.metric("Total Jornadas", total_jornadas)
    
    with col2:
        jugadores_activos = len(df_filtered['Jugador'].unique())
        st.metric("Jugadores Total", jugadores_activos)
    
    with col3:
        total_entradas = (df_filtered['Entradas'].sum())*5
        st.metric("Total Entradas", f"{total_entradas}€")
    
    with col4:
        total_poker = abs(df_filtered['Poker'].sum())
        st.metric("Suma Poker", f"{total_poker}")
    

    
    st.markdown("---")
    
    # Sección principal con dos columnas
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        # Gráfica de rendimiento acumulativo
        st.subheader("📈 Evolución de Utilidad Acumulativa")
        
        # Selector para el tipo de gráfica
        metric_option = st.selectbox(
            "Mostrar:",
            ["Utilidad Acumulada", "Poker Acumulado", "Entradas Acumuladas"],
            key="metric_selector"
        )
        
        metric_map = {
            "Utilidad Acumulada": "Utilidad_Acumulada",
            "Poker Acumulado": "Poker_Acumulado", 
            "Entradas Acumuladas": "Entradas_Acumuladas"
        }
        
        y_column = metric_map[metric_option]
        
        fig_cumulative = px.line(
            df_cumulative[df_cumulative['Jugador'].isin(jugadores_seleccionados)],
            x='Fecha',
            y=y_column,
            color='Jugador',
            title=f"Evolución de {metric_option} por Jugador",
            markers=True
        )
        
        fig_cumulative.update_layout(
            xaxis_title="Fecha",
            yaxis_title=f"{metric_option}",
            hovermode='x unified'
        )
        
        if metric_option != "Entradas Acumuladas":
            fig_cumulative.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
        
        st.plotly_chart(fig_cumulative, use_container_width=True)
    
    with col_right:
        # Tabla de ranking
        st.subheader("🏆 Ranking General")
        
        ranking_df = create_ranking_table(df_filtered)
        
        # Colorear la tabla
        def color_ranking(val):
            if val > 0:
                return 'color: green; font-weight: bold'
            elif val < 0:
                return 'color: red; font-weight: bold'
            else:
                return 'color: black'
        
        styled_ranking = ranking_df.style.applymap(
            color_ranking, 
            subset=['Utilidad_Total', 'Utilidad_Promedio']
        ).format({
            'Utilidad_Total': '{:.1f}€',
            'Poker_Total': '{:.1f}',
            'Utilidad_Promedio': '{:.1f}€',
            'ROI': '{:.1f}%'
        })
        
        st.dataframe(styled_ranking, use_container_width=True)
    
    # Segunda fila de gráficas
    st.markdown("---")
    
    col_graph1, col_graph2 = st.columns(2)
    
    with col_graph1:
        # Gráfica de barras por jornada
        st.subheader("📊 Utilidad por Jornada")
        
        jornada_data = df_filtered.groupby(['Jornada', 'Jugador'])['Utilidad'].sum().reset_index()
        
        fig_jornada = px.bar(
            jornada_data,
            x='Jornada',
            y='Utilidad',
            color='Jugador',
            title="Utilidad por Jornada",
            barmode='group'
        )
        
        fig_jornada.update_layout(
            xaxis_title="Jornada",
            yaxis_title="Utilidad (€)",
            xaxis_tickmode='linear'
        )
        
        fig_jornada.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
        
        st.plotly_chart(fig_jornada, use_container_width=True)
    
    with col_graph2:
        # Gráfica de distribución utilidad vs poker
        st.subheader("🎯 Poker vs Utilidad")
        
        scatter_data = df_filtered.groupby('Jugador').agg({
            'Poker': 'sum',
            'Utilidad': 'sum',
            'Jornada': 'count'  # Cambié 'Partidas' por 'Jornada'
        }).reset_index()
        
        # Renombrar columnas para que funcione con px.scatter
        scatter_data.columns = ['Jugador', 'Poker', 'Utilidad', 'Jornadas']
        
        fig_scatter = px.scatter(
            scatter_data,
            x='Poker',
            y='Utilidad',
            color='Jugador',
            size='Jornadas',
            title="Relación entre Ganancias de Poker y Utilidad Total",
            hover_data=['Jornadas']
        )
        
        fig_scatter.update_layout(
            xaxis_title="Total Poker (€)",
            yaxis_title="Utilidad Total (€)"
        )
        
        # Líneas de referencia
        fig_scatter.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
        fig_scatter.add_vline(x=0, line_dash="dash", line_color="gray", opacity=0.5)
        
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Tabla detallada
    st.markdown("---")
    st.subheader("📋 Historial Detallado")
    
    # Opción para mostrar datos resumidos o detallados
    view_option = st.radio(
        "Vista:",
        ["Últimas Jornadas", "Resumen por Jugador"],
        horizontal=True
    )
    
    if view_option == "Últimas Jornadas":
        # Mostrar últimas jornadas
        df_display = df_filtered.sort_values(['Jornada', 'Jugador'], ascending=[False, True]).copy()
        df_display['Fecha'] = df_display['Fecha'].dt.strftime('%Y-%m-%d')
        
        st.dataframe(
            df_display[['Jornada', 'Fecha', 'Jugador', 'Entradas', 'Poker', 'Utilidad']].head(30),
            use_container_width=True
        )
    else:
        # Mostrar resumen por jugador
        summary_data = df_filtered.groupby('Jugador').agg({
            'Jornada': 'count',
            'Entradas': 'sum',
            'Poker': ['sum', 'mean', 'std'],
            'Utilidad': ['sum', 'mean', 'min', 'max']
        }).round(2)
        
        # Aplanar columnas multiindex
        summary_data.columns = ['Jornadas', 'Total_Entradas', 'Total_Poker', 'Poker_Promedio', 'Poker_Std', 'Utilidad_Total', 'Utilidad_Promedio', 'Peor_Jornada', 'Mejor_Jornada']
        summary_data = summary_data.sort_values('Utilidad_Total', ascending=False)
        
        st.dataframe(summary_data, use_container_width=True)
    
    # Botón para actualizar datos
    st.markdown("---")
    if st.button("🔄 Actualizar Datos"):
        st.cache_data.clear()
        st.rerun()

if __name__ == "__main__":
    main()