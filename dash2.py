# dashboard_bi_avanzado.py
import dash
from dash import dcc, html, callback, Input, Output, State, dash_table
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import base64
import io

# Configuración de la app con tema personalizado
app = dash.Dash(__name__)
app.title = "Huawei BI Analytics Dashboard"

# Datos simulados expandidos y realistas
np.random.seed(42)

# 1. Datos históricos de tendencias (24 meses)
fechas = pd.date_range(start='2023-01-01', end='2024-12-31', freq='M')
tendencias_historicas = []
for i, fecha in enumerate(fechas):
    tendencias_historicas.append({
        'Fecha': fecha,
        'Mes': fecha.strftime('%B'),
        'Trimestre': f"Q{((fecha.month-1)//3)+1}",
        'Año': fecha.year,
        'Tendencias_Identificadas': np.random.poisson(3) + 1,
        'Inversión_Millones': np.random.normal(25, 8),
        'Equipos_Involucrados': np.random.poisson(6) + 2,
        'Prioridad_Alta': np.random.poisson(2),
        'Prioridad_Media': np.random.poisson(3),
        'Prioridad_Baja': np.random.poisson(1),
        'ROI_Esperado': np.random.normal(15, 5),
        'Tiempo_Implementacion': np.random.normal(120, 30),
        'Riesgo_Nivel': np.random.choice(['Alto', 'Medio', 'Bajo'], p=[0.2, 0.5, 0.3]),
        'Region': np.random.choice(['América', 'Europa', 'Asia-Pacífico', 'África'], p=[0.3, 0.25, 0.35, 0.1])
    })
df_tendencias_hist = pd.DataFrame(tendencias_historicas)

# 2. Datos detallados de proyectos
proyectos_data = []
estados_posibles = ['Completado', 'En Proceso', 'Pendiente', 'Cancelado', 'En Revisión', 'Aprobado']
for i in range(150):
    proyectos_data.append({
        'ID_Proyecto': f"PROJ-{i+1:03d}",
        'Nombre': f"Proyecto Tendencia {i+1}",
        'Estado': np.random.choice(estados_posibles, p=[0.35, 0.25, 0.15, 0.05, 0.1, 0.1]),
        'Fecha_Inicio': np.random.choice(fechas),
        'Presupuesto': np.random.normal(2.5, 1) * 1000000,
        'Progreso': np.random.uniform(0, 100),
        'Manager': np.random.choice(['Ana García', 'Carlos López', 'María Chen', 'David Kim', 'Sarah Johnson']),
        'Departamento': np.random.choice(['I+D', 'Marketing', 'Operaciones', 'Estrategia', 'Tecnología']),
        'Prioridad': np.random.choice(['Alta', 'Media', 'Baja'], p=[0.3, 0.5, 0.2]),
        'Impacto_Esperado': np.random.uniform(1, 10),
        'Tecnologia_Principal': np.random.choice(['5G', 'IA', 'IoT', 'Cloud', 'Edge Computing', 'Blockchain'])
    })
df_proyectos = pd.DataFrame(proyectos_data)

# 3. Datos de performance por tecnología con tendencias temporales
tecnologias = ['5G', 'IA/ML', 'IoT', 'Cloud Computing', 'Edge Computing', 'Blockchain', 'Quantum Computing', 'AR/VR', 'Cybersecurity', 'Digital Twins']
tech_performance = []
for tech in tecnologias:
    for fecha in fechas[-12:]:  # Últimos 12 meses
        tech_performance.append({
            'Tecnologia': tech,
            'Fecha': fecha,
            'Impacto_Actual': np.random.normal(60, 15),
            'Potencial_Futuro': np.random.normal(80, 10),
            'Inversion_Actual': np.random.normal(30, 10),
            'Madurez_Tecnologica': np.random.uniform(0.3, 0.9),
            'Adopcion_Mercado': np.random.uniform(0.2, 0.8),
            'Competitividad': np.random.uniform(0.4, 0.95),
            'Satisfaccion_Cliente': np.random.normal(78, 12)
        })
df_tech_performance = pd.DataFrame(tech_performance)

