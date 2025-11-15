import requests
import os  
from bs4 import BeautifulSoup
import time
import re
from typing import List, Dict
from dotenv import load_dotenv


load_dotenv()

class VagasScraper:
    """Scraper para vagas de tecnologia usando JSearch API"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        self.rapidapi_key = os.getenv("RAPIDAPI_KEY")
        self.vagas = []
    
    def buscar_jsearch(self, keyword: str = "python", localizacao: str = "Brazil") -> List[Dict]:
        """
        Busca vagas usando JSearch API (LinkedIn, Indeed, Glassdoor, etc)
        """
        vagas = []
        
        try:
            url = "https://jsearch.p.rapidapi.com/search"
            
            # Monta a query - simplificada
            query = f"{keyword}"
            
            querystring = {
                "query": query,
                "page": "1",
                "num_pages": "1"
                # Removido filtro de data para testar
            }
            
            headers = {
                "X-RapidAPI-Key": self.rapidapi_key,
                "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
            }
            
            print(f"🔗 Consultando API com query: '{query}'")
            
            response = requests.get(url, headers=headers, params=querystring, timeout=15)
            
            print(f"📡 Status Code: {response.status_code}")
            
            response.raise_for_status()
            
            data = response.json()
            
            print(f"📦 Resposta da API: {data.get('status', 'N/A')}")
            print(f"📋 Keys na resposta: {list(data.keys())}")
            
            # Debug: mostra o que tem em data
            if 'data' in data:
                print(f"🔍 Tipo de data: {type(data['data'])}")
                print(f"🔍 Length de data: {len(data['data']) if data['data'] else 0}")
                
                # Mostra primeira vaga como exemplo
                if data['data'] and len(data['data']) > 0:
                    print(f"📄 Exemplo primeira vaga keys: {list(data['data'][0].keys())}")
            
            if 'error' in data:
                print(f"❌ Erro da API: {data.get('error')}")
                print(f"   Mensagem: {data.get('message', 'N/A')}")
            
            if data.get('status') == 'OK' and data.get('data') and len(data['data']) > 0:
                print(f"✨ Total de vagas encontradas na API: {len(data['data'])}")
                
                for job in data['data'][:30]:  # Limita a 30 vagas
                    try:
                        vaga = self._extrair_dados_jsearch(job, localizacao)
                        if vaga:
                            vagas.append(vaga)
                    except Exception as e:
                        print(f"Erro ao processar vaga: {e}")
                        continue
            else:
                print(f"⚠️ Array 'data' está vazio ou não existe")
            
            time.sleep(1)
            
        except requests.exceptions.HTTPError as e:
            print(f"❌ Erro HTTP ao buscar no JSearch: {e}")
            if 'response' in locals():
                print(f"   Response: {response.text[:200]}")
        except Exception as e:
            print(f"❌ Erro ao buscar no JSearch: {e}")
        
        return vagas
    
    def _extrair_dados_jsearch(self, job: Dict, filtro_local: str = "") -> Dict:
        """Extrai dados de uma vaga do JSearch"""
        
        # Título
        titulo = job.get('job_title', 'Não informado')
        
        # Empresa
        empresa = job.get('employer_name', 'Não informada')
        
        # Local
        local = job.get('job_city', '')
        if job.get('job_state'):
            local += f", {job.get('job_state')}"
        if job.get('job_country'):
            local += f" - {job.get('job_country')}"
        
        if not local or local == ' - ':
            if job.get('job_is_remote'):
                local = 'Remoto'
            else:
                local = job.get('job_country', 'Não informado')
        
        # Link
        link = job.get('job_apply_link') or job.get('job_google_link', '#')
        
        # Extrai skills da descrição
        descricao = job.get('job_description', '').lower()
        skills = self._extrair_skills(descricao)
        
        # Se não tem skills na descrição, tenta pegar do título
        if not skills:
            skills = self._extrair_skills(titulo.lower())
        
        # Filtro de localização
        if filtro_local and filtro_local.lower() not in local.lower():
            if not (filtro_local.lower() == 'remoto' and job.get('job_is_remote')):
                return None
        
        return {
            'titulo': titulo,
            'empresa': empresa,
            'local': local,
            'skills': skills if skills else ['Python'],  # Garante pelo menos uma skill
            'link': link,
            'fonte': 'JSearch API'
        }
    
        """
        Busca vagas no Programathor
        """
        vagas = []
        
        try:
            # URL de busca do Programathor
            url = f"https://programathor.com.br/jobs?q={keyword}"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Encontra os cards de vagas (ajustar seletores conforme necessário)
            cards_vagas = soup.find_all('div', class_='job-item') or soup.find_all('article')
            
            for card in cards_vagas[:20]:  # Limita a 20 vagas
                try:
                    vaga = self._extrair_dados_programathor(card)
                    
                    # Filtro de localização se especificado
                    if localizacao and localizacao.lower() not in vaga['local'].lower():
                        continue
                    
                    vagas.append(vaga)
                    
                except Exception as e:
                    print(f"Erro ao processar vaga: {e}")
                    continue
            
            time.sleep(1)  # Rate limiting
            
        except Exception as e:
            print(f"Erro ao buscar no Programathor: {e}")
        
        return vagas
    
    def _extrair_dados_programathor(self, card) -> Dict:
        """Extrai dados de um card de vaga"""
        
        # Título
        titulo_elem = card.find('h2') or card.find('h3') or card.find('a', class_='job-title')
        titulo = titulo_elem.get_text(strip=True) if titulo_elem else "Não informado"
        
        # Empresa
        empresa_elem = card.find('span', class_='company') or card.find('div', class_='company-name')
        empresa = empresa_elem.get_text(strip=True) if empresa_elem else "Não informada"
        
        # Local
        local_elem = card.find('span', class_='location') or card.find('div', class_='job-location')
        local = local_elem.get_text(strip=True) if local_elem else "Remoto"
        
        # Link
        link_elem = card.find('a', href=True)
        link = link_elem['href'] if link_elem else "#"
        if link.startswith('/'):
            link = f"https://programathor.com.br{link}"
        
        # Extrai skills do texto completo
        texto_completo = card.get_text().lower()
        skills = self._extrair_skills(texto_completo)
        
        return {
            'titulo': titulo,
            'empresa': empresa,
            'local': local,
            'skills': skills,
            'link': link,
            'fonte': 'Programathor'
        }
    
    def _extrair_skills(self, texto: str) -> List[str]:
        """Extrai skills técnicas do texto"""
        
        skills_conhecidas = [
            'python', 'java', 'javascript', 'typescript', 'react', 'angular', 'vue',
            'node', 'django', 'flask', 'fastapi', 'spring', 'sql', 'postgresql',
            'mysql', 'mongodb', 'redis', 'docker', 'kubernetes', 'aws', 'azure',
            'gcp', 'git', 'api', 'rest', 'graphql', 'machine learning', 'data science',
            'pandas', 'numpy', 'tensorflow', 'pytorch', 'spark', 'hadoop', 'airflow',
            'ci/cd', 'devops', 'agile', 'scrum', 'html', 'css', 'bootstrap', 'tailwind'
        ]
        
        skills_encontradas = []
        for skill in skills_conhecidas:
            if skill in texto:
                skills_encontradas.append(skill.title())
        
        return list(set(skills_encontradas))  # Remove duplicatas
    
    def buscar_vagas(self, keyword: str = "python", localizacao: str = "") -> List[Dict]:
        """
        Método principal que busca em múltiplas fontes
        """
        print(f"🔍 Buscando vagas de '{keyword}' em '{localizacao or 'todas as localidades'}'...")
        
        todas_vagas = []
        
        # JSearch API (LinkedIn, Indeed, Glassdoor)
        try:
            # loc_busca = localizacao if localizacao else "Brazil"
            loc_busca = localizacao 
            vagas_jsearch = self.buscar_jsearch(keyword, loc_busca)
            todas_vagas.extend(vagas_jsearch)
            print(f"✅ Encontradas {len(vagas_jsearch)} vagas no JSearch")
        except Exception as e:
            print(f"⚠️ JSearch indisponível: {e}")
        
        # Se não encontrou nada na API, usa dados de exemplo
        if not todas_vagas:
            print("ℹ️ Gerando vagas de exemplo para demonstração...")
            todas_vagas = self._gerar_vagas_exemplo(keyword, localizacao)
        
        # Remove duplicatas baseado no título e empresa
        vagas_unicas = self._remover_duplicatas(todas_vagas)
        
        print(f"📊 Total: {len(vagas_unicas)} vagas únicas encontradas")
        
        return vagas_unicas
    
    def _gerar_vagas_exemplo(self, keyword: str, localizacao: str) -> List[Dict]:
        """Gera vagas de exemplo para demonstração do projeto"""
        
        empresas = ['Tech Corp', 'Data Inc', 'Cloud Solutions', 'AI Labs', 'Dev Team', 
                   'Digital Innovations', 'Software House', 'StartupX']
        locais = ['São Paulo - SP', 'Rio de Janeiro - RJ', 'Remoto', 'Belo Horizonte - MG',
                 'Curitiba - PR', 'Porto Alegre - RS', 'Brasília - DF', 'Florianópolis - SC']
        
        cargos_python = [
            'Desenvolvedor Python Pleno',
            'Engenheiro de Dados Python',
            'Python Backend Developer',
            'Desenvolvedor Python Sênior',
            'Data Scientist Python',
            'Python Full Stack Developer',
            'Analista de Dados Python',
            'DevOps Python Engineer'
        ]
        
        skills_python = [
            ['Python', 'Django', 'PostgreSQL', 'Docker', 'API'],
            ['Python', 'Pandas', 'SQL', 'AWS', 'Machine Learning'],
            ['Python', 'Flask', 'MongoDB', 'Redis', 'Git'],
            ['Python', 'FastAPI', 'Docker', 'Kubernetes', 'CI/CD'],
            ['Python', 'TensorFlow', 'PyTorch', 'SQL', 'Spark'],
            ['Python', 'React', 'Node', 'PostgreSQL', 'Docker'],
            ['Python', 'Pandas', 'Matplotlib', 'SQL', 'Excel'],
            ['Python', 'Terraform', 'AWS', 'Jenkins', 'Linux']
        ]
        
        vagas = []
        import random
        
        for i in range(15):
            idx = i % len(cargos_python)
            vaga = {
                'titulo': cargos_python[idx],
                'empresa': random.choice(empresas),
                'local': random.choice(locais) if not localizacao else localizacao,
                'skills': skills_python[idx],
                'link': f'https://exemplo.com/vaga-{i+1}',
                'fonte': 'Demonstração'
            }
            
            # Filtra por localização se especificado
            if localizacao and localizacao.lower() not in vaga['local'].lower():
                continue
                
            vagas.append(vaga)
        
        return vagas
    
    def _remover_duplicatas(self, vagas: List[Dict]) -> List[Dict]:
        """Remove vagas duplicadas"""
        vistas = set()
        unicas = []
        
        for vaga in vagas:
            chave = (vaga['titulo'].lower(), vaga['empresa'].lower())
            if chave not in vistas:
                vistas.add(chave)
                unicas.append(vaga)
        
        return unicas


# Teste rápido
if __name__ == "__main__":
    scraper = VagasScraper()
    vagas = scraper.buscar_vagas("python", "")

    print(f"Total vagas encontradas: {len(vagas)}")
    
    print(f"\n📋 Primeiras 3 vagas encontradas:\n")
    for i, vaga in enumerate(vagas[:3], 1):
        print(f"{i}. {vaga['titulo']} - {vaga['empresa']}")
        print(f"   📍 {vaga['local']}")
        print(f"   🔧 Skills: {', '.join(vaga['skills'][:5])}")
        print()