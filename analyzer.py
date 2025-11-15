import pandas as pd
from typing import List, Dict
from collections import Counter

class VagasAnalyzer:
    """Analisa dados das vagas coletadas"""
    
    def __init__(self, vagas: List[Dict]):
        self.vagas = vagas
        self.df = self._criar_dataframe()
    
    def _criar_dataframe(self) -> pd.DataFrame:
        """Converte lista de vagas em DataFrame"""
        if not self.vagas:
            return pd.DataFrame()
        
        df = pd.DataFrame(self.vagas)
        return df
    
    def get_top_skills(self, top_n: int = 15) -> pd.DataFrame:
        """Retorna as skills mais demandadas"""
        if self.df.empty:
            return pd.DataFrame(columns=['Skill', 'Quantidade'])
        
        # Flatten all skills into a single list
        todas_skills = []
        for skills_list in self.df['skills']:
            todas_skills.extend(skills_list)
        
        # Count occurrences
        skill_counts = Counter(todas_skills)
        top_skills = skill_counts.most_common(top_n)
        
        df_skills = pd.DataFrame(top_skills, columns=['Skill', 'Quantidade'])
        return df_skills
    
    def get_vagas_por_local(self) -> pd.DataFrame:
        """Retorna quantidade de vagas por localização"""
        if self.df.empty:
            return pd.DataFrame(columns=['Local', 'Quantidade'])
        
        # Normaliza localizações
        df_local = self.df.copy()
        df_local['local_normalizado'] = df_local['local'].apply(self._normalizar_local)
        
        vagas_local = df_local['local_normalizado'].value_counts().reset_index()
        vagas_local.columns = ['Local', 'Quantidade']
        
        return vagas_local.head(10)
    
    def _normalizar_local(self, local: str) -> str:
        """Normaliza nomes de localização"""
        local = local.lower()
        
        # Mapeamento de normalizações
        if 'remoto' in local or 'remote' in local or 'home office' in local:
            return 'Remoto'
        elif 'são paulo' in local or 'sp' in local:
            return 'São Paulo'
        elif 'rio de janeiro' in local or 'rj' in local:
            return 'Rio de Janeiro'
        elif 'belo horizonte' in local or 'bh' in local:
            return 'Belo Horizonte'
        elif 'brasília' in local or 'df' in local:
            return 'Brasília'
        elif 'curitiba' in local:
            return 'Curitiba'
        elif 'porto alegre' in local:
            return 'Porto Alegre'
        elif 'florianópolis' in local:
            return 'Florianópolis'
        else:
            return local.title()
    
    def get_vagas_por_empresa(self, top_n: int = 10) -> pd.DataFrame:
        """Retorna empresas com mais vagas"""
        if self.df.empty:
            return pd.DataFrame(columns=['Empresa', 'Quantidade'])
        
        vagas_empresa = self.df['empresa'].value_counts().reset_index()
        vagas_empresa.columns = ['Empresa', 'Quantidade']
        
        return vagas_empresa.head(top_n)
    
    def get_estatisticas(self) -> Dict:
        """Retorna estatísticas gerais"""
        if self.df.empty:
            return {
                'total_vagas': 0,
                'total_empresas': 0,
                'total_locais': 0,
                'skill_mais_demandada': 'N/A'
            }
        
        top_skills = self.get_top_skills(1)
        skill_top = top_skills.iloc[0]['Skill'] if not top_skills.empty else 'N/A'
        
        return {
            'total_vagas': len(self.df),
            'total_empresas': self.df['empresa'].nunique(),
            'total_locais': self.df['local'].nunique(),
            'skill_mais_demandada': skill_top
        }
    
    def exportar_csv(self, caminho: str = "vagas_tech.csv"):
        """Exporta dados para CSV"""
        if self.df.empty:
            print("⚠️ Nenhuma vaga para exportar")
            return
        
        # Converte lista de skills para string
        df_export = self.df.copy()
        df_export['skills'] = df_export['skills'].apply(lambda x: ', '.join(x))
        
        df_export.to_csv(caminho, index=False, encoding='utf-8-sig')
        print(f"✅ Dados exportados para {caminho}")
    
    def get_dataframe(self) -> pd.DataFrame:
        """Retorna o DataFrame completo"""
        return self.df


# Teste rápido
if __name__ == "__main__":
    # Dados de exemplo
    vagas_exemplo = [
        {
            'titulo': 'Desenvolvedor Python',
            'empresa': 'Tech Corp',
            'local': 'São Paulo - SP',
            'skills': ['Python', 'Django', 'PostgreSQL'],
            'link': 'https://exemplo.com',
            'fonte': 'Programathor'
        },
        {
            'titulo': 'Data Scientist',
            'empresa': 'Data Inc',
            'local': 'Remoto',
            'skills': ['Python', 'Machine Learning', 'Pandas'],
            'link': 'https://exemplo.com',
            'fonte': 'Programathor'
        }
    ]
    
    analyzer = VagasAnalyzer(vagas_exemplo)
    
    print("📊 Estatísticas:")
    print(analyzer.get_estatisticas())
    
    print("\n🔧 Top Skills:")
    print(analyzer.get_top_skills())