# 4. Datos de KPIs operacionales
kpis_data = []
for fecha in fechas:
    kpis_data.append({
        'Fecha': fecha,
        'Tiempo_Respuesta_Dias': np.random.normal(35, 10),
        'Satisfaccion_Cliente': np.random.normal(82, 8),
        'Tasa_Exito_Proyectos': np.random.normal(0.75, 0.1),
        'Eficiencia_Operacional': np.random.normal(0.68, 0.12),
        'Innovaciones_Mes': np.random.poisson(5),
        'Revenue_Impacto_Millones': np.random.normal(45, 15),
        'Costo_Operacional_Millones': np.random.normal(25, 8),
        'Margen_Beneficio': np.random.normal(0.35, 0.08),
        'NPS_Score': np.random.normal(72, 15),
        'Tiempo_Market_Meses': np.random.normal(8, 2)
    })
df_kpis = pd.DataFrame(kpis_data)

# 5. Datos de benchmark competitivo
competidores = ['Huawei', 'Ericsson', 'Nokia', 'Samsung', 'Cisco', 'ZTE']
benchmark_data = []
for comp in competidores:
    benchmark_data.append({
        'Empresa': comp,
        'Market_Share': np.random.uniform(0.08, 0.25) if comp == 'Huawei' else np.random.uniform(0.05, 0.2),
        'Innovation_Index': np.random.uniform(0.6, 0.95) if comp == 'Huawei' else np.random.uniform(0.5, 0.85),
        'Customer_Satisfaction': np.random.uniform(75, 90) if comp == 'Huawei' else np.random.uniform(65, 85),
        'R&D_Investment_Billions': np.random.uniform(8, 15) if comp == 'Huawei' else np.random.uniform(3, 12),
        'Patents_Filed': np.random.randint(800, 2000) if comp == 'Huawei' else np.random.randint(200, 1500)
    })
df_benchmark = pd.DataFrame(benchmark_data)

# Funciones auxiliares para análisis avanzado
def calcular_alertas():
    """Genera alertas inteligentes basadas en KPIs"""
    alertas = []
    ultimo_mes = df_kpis.iloc[-1]
    
    if ultimo_mes['Tiempo_Respuesta_Dias'] > 45:
        alertas.append({
            'tipo': 'warning',
            'mensaje': f"⚠️ Tiempo de respuesta elevado: {ultimo_mes['Tiempo_Respuesta_Dias']:.1f} días",
            'prioridad': 'Alta'
        })
    
    if ultimo_mes['Satisfaccion_Cliente'] < 75:
        alertas.append({
            'tipo': 'danger',
            'mensaje': f"🚨 Satisfacción del cliente por debajo del umbral: {ultimo_mes['Satisfaccion_Cliente']:.1f}%",
            'prioridad': 'Crítica'
        })
    
    if ultimo_mes['Tasa_Exito_Proyectos'] < 0.7:
        alertas.append({
            'tipo': 'warning',
            'mensaje': f"⚠️ Tasa de éxito de proyectos baja: {ultimo_mes['Tasa_Exito_Proyectos']:.1%}",
            'prioridad': 'Media'
        })
    
    return alertas

def generar_insights():
    """Genera insights automáticos usando IA simulada"""
    insights = [
        "📈 Las tendencias de IA muestran un crecimiento del 23% este trimestre",
        "🎯 Los proyectos de 5G tienen una tasa de éxito 15% superior al promedio",
        "💡 Oportunidad identificada: Edge Computing subutilizado con potencial alto",
        "⚡ Tiempo de respuesta mejoró 18% comparado con el trimestre anterior",
        "🌟 La satisfacción del cliente en la región Asia-Pacífico lidera con 87%"
    ]
    return insights

