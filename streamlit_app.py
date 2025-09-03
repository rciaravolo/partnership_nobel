import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import warnings
import hashlib

# Configuração da página
st.set_page_config(
    page_title="Matriz de Partnership",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Usuários válidos
VALID_USERS = {
    'vitor.baqueiro': {'password': 'Nobelpartnership2025', 'role': 'lider'},  
    'marco.silveira': {'password': 'Nobelpartnership2025', 'role': 'lider'},    
    'viviane.fabbri': {'password': 'Nobelpartnership2025', 'role': 'lider'},
    'bruna.yendo': {'password': 'Nobelpartnership2025', 'role': 'lider'},
    'rafael.bonfim': {'password': 'Nobelpartnership2025', 'role': 'lider'},
    'carlos.corvelloni': {'password': 'Nobelpartnership2025', 'role': 'lider'}
}

def carregar_dados_limpo(arquivo):
    """Carrega e limpa os dados do Excel"""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            df = pd.read_excel(arquivo)
            df.columns = ['Funcionario', 'Pontuacao', 'Quadrante', 'Equipe'] 
            return df.dropna()
        except FileNotFoundError:
            # Dados de exemplo se arquivo não encontrado
            return pd.DataFrame({
                'Funcionario': ['João Silva', 'Maria Santos', 'Pedro Costa', 'Ana Lima', 'Carlos Souza'],
                'Pontuacao': [85, 45, 72, 38, 91],
                'Quadrante': ['Ganho de Equity', 'Manutenção', 'Opção de Compra', 'Diluição', 'Ganho de Equity'],
                'Equipe': ['Vendas', 'Marketing', 'Vendas', 'Marketing', 'Vendas']
            })

def authenticate_user(username, password):
    """Autentica usuário"""
    if username in VALID_USERS:
        if VALID_USERS[username]['password'] == password:
            return True
    return False

def create_scatter_plot(df_filtrado):
    """Cria o gráfico scatter da matriz"""
    cores_quadrantes = {
        'Diluição': '#E74C3C',
        'Manutenção': '#F39C12',
        'Opção de Compra': '#3498DB',
        'Ganho de Equity': '#27AE60'
    }
    
    fig = go.Figure()
    
    # Adicionar faixas de fundo
    fig.add_shape(type="rect", x0=0, y0=-0.5, x1=40, y1=0.5,
                 fillcolor='rgba(231, 76, 60, 0.1)', line=dict(width=0))
    fig.add_shape(type="rect", x0=40, y0=-0.5, x1=60, y1=0.5,
                 fillcolor='rgba(243, 156, 18, 0.1)', line=dict(width=0))
    fig.add_shape(type="rect", x0=60, y0=-0.5, x1=80, y1=0.5,
                 fillcolor='rgba(52, 152, 219, 0.1)', line=dict(width=0))
    fig.add_shape(type="rect", x0=80, y0=-0.5, x1=100, y1=0.5,
                 fillcolor='rgba(39, 174, 96, 0.1)', line=dict(width=0))
    
    # Adicionar pontos por quadrante
    for quadrante in df_filtrado['Quadrante'].unique():
        subset = df_filtrado[df_filtrado['Quadrante'] == quadrante]
        fig.add_trace(go.Scatter(
            x=subset['Pontuacao'],
            y=[0] * len(subset),
            mode='markers',
            marker=dict(size=15, color=cores_quadrantes[quadrante], 
                       line=dict(width=2, color='white')),
            name=quadrante,
            text=subset['Funcionario'],
            hovertemplate="<b>%{text}</b><br>" +
                         "Pontuação: %{x:.2f}<br>" +
                         f"Quadrante: {quadrante}<br>" +
                         "Equipe: %{customdata}<br>" +
                         "<extra></extra>",
            customdata=subset['Equipe']
        ))
    
    # Linhas divisórias
    for linha in [40, 60, 80]:
        fig.add_vline(x=linha, line_width=3, line_dash="dash", line_color="rgba(44, 62, 80, 0.8)")
    
    # Labels dos quadrantes
    labels = [
        (20, "DILUIÇÃO\n(0-40)", cores_quadrantes['Diluição']),
        (50, "MANUTENÇÃO\n(40-60)", cores_quadrantes['Manutenção']),
        (70, "OPÇÃO DE COMPRA\n(60-80)", cores_quadrantes['Opção de Compra']),
        (90, "GANHO DE EQUITY\n(80-100)", cores_quadrantes['Ganho de Equity'])
    ]
    
    for x, label, cor in labels:
        fig.add_annotation(x=x, y=0.3, text=label, showarrow=False,
                         font=dict(size=12, color='white'), 
                         bgcolor=cor, bordercolor=cor, borderwidth=2)
    
    fig.update_layout(
        title=dict(text="🎯 Matriz de Partnership", font=dict(size=20), x=0.5),
        xaxis=dict(title="Pontuação (0-100)", range=[-5, 105]),
        yaxis=dict(visible=False, range=[-0.5, 0.5]),
        height=500,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig

def main():
    # Inicializar estado da sessão
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'username' not in st.session_state:
        st.session_state.username = ""

    # Página de login
    if not st.session_state.authenticated:
        st.markdown("""
        <div style='text-align: center; padding: 50px;'>
            <h1>🔒 MATRIZ DE PARTNERSHIP</h1>
            <h3 style='color: #7F8C8D;'>Acesso Restrito - Lideranças</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            with st.form("login_form"):
                st.subheader("Login")
                username = st.text_input("Usuário:")
                password = st.text_input("Senha:", type="password")
                submit = st.form_submit_button("Entrar")
                
                if submit:
                    if authenticate_user(username, password):
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.rerun()
                    else:
                        st.error("❌ Usuário ou senha incorretos")
                
                # Mostrar usuários disponíveis
                st.markdown("---")
                st.markdown("**Usuários Disponíveis:**")
                for user in VALID_USERS.keys():
                    st.markdown(f"• {user}")
        return

    # Dashboard principal (usuário autenticado)
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🔒 MATRIZ DE PARTNERSHIP")
    with col2:
        st.markdown(f"**👤 {st.session_state.username}**")
        if st.button("Sair"):
            st.session_state.authenticated = False
            st.session_state.username = ""
            st.rerun()
    
    st.markdown("---")
    
    # Carregar dados
    df = carregar_dados_limpo('partnership.xlsx')
    
    # Controles de filtro
    col1, col2, col3 = st.columns(3)
    
    with col1:
        quadrante_selecionado = st.selectbox(
            "Filtrar por Quadrante:",
            ['Todos'] + list(df['Quadrante'].unique())
        )
    
    with col2:
        equipe_selecionada = st.selectbox(
            "Equipe:",
            ['Todos'] + list(df['Equipe'].unique())
        )
    
    with col3:
        faixa_pontuacao = st.slider(
            "Faixa de Pontuação:",
            min_value=0,
            max_value=100,
            value=(0, 100),
            step=5
        )
    
    # Filtrar dados
    df_filtrado = df.copy()
    
    if quadrante_selecionado != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['Quadrante'] == quadrante_selecionado]
    
    if equipe_selecionada != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['Equipe'] == equipe_selecionada]
    
    df_filtrado = df_filtrado[
        (df_filtrado['Pontuacao'] >= faixa_pontuacao[0]) & 
        (df_filtrado['Pontuacao'] <= faixa_pontuacao[1])
    ]
    
    # Gráfico principal
    fig = create_scatter_plot(df_filtrado)
    st.plotly_chart(fig, use_container_width=True)
    
    # KPIs
    st.markdown("### 📊 Indicadores")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_assessores = len(df_filtrado)
    distribuicao = df_filtrado['Quadrante'].value_counts()
    media_pontuacao = df_filtrado['Pontuacao'].mean() if len(df_filtrado) > 0 else 0
    
    with col1:
        st.metric("Total Assessores", total_assessores)
    
    with col2:
        st.metric("Pontuação Média", f"{media_pontuacao:.2f}")
    
    with col3:
        st.metric("Alto Desempenho", distribuicao.get('Ganho de Equity', 0))
    
    with col4:
        st.metric("Necessita Atenção", distribuicao.get('Diluição', 0))
    
    # Tabela detalhada
    st.markdown("### 📋 Detalhamento por Assessor")
    
    # Aplicar cores na tabela baseado no quadrante
    def color_quadrante(val):
        colors = {
            'Diluição': 'background-color: #FADBD8',
            'Manutenção': 'background-color: #FCF3CF',
            'Opção de Compra': 'background-color: #EBF5FB',
            'Ganho de Equity': 'background-color: #E8F6F3'
        }
        return colors.get(val, '')
    
    styled_df = df_filtrado.style.applymap(color_quadrante, subset=['Quadrante'])
    st.dataframe(styled_df, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: #E74C3C; font-weight: bold;'>"
        "⚠️ CONFIDENCIAL - Dashboard executivo com acesso restrito"
        "</p>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
