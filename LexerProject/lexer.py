
from .tokens import Token
from .constantes import OPERADORES, SIMBOLOS, HARD_KEYWORDS, SOFT_KEYWORDS, MODIFIER_KEYWORDS, KEYWORDS
from .utils import eh_hex, eh_bin, eh_sufixo_inteiro, eh_sufixo_float, eh_separador
from .erros import UnclosedComment, UnclosedString, InvalidCharLiteral

class Lexer: #objeto que vai ler o código e guardar a posicao onde ele está lendo o codigo-fonte
    def __init__(self, source):
        self.source = source #codigo fonte
        #!!porque tem pos, linha e coluna??
        self.pos = 0 #posicao da leitura no texto/codigo-fonte 
        self.linha = 1
        self.coluna = 1

    def ch_atual(self): #funcao para saber em qual caractere o lexer está
        if self.pos < len(self.source): #se ainda nao chegou ao final do codigo-fonte, retorne o caractere na posicao de leitura atual
            return self.source[self.pos] #retorna o caractere na posicao de leitura atual do lexer
        return '\0' #fim do codigo-fonte
    
    def avancar(self): #funcao para avancar a leitura do caracteres -> um por vez
        ch = self.ch_atual()
        self.pos += 1
        if ch == '\n': #indicador no codigo fonte .kts que a linha acabou
            self.linha += 1
            self.coluna = 1
        else:
            self.coluna += 1
        return ch
    
    def pular_linha(self):
        while self.ch_atual() != '\n' and self.ch_atual() != '\0':
            self.avancar()
        if self.ch_atual() == '\n':
            self.avancar()

    def ch_proximo(self): #olha para o proximo caractere no codigo-fonte
        if self.pos + 1 < len(self.source):
            return self.source[self.pos + 1]
        return '\0'

    #funcoes para ignorar inutilidades pro lexer(espaco, comentarios, tabs, \n)
    def pular_espaco(self):
        while self.ch_atual() in [' ', '\t', '\r', '\n']:
            self.avancar()

    def pular_comentario_linha(self):
        while self.ch_atual() != '\n' and self.ch_atual() != '\0':
            self.avancar()

    def pular_comentario_blocos(self):
        profundidade = 1
        self.avancar()
        self.avancar()
        while profundidade > 0:
            if self.ch_atual() == '\0':
                raise Exception("erro lexico: comentario nao fechado!")
            if self.ch_atual() == '/' and self.ch_proximo() == '*':
                profundidade  += 1
                self.avancar()
                self.avancar()
            elif self.ch_atual() == '*' and self.ch_proximo() == '/':
                profundidade -= 1
                self.avancar()
                self.avancar()
            else:
                self.avancar()

    #reconhecimento de identificadores, palavras-chaves, literais etc
    
    def eh_hex(self, ch):
       return ch.isdigit() or ch.lower() in 'abcdef'
    
    def eh_bin(self, ch):
        return ch in '01'
    
    def eh_sufixo_inteiro(self, ch):
        return ch.lower() in ('u', 'l')

    def eh_sufixo_float(self, ch):
        return ch.lower() == 'f'
    
    def eh_separador(self, ch):
        return ch == '_' #retorna true se caractere == '_'
    
    #reconhece literais numericos int, float, hex, bin
    def reconhece_literais_numericos(self):
        inicio = self.pos
        linha = self.linha
        coluna = self.coluna
        tipo = "INT_LITERAL"
        tem_ponto = False
        tem_expoente = False

        #reconhece binario
        if self.ch_atual() == '0' and self.ch_proximo().lower() == 'b':
            self.avancar()
            self.avancar()
            encontrou_digito = False # garantir pelo menos um digito binario

            while self.eh_bin(self.ch_atual()) or self.eh_separador(self.ch_atual()):
                if self.eh_bin(self.ch_atual()):
                    encontrou_digito = True
                self.avancar()
            if not encontrou_digito:
                raise Exception(f"erro lexico: literal binario sem digitos na linha {linha}, coluna {coluna}")
        
        #reconhece hexadecimal
        elif self.ch_atual() == '0' and self.ch_proximo().lower() == 'x':
            self.avancar()
            self.avancar() #duas chamadas para avançar 0x
            # deve ter ao menos um dígito hex
            encontrou_digito = False
            while self.eh_hex(self.ch_atual()) or self.eh_separador(self.ch_atual()):
                if self.eh_hex(self.ch_atual()):
                    encontrou_digito = True
                self.avancar()
            if not encontrou_digito:
                raise Exception(f"erro lexico: literal hexadecimal sem digitos na linha {linha}, coluna {coluna}")

        #reconhece decimal e float

        else:
            #reconhece parte inteira do numero
            while self.ch_atual().isdigit() or self.eh_separador(self.ch_atual()):
                self.avancar()
            
            if self.ch_atual() == '.' and self.ch_proximo() != '.':
                tem_ponto = True
                self.avancar()
                while self.ch_atual().isdigit() or self.eh_separador(self.ch_atual()):
                    self.avancar()

            #reconhece o expoente
            if self.ch_atual().lower() == 'e':
                tem_expoente = True
                self.avancar()
                if self.ch_atual() in ['+', '-']:
                    self.avancar()
                while self.ch_atual().isdigit() or self.eh_separador(self.ch_atual()):
                    self.avancar()

        #reconhece sufixos inteiros u/U e L/l(em qualquer ordem)
        while self.ch_atual().lower() in ['u', 'l']:
            self.avancar()

        #reconhece sufixos float
        if self.ch_atual().lower() == 'f':
            tipo = "FLOAT_LITERAL"
            self.avancar()
        #reconhece se tem ponto ou expoente -> float
        if tem_ponto or tem_expoente:
            tipo = "FLOAT_LITERAL"
        lexema = self.source[inicio:self.pos]
        return Token(tipo, lexema, linha, coluna)
    
                    
                                                            




    #reconhecimento dos identificadores
    def reconhece_identificadores(self):
        inicio = self.pos
        linha = self.linha
        coluna = self.coluna
        #isalnum retorna true se os caracteres ou caractere na string sao numeros ou letras
        while self.ch_atual().isalnum() or self.ch_atual() == '_':  
            self.avancar()
        lexema = self.source[inicio:self.pos]
         # lookup direto no mapa KEYWORDS -> token type específico
        tipo = KEYWORDS.get(lexema)
        if tipo is not None:
            return Token(tipo, lexema, linha, coluna)
        # caso não seja keyword
        return Token("IDENTIFIER", lexema, linha, coluna)
    
    def reconhece_identificador_crase(self):
        linha = self.linha
        coluna = self.coluna
        self.avancar()
        inicio = self.pos
        while self.ch_atual() != '`' and self.ch_atual() != '\0':
            self.avancar()
        if self.ch_atual() != '`':
            raise Exception(f"Identificador com crase nao fechado na linha: {linha}, coluna: {coluna}")
        lexema = self.source[inicio:self.pos]
        self.avancar()
        return Token("Quoted_identifier",lexema, linha,coluna)

    #reconhecendo numeros
    #inutilizado!!!!!!!!!!!!!!!!!!!!!!!!!
    def reconhece_numeros(self):
        inicio = self.pos
        linha = self.linha 
        coluna = self.coluna
        while self.ch_atual().isdigit(): #enquanto o caractere sendo lido pelo lexer for um digito
            self.avancar()
        lexema = self.source[inicio:self.pos]
        return Token("INT_LITERAL", lexema,linha,coluna)

    '''
Testa 3 caracteres (===, ..<)
Depois 2 (==, !=, ?.)
Depois 1 (!, <, >)
    '''
    def reconhece_operadores(self):
        linha = self.linha
        coluna = self.coluna
        #tenta casar do maior para o menor
        for tamanho in (3,2,1):
            lexema = self.source[self.pos:self.pos + tamanho]
            if lexema in OPERADORES:
                for _ in range(tamanho):
                    self.avancar()
                return Token(OPERADORES[lexema], lexema, linha, coluna)
        return None
    
    #inutilizada!!  !is, !in, as? são tokens normais do mapa e sao reconhecidos em reconhece_identificadores()
    #importante para diferenciar !is e nao reconhecer '!' como operador
    def reconhece_hard_keyword_composta(self): #reconhecer keywords compostas como !is como hard_keyword"
        linha = self.linha
        coluna = self.coluna

        for kw in ("as?", "!in", "!is"):
            if self.source.startswith(kw, self.pos):
                for _ in range(len(kw)):
                    self.avancar()
                return Token("HARD_KEYWORD", kw, linha, coluna)

        return None
    
    #reconhece literais de caractere 'a'
    def reconhece_char_literal(self):
        linha = self.linha
        coluna = self.coluna
        self.avancar()  # '
        if self.ch_atual() == '\0' or self.ch_atual() == '\n':
            raise Exception("erro lexico: literal de caractere invalido")

        if self.ch_atual() == '\\':  # escape
          self.avancar()
          if self.ch_atual() == '\0':
            raise Exception("erro lexico: escape invalido em char")
          self.avancar()
        else:
            self.avancar()

        if self.ch_atual() != "'": #erro aqui ao reconhecer 'a'
            raise Exception(
            f"erro lexico: literal de caractere invalido na linha {linha}, coluna {coluna}")
            

        self.avancar()  # fecha aspas simples
        lexema = self.source[self.pos - 3:self.pos]
        return Token("CHAR_LITERAL", lexema, linha, coluna)
    
    #reconhece strings simples "string"
    def reconhece_string_interpolada(self):
        tokens = []
        linha = self.linha
        coluna = self.coluna

        tokens.append(Token("STRING_START", '"', linha, coluna))
        self.avancar()  # consome "

        buffer = ""
        buffer_linha = self.linha
        buffer_coluna = self.coluna

        while True:
            ch = self.ch_atual()

            if ch == '\0':
                raise Exception("erro lexico: string nao fechada")

            # fim da string
            if ch == '"':
                if buffer:
                    tokens.append(Token("STRING_TEXT", buffer, buffer_linha, buffer_coluna))
                tokens.append(Token("STRING_END", '"', self.linha, self.coluna))
                self.avancar()
                break

            # interpolação
            if ch == '$':
                if buffer:
                 tokens.append(Token("STRING_TEXT", buffer, buffer_linha, buffer_coluna))
                 buffer = ""

                self.avancar()  # consome $

                # ${expressao}
                if self.ch_atual() == '{':
                    tokens.append(Token("STRING_INTERP_START", "${", self.linha, self.coluna))
                    self.avancar()  # consome {

                    expr_inicio_linha = self.linha
                    expr_inicio_coluna = self.coluna
                    conteudo = ""

                    while self.ch_atual() != '}' and self.ch_atual() != '\0':
                      conteudo += self.ch_atual()
                      self.avancar()

                    if self.ch_atual() != '}':
                     raise Exception("erro lexico: interpolacao nao fechada")

                    tokens.append(Token(
                     "STRING_INTERP_EXPR",
                     conteudo,
                     expr_inicio_linha,
                     expr_inicio_coluna
                    ))
                    tokens.append(Token("STRING_INTERP_END", "}", self.linha, self.coluna))
                    self.avancar()  # consome }

                    buffer_linha = self.linha
                    buffer_coluna = self.coluna
                    continue

                # $ident
                else:
                    inicio = self.pos
                    while self.ch_atual().isalnum() or self.ch_atual() == '_':
                        self.avancar()

                    if self.pos == inicio:
                        raise Exception(
                            f"erro lexico: interpolacao invalida na linha {self.linha}, coluna {self.coluna}"
                        )

                    ident = self.source[inicio:self.pos]
                    tokens.append(Token("STRING_INTERP_ID", ident, self.linha, self.coluna))
                    buffer = ""
                    buffer_linha = self.linha
                    buffer_coluna = self.coluna
                    continue


            # escape
            if ch == '\\':
                buffer += ch
                self.avancar()
                buffer += self.ch_atual()
                self.avancar()
                continue

            # caractere normal
            buffer += ch
            self.avancar()

        return tokens






    '''
ordem de chamada:
1. ignorar lixo
2. EOF
3. comentários
4. identificadores / keywords simples
5. números
6. identificadores com crase
7. HARD KEYWORDS COMPOSTAS  
8. operadores (maximal munch)
9. símbolos simples
10. erro
'''   

    def proximo_token(self):
        # REGRA ESPECIAL: Shebang (somente no início do arquivo)
        if self.pos == 0 and self.ch_atual() == '#' and self.ch_proximo() == '!':
            self.pular_linha() #?
            return self.proximo_token()
        
        #decide quais caracteres sao irrelevantes e garante o salto de linha ao ler '\n'
        self.pular_espaco()

        #reconhece fim de codigo
        if self.ch_atual() == '\0':
            return Token("EOF", "", self.linha, self.coluna)
        
        #pula comentarios
        if self.ch_atual() == '/' and self.ch_proximo() == '/':
            self.pular_comentario_linha()
            return self.proximo_token()

        if self.ch_atual() == '/' and self.ch_proximo() == '*':
            self.pular_comentario_blocos()
            return self.proximo_token()

        #reconhece identificadores
        #isalpha retorna True apenas se a string contiver exclusivamente letras (A-Z, a-z ou unicode)
        if self.ch_atual().isalpha() or self.ch_atual() == '_':
            return self.reconhece_identificadores()
        
        #reconhece literais numericos
        if self.ch_atual().isdigit():
            return self.reconhece_literais_numericos()
            
        #reconhece strings 
        if self.ch_atual() == '"':
            return self.reconhece_string_interpolada()

        if self.ch_atual() == "'":
            return self.reconhece_char_literal()
        
        #reconhece identificador com crase
        if self.ch_atual() == '`':
            return self.reconhece_identificador_crase()
        

        #reconhece operadores
        op = self.reconhece_operadores()
        if op:
            return op
        
        #reconhece simbolos
        if self.ch_atual() in SIMBOLOS:
            ch = self.avancar()
            return Token(SIMBOLOS[ch], ch, self.linha, self.coluna - 1)
        raise Exception( f"erro lexico: caractere '{self.ch_atual()}' "
                        f"erro na linha {self.linha}, e coluna {self.coluna}" )
          

    def tokenize(self):
        tokens = []
        while True:
            token = self.proximo_token()

            if isinstance(token, list):
                tokens.extend(token)
                last = token[-1]
            else:
                tokens.append(token)
                last = token

            if last.tipo == "EOF":
             break

        return tokens


