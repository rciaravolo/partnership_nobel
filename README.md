# 🔒 Dashboard Seguro - Matriz de Partnership

Dashboard executivo com sistema de autenticação e autorização para visualização de dados de performance de assessores.

## 🚀 Funcionalidades

- **Autenticação Segura**: Sistema de login com hash de senhas
- **Controle de Acesso**: Diferentes níveis de usuário (Admin, Líder, Diretor)
- **Sessões Seguras**: Controle de sessão com timeout automático
- **Dashboard Interativo**: Visualização da matriz de partnership
- **Filtros Avançados**: Por quadrante, equipe e faixa de pontuação


## 🛠️ Instalação

1. **Clone o projeto:**
```bash
cd C:\Users\Usuario\CascadeProjects\secure-dashboard
```

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Configure as variáveis de ambiente:**
   - Copie `.env` e ajuste as configurações
   - **IMPORTANTE**: Altere `SECRET_KEY` em produção

4. **Execute a aplicação:**
```bash
python secure_main.py
```

## 🌐 Deploy Online

### Heroku
```bash
git init
git add .
git commit -m "Initial commit"
heroku create seu-app-name
git push heroku main
```

### Render/Railway
- Faça upload dos arquivos
- Configure as variáveis de ambiente
- Deploy automático

## 🔐 Segurança Implementada

- **Hash de Senhas**: PBKDF2 com salt
- **Sessões Seguras**: Tokens únicos com expiração
- **Banco de Dados**: SQLite com controle de usuários
- **Autorização**: Verificação de níveis de acesso
- **HTTPS Ready**: Configurado para produção

## 📊 Dados

O dashboard espera um arquivo `partnership.xlsx` com as colunas:
- Assessor
- Pontuacao
- Quadrante
- Equipe

Se o arquivo não existir, dados de exemplo serão carregados.

## ⚠️ Importante

- Altere todas as senhas padrão em produção
- Configure `SECRET_KEY` única
- Use HTTPS em produção
- Monitore logs de acesso
