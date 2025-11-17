# 💼 Tech Jobs Aggregator

Agregador de vagas de tecnologia com análise automática de skills e visualizações interativas.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🎯 Funcionalidades

- 🔍 Busca automática de vagas em múltiplas plataformas
- 📊 Análise de skills mais demandadas
- 📍 Distribuição geográfica de vagas
- 🏢 Empresas que mais contratam
- 💾 Exportação para CSV
- 🎨 Interface web interativa

## 🚀 Como Usar
### Teste Online
[vagas-tech.streamlit.app](https://vagas-tech.streamlit.app/)

1. **Clone o repositório**
```bash
[vagas-tech.streamlit.app](https://vagas-tech.streamlit.app/)
cd vagas-tech
```

### Instalação Local

1. **Clone o repositório**
```bash
git clone https://github.com/felippemcc/vagas-tech.git
cd vagas-tech
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Execute o app**
```bash
streamlit run app.py
```

5. **Acesse no navegador**
```
http://localhost:8501
```

## 📦 Estrutura do Projeto

```
vagas-tech/
├── scraper.py      # Lógica de web scraping
├── analyzer.py     # Análise de dados
├── app.py          # Interface Streamlit
├── requirements.txt
└── README.md
```

## 🛠️ Tecnologias

- **Python 3.8+**
- **Streamlit** - Interface web
- **BeautifulSoup4** - Web scraping
- **Pandas** - Análise de dados
- **Plotly** - Visualizações interativas

## 📊 Fontes de Dados

Atualmente coletando de:
- Programathor
- *(mais fontes em breve)*

## 🎨 Screenshots

*Em breve*

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se livre para:
- Reportar bugs
- Sugerir novas features
- Adicionar novos scrapers
- Melhorar a documentação

## 📝 Licença

Este projeto está sob a licença MIT.

## 👨‍💻 Autor

**Felippe Moura**
- GitHub: [@felippemcc](https://github.com/felippemcc)
- LinkedIn: [Felippe Moura](https://www.linkedin.com/in/felippemoura/)

---

⭐ Se este projeto te ajudou, considere dar uma estrela!
