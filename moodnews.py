import streamlit as st
import requests
from textblob import TextBlob
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from deep_translator import GoogleTranslator

# SETCONFIG
st.set_page_config(page_title="MoodNews Pro", page_icon="⚡", layout="wide")

API_KEY = st.secrets["API_KEY"] #La API_KEY debe verse así para correrlo local ---> API_KEY = 'TU APIKEY'

# MEMORY
if 'favoritos' not in st.session_state: st.session_state.favoritos = []
if 'resultados' not in st.session_state: st.session_state.resultados = None
if 'query_activa' not in st.session_state: st.session_state.query_activa = ""
if 'q_display' not in st.session_state: st.session_state.q_display = ""
if 'auto_run' not in st.session_state: st.session_state.auto_run = False
if 'busqueda_input' not in st.session_state: st.session_state.busqueda_input = ""

# EVENTS
def handle_modo_change():
    st.session_state.busqueda_input = ""
    if st.session_state.modo == "Categoría":
        st.session_state.auto_run = True
    else:
        st.session_state.resultados = None
        st.session_state.query_activa = ""
        st.session_state.q_display = ""

def handle_cat_change():
    st.session_state.busqueda_input = ""
    st.session_state.auto_run = True

# CORE FUNTION
def traducir(texto, dest='en'):
    try: 
        if not texto: return ""
        return GoogleTranslator(source='auto', target=dest).translate(texto)
    except: return texto

def obtener_fiabilidad(fuente):
    reputacion = {
        "Reuters": (98, "🥇 Alta"), "BBC News": (98, "🥇 Alta"), "The Verge": (95, "🥈 Confiable"),
        "Wired": (92, "🥈 Confiable"), "TechCrunch": (90, "🥈 Confiable"), "Kotaku": (80, "🥉 Media")
    }
    return reputacion.get(fuente, (70, "🔘 Sin verificar"))

# BARRA LATERAL
with st.sidebar:
    st.markdown("<h2 style='color: #58a6ff;'>🧠 Intelligence Hub</h2>", unsafe_allow_html=True)
    
    st.radio("Método de búsqueda:", ["Personalizado", "Categoría"], key="modo", on_change=handle_modo_change)
    
    if st.session_state.modo == "Categoría":
        st.selectbox("Sector:", ["Technology", "Gaming", "Business", "Science"], key="cat_f", on_change=handle_cat_change)
    
    st.markdown("---")
    st.subheader("⭐ Mis Favoritos")
    
    if st.session_state.favoritos:
        for idx, fav in enumerate(st.session_state.favoritos):
            c1, c2 = st.columns([5, 1])
            with c1:
                st.markdown(f"[{fav['fuente']}: {fav['titulo'][:25]}...]({fav['url']})")
            with c2:
                if st.button("🗑️", key=f"del_{idx}"):
                    st.session_state.favoritos.pop(idx)
                    st.rerun()
    else:
        st.info("No tienes ninguna noticia favorita  :C.")

# BODY
st.markdown("<h1 style='text-align: center; color: #58a6ff; font-size: 60px;'>MoodNews</h1>", unsafe_allow_html=True)

# SEARCH
c_in, c_btn = st.columns([10, 1])
with c_in:
    busqueda_usuario = st.text_input("", placeholder="Escribe tu tema y presiona Enter...", label_visibility="collapsed", key="busqueda_input")
with c_btn:
    ejecutar = st.button("🔍", use_container_width=True)

# MOTOR DE BUSQUEDA LOGICO
run_search = False
q_base = ""

if ejecutar or (busqueda_usuario and busqueda_usuario != st.session_state.query_activa):
    run_search = True
    q_base = busqueda_usuario
    st.session_state.auto_run = False
    
elif st.session_state.auto_run:
    run_search = True
    q_base = st.session_state.cat_f if st.session_state.modo == "Categoría" else ""
    st.session_state.auto_run = False

if run_search and q_base:
    if st.session_state.modo == "Categoría":
        if q_base == st.session_state.cat_f:
            q_final = st.session_state.cat_f 
        else:
            q_final = f"{q_base} {st.session_state.cat_f}".strip() 
    else:
        q_final = q_base

    with st.status("🚀 Procesando inteligencia global...", expanded=True) as status:
        q_en = traducir(q_final, 'en')
        url = f'https://newsapi.org/v2/everything?q={q_en}&sortBy=popularity&language=en&pageSize=15&apiKey={API_KEY}'
        
        try:
            res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).json()
            
            if res.get('articles'):
                st.session_state.resultados = [{
                    "Noticia": traducir(art['title'], 'es'),
                    "Resumen": traducir(art['description'], 'es'),
                    "Impacto": round((TextBlob(art['title']).sentiment.polarity + 1) * 50, 1),
                    "Fuente": art['source']['name'],
                    "URL": art['url'],
                    "Veracidad": obtener_fiabilidad(art['source']['name'])[1]
                } for art in res['articles']]
                
                st.session_state.query_activa = busqueda_usuario 
                st.session_state.q_display = q_final 
                status.update(label="✅ Análisis Completado", state="complete", expanded=False)
            else:
                st.session_state.resultados = []
                status.update(label="❌ Sin resultados", state="error", expanded=False)
        except Exception as e:
            st.session_state.resultados = []
            status.update(label="❌ Error de conexión", state="error", expanded=False)

# RESPUESTA VISUAL DE DATOS
if st.session_state.resultados:
    df = pd.DataFrame(st.session_state.resultados)
    promedio = df["Impacto"].mean()

    st.markdown(f"""<div style="background:#161b22;padding:20px;border-radius:15px;border-left:10px solid #58a6ff;margin-bottom:20px;">
        <h2 style="margin:0;">Mood: {promedio:.1f}/100</h2>
        <p style="color:#8b949e;">Basado en las noticias más recientes y populares sobre: <b>{st.session_state.q_display.upper()}</b></p>
    </div>""", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        df_g = df.groupby("Fuente")["Impacto"].mean().reset_index()
        fig = go.Figure(data=go.Scatterpolar(r=df_g['Impacto'], theta=df_g['Fuente'], fill='toself', line_color='#58a6ff'))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), title="Mapa de Sentimiento", paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig_pie = px.pie(df, names='Fuente', hole=0.5, title="Cuota de Voz")
        fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader("📰 Inteligencia de Titulares")
    for i, row in df.iterrows():
        col_t, col_f = st.columns([9, 1])
        with col_t:
            with st.expander(f"{row['Impacto']} pts | {row['Veracidad']} | {row['Noticia']}"):
                st.write(f"**Fuente:** {row['Fuente']} | **Resumen:** _{row['Resumen']}_")
                st.link_button("Leer noticia original", row['URL'])
        with col_f:
            if st.button("⭐", key=f"fav_{i}"):
                nuevo = {"titulo": row['Noticia'], "fuente": row['Fuente'], "url": row['URL']}
                if nuevo not in st.session_state.favoritos:
                    st.session_state.favoritos.append(nuevo)
                    st.toast(f"¡Guardado: {row['Fuente']}!")
                    st.rerun()

elif st.session_state.resultados == []:
    st.warning("No se hallaron resultados para esta configuración.")