# Funciones para crear gráficos avanzados
def crear_grafico_tendencias_avanzado(año_filtro=None, region_filtro=None):
    """Gráfico de tendencias con filtros y análisis predictivo"""
    df_filtrado = df_tendencias_hist.copy()
    
    if año_filtro:
        df_filtrado = df_filtrado[df_filtrado['Año'] == año_filtro]
    if region_filtro and region_filtro != 'Todas':
        df_filtrado = df_filtrado[df_filtrado['Region'] == region_filtro]
    
    fig = go.Figure()
    
    # Tendencias por trimestre
    df_trim = df_filtrado.groupby(['Trimestre', 'Año']).agg({
        'Tendencias_Identificadas': 'sum',
        'Inversión_Millones': 'sum',
        'ROI_Esperado': 'mean'
    }).reset_index()
    
    df_trim['Periodo'] = df_trim['Año'].astype(str) + '-' + df_trim['Trimestre']
    
    fig.add_trace(go.Bar(
        x=df_trim['Periodo'],
        y=df_trim['Tendencias_Identificadas'],
        name='Tendencias Identificadas',
        marker_color='rgba(55, 128, 191, 0.8)',
        hovertemplate='<b>%{x}</b><br>' +
                      'Tendencias: %{y}<br>' +
                      'Inversión: $%{customdata[0]:.1f}M<br>' +
                      'ROI Esperado: %{customdata[1]:.1f}%<extra></extra>',
        customdata=np.column_stack((df_trim['Inversión_Millones'], df_trim['ROI_Esperado']))
    ))
    
    # Línea de tendencia predictiva
    z = np.polyfit(range(len(df_trim)), df_trim['Tendencias_Identificadas'], 1)
    p = np.poly1d(z)
    prediccion = p(range(len(df_trim), len(df_trim) + 4))
    
    fig.add_trace(go.Scatter(
        x=df_trim['Periodo'].tolist() + [f"Pred-{i+1}" for i in range(4)],
        y=df_trim['Tendencias_Identificadas'].tolist() + prediccion.tolist(),
        mode='lines+markers',
        name='Predicción IA',
        line=dict(color='red', width=2, dash='dash'),
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        title='📊 Análisis Predictivo de Tendencias Emergentes',
        xaxis_title='Período',
        yaxis_title='Número de Tendencias',
        hovermode='x unified',
        template='plotly_white',
        height=500
    )
    
    return fig

def crear_matriz_riesgo_oportunidad():
    """Matriz de riesgo vs oportunidad para tecnologías"""
    df_actual = df_tech_performance[df_tech_performance['Fecha'] == df_tech_performance['Fecha'].max()]
    
    fig = px.scatter(
        df_actual,
        x='Madurez_Tecnologica',
        y='Potencial_Futuro',
        size='Inversion_Actual',
        color='Adopcion_Mercado',
        hover_name='Tecnologia',
        hover_data={
            'Impacto_Actual': ':.1f',
            'Competitividad': ':.2f',
            'Satisfaccion_Cliente': ':.1f'
        },
        color_continuous_scale='Viridis',
        title='🎯 Matriz Estratégica: Riesgo vs Oportunidad por Tecnología'
    )
    
    # Añadir cuadrantes
    fig.add_hline(y=70, line_dash="dash", line_color="gray", opacity=0.5)
    fig.add_vline(x=0.6, line_dash="dash", line_color="gray", opacity=0.5)
    
    # Etiquetas de cuadrantes
    fig.add_annotation(x=0.8, y=85, text="⭐ Estrellas", showarrow=False, bgcolor="lightgreen", opacity=0.7)
    fig.add_annotation(x=0.4, y=85, text="🚀 Potencial Alto", showarrow=False, bgcolor="lightblue", opacity=0.7)
    fig.add_annotation(x=0.8, y=55, text="💰 Cash Cows", showarrow=False, bgcolor="lightyellow", opacity=0.7)
    fig.add_annotation(x=0.4, y=55, text="❓ Interrogantes", showarrow=False, bgcolor="lightcoral", opacity=0.7)
    
    fig.update_layout(
        xaxis_title='Madurez Tecnológica',
        yaxis_title='Potencial Futuro',
        template='plotly_white',
        height=600
    )
    
    return fig

def crear_dashboard_kpis():
    """Dashboard de KPIs con métricas en tiempo real"""
    ultimo_mes = df_kpis.iloc[-1]
    mes_anterior = df_kpis.iloc[-2]
    
    # Calcular cambios
    cambios = {
        'tiempo_respuesta': ((ultimo_mes['Tiempo_Respuesta_Dias'] - mes_anterior['Tiempo_Respuesta_Dias']) / mes_anterior['Tiempo_Respuesta_Dias']) * 100,
        'satisfaccion': ((ultimo_mes['Satisfaccion_Cliente'] - mes_anterior['Satisfaccion_Cliente']) / mes_anterior['Satisfaccion_Cliente']) * 100,
        'eficiencia': ((ultimo_mes['Eficiencia_Operacional'] - mes_anterior['Eficiencia_Operacional']) / mes_anterior['Eficiencia_Operacional']) * 100,
        'revenue': ((ultimo_mes['Revenue_Impacto_Millones'] - mes_anterior['Revenue_Impacto_Millones']) / mes_anterior['Revenue_Impacto_Millones']) * 100
    }
    
    fig = go.Figure()
    
    # Indicadores tipo gauge
    kpis = [
        ('Satisfacción Cliente', ultimo_mes['Satisfaccion_Cliente'], cambios['satisfaccion'], 0, 100, [0, 60, 80, 100]),
        ('Eficiencia Operacional', ultimo_mes['Eficiencia_Operacional'] * 100, cambios['eficiencia'], 0, 100, [0, 50, 75, 100]),
        ('Tiempo Respuesta', 60 - ultimo_mes['Tiempo_Respuesta_Dias'], -cambios['tiempo_respuesta'], 0, 60, [0, 20, 40, 60]),
        ('Revenue Impact', ultimo_mes['Revenue_Impacto_Millones'], cambios['revenue'], 0, 100, [0, 30, 60, 100])
    ]
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    
    for i, (nombre, valor, cambio, min_val, max_val, thresholds) in enumerate(kpis):
        fig.add_trace(go.Indicator(
            mode="gauge+number+delta",
            value=valor,
            domain={'row': i//2, 'column': i%2},
            title={'text': f"{nombre}"},
            delta={'reference': valor - (valor * cambio / 100), 'increasing': {'color': "green"}, 'decreasing': {'color': "red"}},
            gauge={
                'axis': {'range': [min_val, max_val]},
                'bar': {'color': colors[i]},
                'steps': [
                    {'range': [thresholds[0], thresholds[1]], 'color': "lightgray"},
                    {'range': [thresholds[1], thresholds[2]], 'color': "yellow"},
                    {'range': [thresholds[2], thresholds[3]], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': thresholds[2]
                }
            }
        ))
    
    fig.update_layout(
        grid={'rows': 2, 'columns': 2, 'pattern': "independent"},
        template='plotly_white',
        height=600,
        title='📊 Dashboard de KPIs en Tiempo Real'
    )
    
    return fig

def crear_analisis_competitivo():
    """Análisis competitivo radar avanzado"""
    fig = go.Figure()
    
    categorias = ['Market Share', 'Innovation Index', 'Customer Satisfaction', 'R&D Investment', 'Patents Filed']
    
    for empresa in df_benchmark['Empresa']:
        empresa_data = df_benchmark[df_benchmark['Empresa'] == empresa].iloc[0]
        valores = [
            empresa_data['Market_Share'] * 100,
            empresa_data['Innovation_Index'] * 100,
            empresa_data['Customer_Satisfaction'],
            (empresa_data['R&D_Investment_Billions'] / 15) * 100,  # Normalizado
            (empresa_data['Patents_Filed'] / 2000) * 100  # Normalizado
        ]
        
        fig.add_trace(go.Scatterpolar(
            r=valores + [valores[0]],
            theta=categorias + [categorias[0]],
            fill='toself' if empresa == 'Huawei' else 'none',
            name=empresa,
            line=dict(width=3 if empresa == 'Huawei' else 1),
            fillcolor='rgba(31, 119, 180, 0.3)' if empresa == 'Huawei' else None
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=10)
            )
        ),
        title='🏆 Análisis Competitivo - Posicionamiento en el Mercado',
        template='plotly_white',
        height=600
    )
    
    return fig

def crear_tabla_proyectos():
    """Tabla interactiva de proyectos con filtros"""
    df_tabla = df_proyectos.copy()
    df_tabla['Fecha_Inicio'] = df_tabla['Fecha_Inicio'].dt.strftime('%Y-%m-%d')
    df_tabla['Presupuesto'] = df_tabla['Presupuesto'].apply(lambda x: f"${x/1000000:.1f}M")
    df_tabla['Progreso'] = df_tabla['Progreso'].apply(lambda x: f"{x:.1f}%")
    
    return dash_table.DataTable(
        data=df_tabla.to_dict('records'),
        columns=[
            {'name': 'ID', 'id': 'ID_Proyecto'},
            {'name': 'Proyecto', 'id': 'Nombre'},
            {'name': 'Estado', 'id': 'Estado'},
            {'name': 'Fecha Inicio', 'id': 'Fecha_Inicio'},
            {'name': 'Presupuesto', 'id': 'Presupuesto'},
            {'name': 'Progreso', 'id': 'Progreso'},
            {'name': 'Manager', 'id': 'Manager'},
            {'name': 'Departamento', 'id': 'Departamento'},
            {'name': 'Prioridad', 'id': 'Prioridad'},
            {'name': 'Tecnología', 'id': 'Tecnologia_Principal'}
        ],
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        page_action="native",
        page_current=0,
        page_size=10,
        style_cell={'textAlign': 'left', 'padding': '10px'},
        style_data_conditional=[
            {
                'if': {'filter_query': '{Estado} = Completado'},
                'backgroundColor': '#d4edda',
                'color': 'black',
            },
            {
                'if': {'filter_query': '{Estado} = Cancelado'},
                'backgroundColor': '#f8d7da',
                'color': 'black',
            },
            {
                'if': {'filter_query': '{Prioridad} = Alta'},
                'backgroundColor': '#fff3cd',
                'color': 'black',
            }
        ],
        style_header={
            'backgroundColor': '#007bff',
            'color': 'white',
            'fontWeight': 'bold'
        }
    )

# Layout principal del dashboard avanzado
app.layout = html.Div([
    # Header principal con branding
    html.Div([
        html.Div([
            html.H1('🚀 Huawei Enterprise BI Analytics', 
                    style={'color': '#FFFFFF', 'margin': '0', 'fontSize': '2.5rem'}),
            html.P('Advanced Business Intelligence Dashboard | Real-time Analytics & Predictive Insights',
                   style={'color': '#E3F2FD', 'margin': '5px 0 0 0', 'fontSize': '1.1rem'})
        ], style={'flex': '1'}),
        
        html.Div([
            html.Div(id='live-clock', style={'color': '#FFFFFF', 'fontSize': '1.2rem', 'textAlign': 'right'}),
            html.P('🟢 Sistema Online | Última actualización: Tiempo real', 
                   style={'color': '#C8E6C9', 'margin': '5px 0 0 0', 'fontSize': '0.9rem', 'textAlign': 'right'})
        ])
    ], style={
        'background': 'linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)',
        'padding': '25px 40px',
        'display': 'flex',
        'justifyContent': 'space-between',
        'alignItems': 'center',
        'marginBottom': '0px',
        'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'
    }),
    
    # Panel de alertas inteligentes
    html.Div(id='alertas-panel', style={'margin': '20px'}),
    
    # Panel de control avanzado
    html.Div([
        html.Div([
            html.Label('📅 Período de Análisis:', style={'fontWeight': 'bold', 'marginBottom': '5px', 'display': 'block'}),
            dcc.DatePickerRange(
                id='date-picker-range',
                start_date=df_tendencias_hist['Fecha'].min(),
                end_date=df_tendencias_hist['Fecha'].max(),
                display_format='DD/MM/YYYY',
                style={'width': '100%'}
            )
        ], className='control-item'),
        
        html.Div([
            html.Label('🌍 Región:', style={'fontWeight': 'bold', 'marginBottom': '5px', 'display': 'block'}),
            dcc.Dropdown(
                id='region-filter',
                options=[{'label': 'Todas las Regiones', 'value': 'Todas'}] +
                        [{'label': region, 'value': region} for region in df_tendencias_hist['Region'].unique()],
                value='Todas',
                clearable=False
            )
        ], className='control-item'),
        
        html.Div([
            html.Label('📊 Vista del Dashboard:', style={'fontWeight': 'bold', 'marginBottom': '5px', 'display': 'block'}),
            dcc.Dropdown(
                id='dashboard-view',
                options=[
                    {'label': '🎯 Executive Summary', 'value': 'executive'},
                    {'label': '📈 Análisis Predictivo', 'value': 'predictivo'},
                    {'label': '💼 Gestión de Proyectos', 'value': 'proyectos'},
                    {'label': '🏆 Análisis Competitivo', 'value': 'competitivo'},
                    {'label': '🔍 Vista Completa', 'value': 'completa'}
                ],
                value='executive',
                clearable=False
            )
        ], className='control-item'),
        
        html.Div([
            html.Button('📊 Exportar Datos', id='export-btn', 
                       style={'backgroundColor': '#28a745', 'color': 'white', 'border': 'none', 
                             'padding': '10px 20px', 'borderRadius': '5px', 'cursor': 'pointer', 'width': '100%'}),
            html.Button('🔄 Actualizar Dashboard', id='refresh-btn',
                       style={'backgroundColor': '#007bff', 'color': 'white', 'border': 'none',
                             'padding': '10px 20px', 'borderRadius': '5px', 'cursor': 'pointer', 'width': '100%', 'marginTop': '10px'})
        ], className='control-item')
    ], style={
        'display': 'grid',
        'gridTemplateColumns': 'repeat(auto-fit, minmax(250px, 1fr))',
        'gap': '20px',
        'margin': '20px',
        'padding': '20px',
        'backgroundColor': '#f8f9fa',
        'borderRadius': '10px',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
    }),
    
    # Panel de insights de IA
    html.Div([
        html.H3('🤖 Insights Inteligentes', style={'color': '#2c3e50', 'marginBottom': '15px'}),
        html.Div(id='insights-panel')
    ], style={'margin': '20px', 'padding': '20px', 'backgroundColor': '#e8f4fd', 'borderRadius': '10px'}),
    
    # Contenedor principal de visualizaciones
    html.Div(id='main-dashboard-content'),
    
    # Footer con información del sistema
    html.Div([
        html.Div([
            html.P('📊 Huawei Enterprise BI Analytics Platform v2.0', style={'margin': '0', 'fontWeight': 'bold'}),
            html.P('Powered by Advanced Analytics & Machine Learning', style={'margin': '0', 'fontSize': '0.9rem', 'color': '#666'})
        ], style={'flex': '1'}),
        
        html.Div([
            html.P(f'📅 {datetime.now().strftime("%d/%m/%Y %H:%M")}', style={'margin': '0', 'textAlign': 'right'}),
            html.P('🔐 Secure Connection | 🌐 Global Access', style={'margin': '0', 'fontSize': '0.9rem', 'color': '#666', 'textAlign': 'right'})
        ])
    ], style={
        'backgroundColor': '#2c3e50',
        'color': 'white',
        'padding': '20px 40px',
        'marginTop': '40px',
        'display': 'flex',
        'justifyContent': 'space-between',
        'alignItems': 'center'
    }),
    
    dcc.Download(id="download-dataframe-csv"),
    dcc.Interval(id='interval-component', interval=60*1000, n_intervals=0)  # Actualiza cada minuto
])

# Callbacks para interactividad avanzada
@app.callback(
    Output('live-clock', 'children'),
    [Input('interval-component', 'n_intervals')]
)
def update_clock(n):
    return datetime.now().strftime('%H:%M:%S | %d/%m/%Y')

@app.callback(
    Output('alertas-panel', 'children'),
    [Input('interval-component', 'n_intervals')]
)
def update_alertas(n):
    alertas = calcular_alertas()
    if not alertas:
        return html.Div([
            html.H4('✅ Sistema Operando Normalmente', style={'color': '#28a745', 'textAlign': 'center'})
        ], style={'backgroundColor': '#d4edda', 'padding': '15px', 'borderRadius': '5px', 'border': '1px solid #c3e6cb'})
    
    alertas_html = []
    for alerta in alertas:
        color = '#dc3545' if alerta['tipo'] == 'danger' else '#ffc107'
        bg_color = '#f8d7da' if alerta['tipo'] == 'danger' else '#fff3cd'
        alertas_html.append(
            html.Div([
                html.Strong(f"[{alerta['prioridad']}] "),
                html.Span(alerta['mensaje'])
            ], style={'backgroundColor': bg_color, 'padding': '10px', 'margin': '5px 0', 
                     'borderRadius': '5px', 'border': f'1px solid {color}', 'color': '#721c24' if alerta['tipo'] == 'danger' else '#856404'})
        )
    
    return html.Div(alertas_html)

@app.callback(
    Output('insights-panel', 'children'),
    [Input('refresh-btn', 'n_clicks')]
)
def update_insights(n_clicks):
    insights = generar_insights()
    return html.Div([
        html.Div([
            html.Span('💡 ', style={'fontSize': '1.2rem', 'marginRight': '10px'}),
            html.Span(insight, style={'fontSize': '1rem'})
        ], style={'backgroundColor': 'white', 'padding': '12px', 'margin': '8px 0', 
                 'borderRadius': '8px', 'border': '1px solid #bee5eb', 'boxShadow': '0 1px 3px rgba(0,0,0,0.1)'})
        for insight in insights
    ])

@app.callback(
    Output('main-dashboard-content', 'children'),
    [Input('dashboard-view', 'value'),
     Input('region-filter', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_dashboard_content(vista, region, start_date, end_date):
    if vista == 'executive':
        return html.Div([
            # Métricas principales en cards
            html.Div([
                html.Div([
                    html.H3('📊 KPIs Ejecutivos', style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '20px'})
                ], style={'gridColumn': '1 / -1'}),
                
                # Card 1: Revenue Impact
                html.Div([
                    html.H4(f'${df_kpis.iloc[-1]["Revenue_Impacto_Millones"]:.1f}M', style={'color': '#28a745', 'fontSize': '2.5rem', 'margin': '0'}),
                    html.P('Revenue Impact', style={'color': '#666', 'margin': '5px 0'}),
                    html.P(f'+{((df_kpis.iloc[-1]["Revenue_Impacto_Millones"] - df_kpis.iloc[-2]["Revenue_Impacto_Millones"]) / df_kpis.iloc[-2]["Revenue_Impacto_Millones"] * 100):.1f}% vs mes anterior', 
                           style={'color': '#28a745', 'fontSize': '0.9rem', 'margin': '0'})
                ], className='metric-card'),
                
                # Card 2: Proyectos Activos
                html.Div([
                    html.H4(f'{len(df_proyectos[df_proyectos["Estado"].isin(["En Proceso", "Aprobado"])])}', 
                           style={'color': '#007bff', 'fontSize': '2.5rem', 'margin': '0'}),
                    html.P('Proyectos Activos', style={'color': '#666', 'margin': '5px 0'}),
                    html.P(f'{len(df_proyectos[df_proyectos["Estado"] == "Completado"])} completados este mes', 
                           style={'color': '#007bff', 'fontSize': '0.9rem', 'margin': '0'})
                ], className='metric-card'),
                
                # Card 3: Satisfacción Cliente
                html.Div([
                    html.H4(f'{df_kpis.iloc[-1]["Satisfaccion_Cliente"]:.1f}%', 
                           style={'color': '#dc3545', 'fontSize': '2.5rem', 'margin': '0'}),
                    html.P('Satisfacción Cliente', style={'color': '#666', 'margin': '5px 0'}),
                    html.P(f'NPS Score: {df_kpis.iloc[-1]["NPS_Score"]:.0f}', 
                           style={'color': '#dc3545', 'fontSize': '0.9rem', 'margin': '0'})
                ], className='metric-card'),
                
                # Card 4: Eficiencia Operacional
                html.Div([
                    html.H4(f'{df_kpis.iloc[-1]["Eficiencia_Operacional"]:.1%}', 
                           style={'color': '#ffc107', 'fontSize': '2.5rem', 'margin': '0'}),
                    html.P('Eficiencia Operacional', style={'color': '#666', 'margin': '5px 0'}),
                    html.P(f'Tiempo al mercado: {df_kpis.iloc[-1]["Tiempo_Market_Meses"]:.1f} meses', 
                           style={'color': '#ffc107', 'fontSize': '0.9rem', 'margin': '0'})
                ], className='metric-card')
            ], style={
                'display': 'grid',
                'gridTemplateColumns': 'repeat(auto-fit, minmax(250px, 1fr))',
                'gap': '20px',
                'margin': '20px 0'
            }),
            
            # Dashboard de KPIs
            html.Div([
                dcc.Graph(figure=crear_dashboard_kpis())
            ], style={'margin': '20px 0'}),
            
            # Tendencias principales
            html.Div([
                dcc.Graph(figure=crear_grafico_tendencias_avanzado(region_filtro=region))
            ], style={'margin': '20px 0'})
        ])
    
    elif vista == 'predictivo':
        return html.Div([
            html.H2('🔮 Análisis Predictivo Avanzado', style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '30px'}),
            
            # Matriz de riesgo-oportunidad
            html.Div([
                dcc.Graph(figure=crear_matriz_riesgo_oportunidad())
            ], style={'margin': '20px 0'}),
            
            # Predicciones de tendencias
            html.Div([
                dcc.Graph(figure=crear_grafico_tendencias_avanzado(region_filtro=region))
            ], style={'margin': '20px 0'}),
            
            # Análisis de correlaciones
            html.Div([
                html.H3('📊 Análisis de Correlaciones Clave', style={'color': '#2c3e50'}),
                dcc.Graph(
                    figure=px.scatter_matrix(
                        df_kpis[['Tiempo_Respuesta_Dias', 'Satisfaccion_Cliente', 'Eficiencia_Operacional', 'Revenue_Impacto_Millones']].tail(50),
                        title='Matriz de Correlaciones - Últimos 50 períodos',
                        height=600
                    )
                )
            ], style={'margin': '20px 0'})
        ])
    
    elif vista == 'proyectos':
        return html.Div([
            html.H2('💼 Gestión Avanzada de Proyectos', style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '30px'}),
            
            # Resumen de proyectos por estado
            html.Div([
                html.Div([
                    dcc.Graph(
                        figure=px.pie(
                            df_proyectos.groupby('Estado').size().reset_index(name='count'),
                            values='count',
                            names='Estado',
                            title='🎯 Distribución de Proyectos por Estado',
                            color_discrete_sequence=px.colors.qualitative.Set3
                        )
                    )
                ], style={'width': '50%', 'display': 'inline-block'}),
                
                html.Div([
                    dcc.Graph(
                        figure=px.box(
                            df_proyectos,
                            x='Departamento',
                            y='Progreso',
                            title='📈 Progreso por Departamento',
                            color='Prioridad'
                        )
                    )
                ], style={'width': '50%', 'display': 'inline-block'})
            ]),
            
            # Análisis de presupuesto vs progreso
            html.Div([
                dcc.Graph(
                    figure=px.scatter(
                        df_proyectos,
                        x='Presupuesto',
                        y='Progreso',
                        size='Impacto_Esperado',
                        color='Estado',
                        hover_name='Nombre',
                        title='💰 Análisis Presupuesto vs Progreso vs Impacto',
                        labels={'Presupuesto': 'Presupuesto ($M)', 'Progreso': 'Progreso (%)'}
                    )
                )
            ], style={'margin': '20px 0'}),
            
            # Tabla detallada de proyectos
            html.Div([
                html.H3('📋 Tabla Detallada de Proyectos', style={'color': '#2c3e50', 'marginBottom': '15px'}),
                crear_tabla_proyectos()
            ], style={'margin': '20px 0'})
        ])
    
    elif vista == 'competitivo':
        return html.Div([
            html.H2('🏆 Inteligencia Competitiva', style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '30px'}),
            
            # Análisis radar competitivo
            html.Div([
                dcc.Graph(figure=crear_analisis_competitivo())
            ], style={'margin': '20px 0'}),
            
            # Métricas competitivas
            html.Div([
                html.Div([
                    dcc.Graph(
                        figure=px.bar(
                            df_benchmark.sort_values('Market_Share', ascending=True),
                            x='Market_Share',
                            y='Empresa',
                            title='📊 Market Share por Competidor',
                            orientation='h',
                            color='Market_Share',
                            color_continuous_scale='viridis'
                        )
                    )
                ], style={'width': '50%', 'display': 'inline-block'}),
                
                html.Div([
                    dcc.Graph(
                        figure=px.scatter(
                            df_benchmark,
                            x='R&D_Investment_Billions',
                            y='Innovation_Index',
                            size='Patents_Filed',
                            color='Customer_Satisfaction',
                            hover_name='Empresa',
                            title='🔬 I+D vs Innovación vs Patentes',
                            labels={'R&D_Investment_Billions': 'Inversión I+D (B$)', 'Innovation_Index': 'Índice de Innovación'}
                        )
                    )
                ], style={'width': '50%', 'display': 'inline-block'})
            ])
        ])
    
    else:  # vista completa
        return html.Div([
            html.H2('🔍 Vista Completa del Dashboard', style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '30px'}),
            
            # Grid de gráficos completo
            html.Div([
                dcc.Graph(figure=crear_dashboard_kpis()),
                dcc.Graph(figure=crear_grafico_tendencias_avanzado(region_filtro=region)),
                dcc.Graph(figure=crear_matriz_riesgo_oportunidad()),
                dcc.Graph(figure=crear_analisis_competitivo())
            ])
        ])

@app.callback(
    Output("download-dataframe-csv", "data"),
    [Input("export-btn", "n_clicks")],
    prevent_initial_call=True
)
def export_data(n_clicks):
    if n_clicks:
        # Combinar todos los datos para exportación
        export_data = {
            'tendencias': df_tendencias_hist.to_csv(index=False),
            'proyectos': df_proyectos.to_csv(index=False),
            'kpis': df_kpis.to_csv(index=False),
            'benchmark': df_benchmark.to_csv(index=False)
        }
        
        return dict(content=json.dumps(export_data, indent=2), 
                   filename=f"huawei_bi_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

# CSS personalizado
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            .metric-card {
                background: white;
                border-radius: 10px;
                padding: 25px;
                text-align: center;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                border-left: 4px solid #007bff;
                transition: all 0.3s ease;
            }
            .metric-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
            }
            .control-item {
                background: white;
                padding: 15px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                background-color: #f5f7fa;
            }
            .dash-table-container {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)