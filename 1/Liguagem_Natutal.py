# Nome: Sérgio Ornellas Violante Junior
# Curso:Inteligência Artificial
# Disciplina:Classificação e Predição
# Unidade 4 Atividade 5  

import re
import string
from collections import Counter
from typing import List, Dict, Set

class TokenizadorNLP:
    """
    Tokenizador básico para processamento de linguagem natural em português
    """
    
    def __init__(self):
        # Palavras vazias comuns em português
        self.stop_words = {
            'a', 'à', 'ao', 'aos', 'as', 'às', 'da', 'das', 'de', 'do', 'dos',
            'e', 'em', 'na', 'nas', 'no', 'nos', 'o', 'os', 'ou', 'por', 'para',
            'que', 'se', 'com', 'como', 'mais', 'mas', 'não', 'muito', 'bem',
            'já', 'só', 'ainda', 'também', 'quando', 'onde', 'um', 'uma', 'uns',
            'umas', 'esse', 'essa', 'esses', 'essas', 'este', 'esta', 'estes',
            'estas', 'aquele', 'aquela', 'aqueles', 'aquelas', 'seu', 'sua',
            'seus', 'suas', 'meu', 'minha', 'meus', 'minhas', 'nosso', 'nossa',
            'nossos', 'nossas', 'ele', 'ela', 'eles', 'elas', 'eu', 'tu', 'você',
            'vocês', 'nós', 'me', 'te', 'se', 'nos', 'lhe', 'lhes', 'o', 'a',
            'os', 'as', 'lo', 'la', 'los', 'las', 'sim', 'até', 'foi', 'ser',
            'estar', 'ter', 'haver', 'ir', 'vir', 'dar', 'fazer', 'dizer',
            'pode', 'podem', 'deve', 'devem', 'vai', 'vão', 'fica', 'ficam'
        }
        
        # Contrações comuns em português
        self.contracoes = {
            'do': ['de', 'o'],
            'da': ['de', 'a'],
            'dos': ['de', 'os'],
            'das': ['de', 'as'],
            'no': ['em', 'o'],
            'na': ['em', 'a'],
            'nos': ['em', 'os'],
            'nas': ['em', 'as'],
            'ao': ['a', 'o'],
            'aos': ['a', 'os'],
            'às': ['a', 'as'],
            'pelo': ['por', 'o'],
            'pela': ['por', 'a'],
            'pelos': ['por', 'os'],
            'pelas': ['por', 'as'],
            'dum': ['de', 'um'],
            'duma': ['de', 'uma'],
            'duns': ['de', 'uns'],
            'dumas': ['de', 'umas'],
            'num': ['em', 'um'],
            'numa': ['em', 'uma'],
            'nuns': ['em', 'uns'],
            'numas': ['em', 'umas']
        }
    
    def limpar_texto(self, texto: str) -> str:
        """Remove caracteres especiais e normaliza o texto"""
        # Converte para minúsculas
        texto = texto.lower()
        
        # Remove URLs
        texto = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', texto)
        
        # Remove menções (@usuario)
        texto = re.sub(r'@\w+', '', texto)
        
        # Remove hashtags (#tag)
        texto = re.sub(r'#\w+', '', texto)
        
        # Remove números isolados
        texto = re.sub(r'\b\d+\b', '', texto)
        
        # Remove caracteres especiais, mantendo espaços e alguns sinais de pontuação
        texto = re.sub(r'[^\w\s.,!?;:-]', '', texto)
        
        # Remove espaços extras
        texto = re.sub(r'\s+', ' ', texto).strip()
        
        return texto
    
    def tokenizar_sentencas(self, texto: str) -> List[str]:
        """Divide o texto em sentenças"""
        # Pattern para divisão de sentenças
        pattern = r'[.!?]+\s+'
        sentencas = re.split(pattern, texto)
        
        # Remove sentenças vazias e muito curtas
        sentencas = [s.strip() for s in sentencas if len(s.strip()) > 3]
        
        return sentencas
    
    def tokenizar_palavras(self, texto: str) -> List[str]:
        """Divide o texto em palavras (tokens)"""
        # Limpa o texto
        texto_limpo = self.limpar_texto(texto)
        
        # Tokenização básica por espaços e pontuação
        tokens = re.findall(r'\b\w+\b', texto_limpo)
        
        # Expande contrações
        tokens_expandidos = []
        for token in tokens:
            if token in self.contracoes:
                tokens_expandidos.extend(self.contracoes[token])
            else:
                tokens_expandidos.append(token)
        
        return tokens_expandidos
    
    def remover_stop_words(self, tokens: List[str]) -> List[str]:
        """Remove palavras vazias (stop words)"""
        return [token for token in tokens if token not in self.stop_words]
    
    def stemming_simples(self, palavra: str) -> str:
        """Stemming simples para português (remoção de sufixos comuns)"""
        sufixos = [
            'mente', 'ação', 'ções', 'ando', 'endo', 'indo',
            'ados', 'idas', 'idos', 'adas', 'ante', 'ente',
            'aram', 'eram', 'iram', 'avam', 'emos', 'imos',
            'ado', 'ida', 'ido', 'ada', 'ção', 'são', 'dor',
            'mos', 'ndo', 'ram', 'ava', 'ia', 'ar', 'er',
            'ir', 'am', 'em', 'ou', 'ei', 'ai', 'o', 's'
        ]
        
        palavra_original = palavra
        for sufixo in sufixos:
            if palavra.endswith(sufixo) and len(palavra) > len(sufixo) + 2:
                return palavra[:-len(sufixo)]
        
        return palavra_original
    
    def processar_texto_completo(self, texto: str, remover_stops: bool = True, 
                                fazer_stemming: bool = False) -> Dict:
        """Processa um texto completo e retorna estatísticas"""
        # Tokenização de sentenças
        sentencas = self.tokenizar_sentencas(texto)
        
        # Tokenização de palavras
        tokens = self.tokenizar_palavras(texto)
        
        # Remove stop words se solicitado
        if remover_stops:
            tokens = self.remover_stop_words(tokens)
        
        # Aplica stemming se solicitado
        if fazer_stemming:
            tokens = [self.stemming_simples(token) for token in tokens]
        
        # Calcula estatísticas
        freq_palavras = Counter(tokens)
        
        resultado = {
            'texto_original': texto,
            'num_sentencas': len(sentencas),
            'sentencas': sentencas,
            'num_tokens': len(tokens),
            'tokens': tokens,
            'tokens_unicos': len(set(tokens)),
            'frequencia_palavras': dict(freq_palavras.most_common(10)),
            'densidade_lexical': len(set(tokens)) / len(tokens) if tokens else 0
        }
        
        return resultado
    
    def analisar_sentimento_basico(self, tokens: List[str]) -> Dict:
        """Análise básica de sentimento usando palavras-chave"""
        palavras_positivas = {
            'bom', 'boa', 'ótimo', 'ótima', 'excelente', 'maravilhoso',
            'fantástico', 'incrível', 'amor', 'alegria', 'feliz', 'felicidade',
            'sucesso', 'vitória', 'positivo', 'positiva', 'legal', 'bacana',
            'gosto', 'adoro', 'perfeito', 'perfeita', 'lindo', 'linda'
        }
        
        palavras_negativas = {
            'ruim', 'péssimo', 'péssima', 'terrível', 'horrível', 'ódio',
            'raiva', 'triste', 'tristeza', 'fracasso', 'derrota', 'negativo',
            'negativa', 'detesto', 'odeio', 'chato', 'chata', 'feio', 'feia',
            'problema', 'dificuldade', 'erro', 'falha', 'mal'
        }
        
        positivas = sum(1 for token in tokens if token in palavras_positivas)
        negativas = sum(1 for token in tokens if token in palavras_negativas)
        
        if positivas > negativas:
            sentimento = 'positivo'
        elif negativas > positivas:
            sentimento = 'negativo'
        else:
            sentimento = 'neutro'
        
        return {
            'sentimento': sentimento,
            'palavras_positivas': positivas,
            'palavras_negativas': negativas,
            'polaridade': (positivas - negativas) / max(len(tokens), 1)
        }

