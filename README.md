# 🃏 Dashboard de Poker - Grupo de Amigos

Dashboard interactivo para el seguimiento y análisis de partidas de poker entre amigos. Visualiza estadísticas, rankings y evolución de ganancias/pérdidas en tiempo real.

## 🚀 Ver Dashboard

**[🎮 Acceder al Dashboard](https://tu-app-poker.streamlit.app)** *(Reemplaza con tu URL real)*

## 📊 Características

### 🏆 Ranking General
- Clasificación por utilidad total
- ROI (Return on Investment) de cada jugador
- Estadísticas de participación por jornada
- Total de entradas pagadas vs ganancias del poker

### 📈 Análisis Visual
- **Evolución acumulativa**: Seguimiento de utilidad, poker y entradas a lo largo del tiempo
- **Rendimiento por jornada**: Comparación de resultados jornada a jornada
- **Poker vs Utilidad**: Análisis de la relación entre ganancias del poker y utilidad final
- **Filtros interactivos**: Por jugador y rango de fechas

### 📋 Datos Detallados
- Historial completo de todas las jornadas
- Resumen estadístico por jugador
- Métricas clave: total de jornadas, dinero en juego, utilidad promedio

## 🎯 Funcionalidades

- ✅ **Actualización automática** desde Google Sheets
- ✅ **Responsive design** - funciona en móviles y desktop
- ✅ **Filtros interactivos** por jugador y fecha
- ✅ **Gráficas dinámicas** con Plotly
- ✅ **Métricas en tiempo real**
- ✅ **Exportación de datos** (próximamente)

## 📱 Cómo usar

1. **Accede al dashboard** desde cualquier dispositivo
2. **Usa los filtros** en la barra lateral para personalizar la vista
3. **Explora las gráficas** haciendo hover para ver detalles
4. **Cambia entre vistas** en el historial detallado
5. **Actualiza datos** con el botón de actualizar

## 🔧 Estructura de Datos

El dashboard se alimenta automáticamente de un Google Sheet con estas columnas:

| Columna | Descripción | Ejemplo |
|---------|-------------|---------|
| `Jugador` | Nombre del jugador | "Carlos" |
| `Fecha` | Fecha de la jornada | "2024-01-15" |
| `Jornada` | Número de jornada | 1, 2, 3... |
| `Entradas` | Coste de entrada (€) | 5 |
| `Poker` | Ganancia/pérdida del poker (€) | 25, -10 |
| `Utilidad` | Ganancia neta (Poker - Entradas) | 20, -15 |

## 🎨 Capturas de Pantalla

### Dashboard Principal
*Aquí puedes añadir screenshots del dashboard*

### Ranking de Jugadores
*Screenshot del ranking*

### Evolución Temporal
*Screenshot de las gráficas*

## 🛠️ Tecnologías

- **Frontend**: Streamlit
- **Visualizaciones**: Plotly
- **Datos**: Pandas + Google Sheets
- **Deployment**: Streamlit Cloud
- **Actualización**: Tiempo real desde Google Sheets

## 📈 Métricas Principales

- **Utilidad Total**: Ganancia/pérdida neta por jugador
- **ROI**: Rendimiento sobre entradas pagadas
- **Jornadas Jugadas**: Participación de cada jugador
- **Evolución Acumulativa**: Progreso a lo largo del tiempo

## 🔄 Actualizaciones

El dashboard se actualiza automáticamente cada 5 minutos con los datos más recientes del Google Sheet. Para forzar una actualización inmediata, usa el botón "🔄 Actualizar Datos".

## 👥 Para los Jugadores

### Cómo ver tus estadísticas:
1. Abre el dashboard
2. Usa el filtro de jugadores para ver solo tus datos
3. Revisa tu posición en el ranking
4. Analiza tu evolución en las gráficas
5. Consulta el historial detallado

### Interpretación de las métricas:
- **Utilidad positiva**: Estás ganando dinero 💚
- **ROI > 0%**: Tus ganancias del poker superan las entradas 📈
- **Línea ascendente**: Tendencia positiva en el tiempo ⬆️

## 🎮 Próximas Funcionalidades

- [ ] Predicción de tendencias
- [ ] Alertas de rachas ganadoras/perdedoras
- [ ] Comparación con estadísticas históricas
- [ ] Exportación de reportes en PDF
- [ ] Sistema de logros y badges
- [ ] Análisis de varianza y volatilidad

## 🤝 Contribuciones

¿Ideas para mejorar el dashboard? ¡Comparte tus sugerencias!

## 📞 Soporte

Si encuentras algún problema o tienes sugerencias:
- Reporta el issue en este repositorio
- O contacta directamente al administrador

---

**🎯 ¡Que gane el mejor!** 🃏

*Dashboard creado con ❤️ para el grupo de poker*