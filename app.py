import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from scraper import VagasScraper
from analyzer import VagasAnalyzer
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="Tech Jobs Aggregator",
    page_icon="💼",
    layout="wide"
)

# Título e descrição
st.title("💼 Agregador de Vagas Tech")
st.markdown("""
Busque vagas de tecnologia em múltiplas plataformas e veja análises em tempo real!
""")

# Sidebar com filtros
st.sidebar.header("🔍 Filtros de Busca")

keyword = st.sidebar.text_input(
    "Palavra-chave",
    value="python",
    help="Ex: python, data science, react, etc."
)

localizacao = st.sidebar.text_input(
    "Localização (opcional)",
    value="",
    help="Ex: São Paulo, Remoto, Rio de Janeiro"
)

buscar_btn = st.sidebar.button("🚀 Buscar Vagas", type="primary", use_container_width=True)

# Inicializa session state
if 'vagas' not in st.session_state:
    st.session_state.vagas = []
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = None

# Lógica de busca
if buscar_btn:
    with st.spinner("🔎 Buscando vagas..."):
        scraper = VagasScraper()
        st.session_state.vagas = scraper.buscar_vagas(keyword, localizacao)
        
        if st.session_state.vagas:
            st.session_state.analyzer = VagasAnalyzer(st.session_state.vagas)
            st.success(f"✅ {len(st.session_state.vagas)} vagas encontradas!")
        else:
            st.warning("⚠️ Nenhuma vaga encontrada. Tente outros termos de busca.")

# Exibe resultados se houver vagas
if st.session_state.vagas and st.session_state.analyzer:
    analyzer = st.session_state.analyzer
    
    # Métricas principais
    st.markdown("---")
    st.subheader("📊 Visão Geral")
    
    stats = analyzer.get_estatisticas()
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Vagas", stats['total_vagas'])
    with col2:
        st.metric("Empresas", stats['total_empresas'])
    with col3:
        st.metric("Localidades", stats['total_locais'])
    with col4:
        st.metric("Top Skill", stats['skill_mais_demandada'])
    
    # Gráficos
    st.markdown("---")
    
    col_graficos1, col_graficos2 = st.columns(2)
    
    with col_graficos1:
        st.subheader("🔧 Skills Mais Demandadas")
        df_skills = analyzer.get_top_skills(10)
        
        if not df_skills.empty:
            fig_skills = px.bar(
                df_skills,
                x='Quantidade',
                y='Skill',
                orientation='h',
                color='Quantidade',
                color_continuous_scale='Blues',
                text='Quantidade'
            )
            fig_skills.update_layout(
                showlegend=False,
                height=400,
                yaxis={'categoryorder': 'total ascending'}
            )
            fig_skills.update_traces(textposition='outside')
            st.plotly_chart(fig_skills, use_container_width=True)
        else:
            st.info("Nenhuma skill identificada")
    
    with col_graficos2:
        st.subheader("📍 Vagas por Localização")
        df_local = analyzer.get_vagas_por_local()
        
        if not df_local.empty:
            fig_local = px.pie(
                df_local,
                values='Quantidade',
                names='Local',
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_local.update_layout(height=400)
            st.plotly_chart(fig_local, use_container_width=True)
        else:
            st.info("Nenhuma localização identificada")
    
    # Top Empresas
    st.markdown("---")
    st.subheader("🏢 Empresas com Mais Vagas")
    df_empresas = analyzer.get_vagas_por_empresa(8)
    
    if not df_empresas.empty:
        fig_empresas = go.Figure(data=[
            go.Bar(
                x=df_empresas['Empresa'],
                y=df_empresas['Quantidade'],
                marker_color='lightblue',
                text=df_empresas['Quantidade'],
                textposition='outside'
            )
        ])
        fig_empresas.update_layout(
            xaxis_title="Empresa",
            yaxis_title="Quantidade de Vagas",
            height=400,
            showlegend=False
        )
        st.plotly_chart(fig_empresas, use_container_width=True)
    
    # Tabela de vagas
    st.markdown("---")
    st.subheader("📋 Todas as Vagas Encontradas")
    
    df_display = analyzer.get_dataframe().copy()
    df_display['skills'] = df_display['skills'].apply(lambda x: ', '.join(x[:5]))  # Mostra até 5 skills
    df_display['link'] = df_display['link'].apply(lambda x: f'<a href="{x}" target="_blank">Ver vaga</a>')
    
    # Exibe tabela
    st.dataframe(
        df_display[['titulo', 'empresa', 'local', 'skills', 'fonte']],
        use_container_width=True,
        height=400
    )
    
    # Botão de download
    st.markdown("---")
    col_download1, col_download2 = st.columns([3, 1])
    
    with col_download2:
        # Prepara CSV para download
        df_export = analyzer.get_dataframe().copy()
        df_export['skills'] = df_export['skills'].apply(lambda x: ', '.join(x))
        csv = df_export.to_csv(index=False, encoding='utf-8-sig')
        
        st.download_button(
            label="📥 Baixar CSV",
            data=csv,
            file_name=f"vagas_{keyword}.csv",
            mime="text/csv",
            use_container_width=True
        )

else:
    # Mensagem inicial
    st.info("👈 Use os filtros na barra lateral e clique em 'Buscar Vagas' para começar!")
    
    # Informações sobre o projeto
    st.markdown("---")
    st.markdown("""
    ### 🎯 Como funciona?
    
    1. **Digite** a palavra-chave (ex: python, react, data science)
    2. **Adicione** uma localização (opcional)
    3. **Clique** em "Buscar Vagas"
    4. **Veja** análises automáticas e baixe os resultados!
    
    ### 📊 O que você verá?
    - Total de vagas encontradas
    - Skills mais demandadas
    - Distribuição por localização
    - Empresas que mais contratam
    - Lista completa com links
    
    ### 💡 Dicas
    - Use termos simples como "python", "java", "react"
    - Para localização, use "Remoto" ou nome da cidade
    - Você pode baixar os resultados em CSV
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    Desenvolvido com ❤️ por Felippe | 
    <a href='https://github.com/felippemcc' target='_blank'>GitHub</a>
</div>
""", unsafe_allow_html=True)