# Exemplo de uso
if __name__ == "__main__":
    tokenizador = TokenizadorNLP()
    
    # Cole aqui o texto que será analisado:
    texto_exemplo = """
    Olá, eu sou Patrícia, venho falar um pouquinho sobre a minha vida, de onde eu vim.

Eu morava em Batalha Alagoas onde eu morava com os meus pais mas não era fácil. Estar com eles foram dias muito tristes e de chorar. Eu sofri muito, eles batiam muito em mim.

Eu tenho 13 irmãos mas uns foram embora e deixaram com eles e a minha irmã mais nova.

Os meus pais fizeram eu pedir esmola na rua, tinha muita vergonha de sair e ficar pedindo nas casas, ficava com vergonha de bater na casa da minha professora. Ficava muito triste porque a minha irmã mais nova não saia para pedir esmolars.Eu ia sozinha e ela só ia para escola, o meu sonho era estudar só que os meus pais não deixavam ir para escola, só irmã.

Quando era pra gente comprar roupas é muito triste porque o meu pai falou pra mim escolher só uma roupa, eu fui e peguei um vestido para mim porque ele deixou a minha irmã pegar o que ela quisesse. Para mim era muito triste eu só fiquei chorando e a minha irmã pegou blusa, calça,vestido, chinelo…

A minha mãe fazia eu trabalhar todos os dias .Ela chamava a minha irmã de rainha da casa e eu ficava de lado como se não estivesse ali, mas o meu outro irmão ligou pra mim perguntando se eu queria vir para Campinas e eu falei que sim, só que a minha mãe não queria que eu viesse. Ela falou assim pro meu irmão: - porque não você leva a Jessica e deixa a Patrícia aqui comigo ? E ele falou assim: -não, eu vou ficar com esta burra aí que a senhora está falando.

A minha mãe ficou muito brava com o meu irmão só que eu vim para Campinas para viver a minha vida e história, agora eu estudo com as professora lindas, estou vivendo a minha vida e hoje muito feliz onde estou com uma família de coração que me adotou, gosto muito deles. A minha história tem um final triste e outro feliz Sou muito grata a Deus
    """
    
    print("=== TOKENIZADOR DE LINGUAGEM NATURAL ===\n")
    
    # Processamento completo
    resultado = tokenizador.processar_texto_completo(
        texto_exemplo, 
        remover_stops=True, 
        fazer_stemming=True
    )
    
    print(f"Número de sentenças: {resultado['num_sentencas']}")
    print(f"Número de tokens: {resultado['num_tokens']}")
    print(f"Tokens únicos: {resultado['tokens_unicos']}")
    print(f"Densidade lexical: {resultado['densidade_lexical']:.2f}")
    
    print("\nSentenças encontradas:")
    for i, sentenca in enumerate(resultado['sentencas'], 1):
        print(f"{i}. {sentenca}")
    
    print("\nPalavras mais frequentes:")
    for palavra, freq in resultado['frequencia_palavras'].items():
        print(f"- {palavra}: {freq}")
    
    print("\nTokens processados:")
    print(resultado['tokens'])
    
    # Análise de sentimento
    analise_sentimento = tokenizador.analisar_sentimento_basico(resultado['tokens'])
    print(f"\n=== ANÁLISE DE SENTIMENTO ===")
    print(f"Sentimento: {analise_sentimento['sentimento']}")
    print(f"Palavras positivas: {analise_sentimento['palavras_positivas']}")
    print(f"Palavras negativas: {analise_sentimento['palavras_negativas']}")
    print(f"Polaridade: {analise_sentimento['polaridade']:.2f}")

   