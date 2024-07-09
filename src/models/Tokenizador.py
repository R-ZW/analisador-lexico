import models.Token as model_token

# ESTADOS GERAIS ----------------------------------------------------------------------------------------------
INICIAL                                         = "INICIAL"
ESPERANDO_FIM_DE_SENTENCA                       = "ESPERANDO FIM DE SENTENÇA"
# -------------------------------------------------------------------------------------------------------------
# ESTADOS DE DECLARAÇÃO DE VARIÁVEL ---------------------------------------------------------------------------
VARIAVEL_DECLARADA                              = "VARIÁVEL DECLARADA"
VARIAVEL_NOMEADA                                = "VARIÁVEL NOMEADA"
VARIAVEL_TIPO_PENDENTE                          = "VARIÁVEL NOMEADA, COM TIPO PENDENTE"
VARIAVEL_NUMBER                                 = "VARIÁVEL NOMEADA, COM TIPO NUMBER"
VARIAVEL_STRING                                 = "VARIÁVEL NOMEADA, COM TIPO STRING"
VARIAVEL_LOGICA                                 = "VARIÁVEL NOMEADA, COM TIPO LÓGICO"
ESPERANDO_NUMBER                                = "VARIÁVEL NUMBER, ESPERANDO NÚMERO"
ESPERANDO_STRING                                = "VARIÁVEL STRING, ESPERANDO STRING"
ESPERANDO_LOGICO                                = "VARIÁVEL LÓGICA, ESPERANDO LÓGICO"
# --------------------------------------------------------------------------------------------------------------
# ESTADOS DE ATRIBUIÇÃO ----------------------------------------------------------------------------------------
ESPERANDO_ATRIBUICAO                            = "ESPERANDO ATRIBUIÇÃO"
ATRIBUICAO_ESPERANDO_VALOR                      = "ATRIBUIÇÃO ESPERANDO VALOR"
# --------------------------------------------------------------------------------------------------------------
# ESTADOS DE IMPRESSÃO -----------------------------------------------------------------------------------------
IMPRESSAO_ESPERANDO_PARENTESE_ESQUERDA          = "FUNÇÃO DE IMPRESSÃO ESPERANDO UM PARÊNTESE ABERTO"
IMPRESSAO_ESPERANDO_VALOR                       = "FUNÇÃO DE IMPRESSÃO ESPERANDO O QUE VAI SER IMPRESSO"
IMPRESSAO_ESPERANDO_PARENTESE_DIREITA           = "FUNÇÃO DE IMPRESSÃO ESPERANDO UM PARÊNTESE FECHADO"
# --------------------------------------------------------------------------------------------------------------
# ESTADOS DE LEITURA -------------------------------------------------------------------------------------------
ESPERANDO_COMANDO_DE_LEITURA                    = "ESPERANDO O COMANDO INPUT PARA LEITURA"
LEITURA_ESPERANDO_PARENTESE_ESQUERDA            = "FUNÇÃO DE LEITURA ESPERANDO UM PARÊNTESE ABERTO"
LEITURA_ESPERANDO_TEXTO                         = "FUNÇÃO DE LEITURA ESPERANDO O TEXTO DE SOLICITAÇÃO"
LEITURA_ESPERANDO_PARENTESE_DIREITA             = "FUNÇÃO DE LEITURA ESPERANDO UM PARÊNTESE FECHADO"
# --------------------------------------------------------------------------------------------------------------
# ESTADOS DO CONDICIONAL ---------------------------------------------------------------------------------------
CONDICIONAL_ESPERANDO_PARENTESE_ESQUERDA            = "CONDICIONAL ESPERANDO UM PARÊNTESE ABERTO"
CONDICIONAL_ESPERANDO_VARIAVEL_VALOR                = "CONDICIONAL ESPERANDO UMA VARIÁVEL OU VALOR"
CONDICIONAL_ESPERANDO_OPERADOR_PARENTESE_DIREITA    = "CONDICIONAL ESPERANDO UM OPERADOR OU PARÊNTESE FECHADO"
CONDICIONAL_ESPERANDO_ABERTURA_DE_BLOCO             = "CONDICIONAL ESPERANDO A ABERTURA DE UM BLOCO"
# --------------------------------------------------------------------------------------------------------------

class Tokenizador:
    def __init__(self):
        self.symbols        = []            #TODOS OS SÍMBOLOS DO CÓDIGO
        self.estado         = INICIAL       #ESTADO DO AUTOMATO
        self.tokens         = []            #TODOS OS TOKENS IDENTIFICADOS
        self.token          = ""            #NOME DO TOKEN
        self.symbols_token  = []            #SÍMBOLOS PRESENTES NO ULTIMO TOKEN
        self.linha          = 1             #LINHA ATUAL
        self.continua       = True          #CONTINUAR A LEITURA
        self.if_aberto      = False         #SE O IF ESTÁ ABERTO

    def identificar_tokens(self):
        for symbol in self.symbols:
            if self.continua:
                self.continua = False

                if symbol.name != "COMENTARIO" and symbol.name != "NOVA_LINHA":
                    self.symbols_token.append(symbol)

                match symbol.name:
                    case "ESPACO_OU_TAB" | "COMENTARIO":
                        self.continua = True
                        continue

                    case "PALAVRA_RESERVADA":
                        match symbol.value:
                            case "let" | "const" | "var":
                                if self.estado == INICIAL:                                    
                                    self.estado = VARIAVEL_DECLARADA
                                    self.continua = True
                                    continue

                            case "console.log":
                                if self.estado == INICIAL:                                    
                                    self.token = "Impressão no console"
                                    self.estado = IMPRESSAO_ESPERANDO_PARENTESE_ESQUERDA
                                    self.continua = True
                                    continue

                            case "await":
                                if self.estado == INICIAL or self.estado == ATRIBUICAO_ESPERANDO_VALOR:
                                    self.estado = ESPERANDO_COMANDO_DE_LEITURA
                                    self.continua = True
                                    continue

                            case "input":
                                if self.estado == ESPERANDO_COMANDO_DE_LEITURA:                                    
                                    self.token = "Leitura no console"
                                    self.estado = LEITURA_ESPERANDO_PARENTESE_ESQUERDA
                                    self.continua = True
                                    continue

                            case "if":
                                if self.estado == INICIAL:
                                    self.estado = CONDICIONAL_ESPERANDO_PARENTESE_ESQUERDA
                                    self.continua = True
                                    continue

                            case "number":
                                if self.estado == VARIAVEL_TIPO_PENDENTE:                                    
                                    self.estado = VARIAVEL_NUMBER
                                    self.continua = True
                                    continue

                            case "string":
                                if self.estado == VARIAVEL_TIPO_PENDENTE:                                    
                                    self.estado = VARIAVEL_STRING
                                    self.continua = True
                                    continue

                                if self.estado == ATRIBUICAO_ESPERANDO_VALOR:
                                    self.estado = ESPERANDO_FIM_DE_SENTENCA
                                    self.continua = True
                                    continue

                            case "boolean":
                                if self.estado == VARIAVEL_TIPO_PENDENTE:                                    
                                    self.estado = VARIAVEL_LOGICA
                                    self.continua = True
                                    continue

                            case "true" | "false":
                                if self.estado == ESPERANDO_LOGICO:                                    
                                    self.token = "Declaração de variável de tipo lógico"
                                    self.estado = ESPERANDO_FIM_DE_SENTENCA
                                    self.continua = True
                                    continue

                    case "IDENTIFICADOR":   
                        if self.estado == INICIAL:
                            self.estado = ESPERANDO_ATRIBUICAO
                            self.continua = True
                            continue

                        if self.estado == ESPERANDO_NUMBER:
                            self.estado = ESPERANDO_FIM_DE_SENTENCA
                            self.token = "Declaração de variável de tipo number"
                            self.continua = True
                            continue
               
                        if self.estado == VARIAVEL_DECLARADA:                            
                            self.estado = VARIAVEL_NOMEADA
                            self.continua = True
                            continue

                        if self.estado == IMPRESSAO_ESPERANDO_VALOR:                            
                            self.estado = IMPRESSAO_ESPERANDO_PARENTESE_DIREITA
                            self.continua = True
                            continue

                        if self.estado == LEITURA_ESPERANDO_TEXTO:                            
                            self.estado = LEITURA_ESPERANDO_PARENTESE_DIREITA
                            self.continua = True
                            continue

                        if self.estado == CONDICIONAL_ESPERANDO_VARIAVEL_VALOR:
                            self.estado = CONDICIONAL_ESPERANDO_OPERADOR_PARENTESE_DIREITA
                            self.continua = True
                            continue

                        if self.estado == ATRIBUICAO_ESPERANDO_VALOR:
                            self.estado = ESPERANDO_FIM_DE_SENTENCA
                            self.continua = True
                            continue


                    case "DOIS_PONTOS":
                        if self.estado == VARIAVEL_NOMEADA:                            
                            self.estado = VARIAVEL_TIPO_PENDENTE
                            self.continua = True
                            continue

                    
                    case "OPERADOR_ARITMETICO":
                        match symbol.value:
                            case "+":
                                if self.estado == ESPERANDO_FIM_DE_SENTENCA:
                                    novo_token = model_token.Token("Operador de adição", self.linha, ["+"])
                                    self.tokens.append(novo_token)
                                    self.estado = ESPERANDO_NUMBER
                                    self.continua = True
                                    continue
                            
                            case "-":
                                if self.estado == ESPERANDO_FIM_DE_SENTENCA:                                
                                    novo_token = model_token.Token("Operador de subtração", self.linha, ["-"])
                                    self.tokens.append(novo_token)
                                    self.estado = ESPERANDO_NUMBER
                                    self.continua = True
                                    continue

                            case "*":
                                if self.estado == ESPERANDO_FIM_DE_SENTENCA:
                                    novo_token = model_token.Token("Operador de multiplicação", self.linha, ["*"])
                                    self.tokens.append(novo_token)
                                    self.estado = ESPERANDO_NUMBER
                                    self.continua = True
                                    continue

                            case "/":
                                if self.estado == ESPERANDO_FIM_DE_SENTENCA:
                                    novo_token = model_token.Token("Operador de divisão", self.linha, ["/"])
                                    self.tokens.append(novo_token)
                                    self.estado = ESPERANDO_NUMBER
                                    self.continua = True
                                    continue

                            case "%":
                                if self.estado == ESPERANDO_FIM_DE_SENTENCA:
                                    novo_token = model_token.Token("Operador de módulo", self.linha, ["%"])
                                    self.tokens.append(novo_token)
                                    self.estado = ESPERANDO_NUMBER
                                    self.continua = True
                                    continue


                    case "OPERADOR_LOGICO":
                        match symbol.value:
                            case "==":
                                if self.estado == CONDICIONAL_ESPERANDO_OPERADOR_PARENTESE_DIREITA:
                                    novo_token = model_token.Token("Operador de igualdade", self.linha, ["=="])
                                    self.tokens.append(novo_token)
                                    self.estado = CONDICIONAL_ESPERANDO_VARIAVEL_VALOR
                                    self.continua = True
                                    continue
                            
                            case "!=":
                                if self.estado == CONDICIONAL_ESPERANDO_OPERADOR_PARENTESE_DIREITA:
                                    novo_token = model_token.Token("Operador de diferença", self.linha, ["!="])
                                    self.tokens.append(novo_token)
                                    self.estado = CONDICIONAL_ESPERANDO_VARIAVEL_VALOR
                                    self.continua = True
                                    continue
                            
                            case ">":
                                if self.estado == CONDICIONAL_ESPERANDO_OPERADOR_PARENTESE_DIREITA:
                                    novo_token = model_token.Token("Operador de maior que", self.linha, [">"])
                                    self.tokens.append(novo_token)
                                    self.estado = CONDICIONAL_ESPERANDO_VARIAVEL_VALOR
                                    self.continua = True
                                    continue
                            
                            case "<":
                                if self.estado == CONDICIONAL_ESPERANDO_OPERADOR_PARENTESE_DIREITA:
                                    novo_token = model_token.Token("Operador de menor que", self.linha, ["<"])
                                    self.tokens.append(novo_token)
                                    self.estado = CONDICIONAL_ESPERANDO_VARIAVEL_VALOR
                                    self.continua = True
                                    continue

                            case ">=":
                                if self.estado == CONDICIONAL_ESPERANDO_OPERADOR_PARENTESE_DIREITA:
                                    novo_token = model_token.Token("Operador de maior ou igual que", self.linha, [">="])
                                    self.tokens.append(novo_token)
                                    self.estado = CONDICIONAL_ESPERANDO_VARIAVEL_VALOR
                                    self.continua = True
                                    continue

                            case "<=":
                                if self.estado == CONDICIONAL_ESPERANDO_OPERADOR_PARENTESE_DIREITA:
                                    novo_token = model_token.Token("Operador de menor ou igual que", self.linha, ["<="])
                                    self.tokens.append(novo_token)
                                    self.estado = CONDICIONAL_ESPERANDO_VARIAVEL_VALOR
                                    self.continua = True
                                    continue

                            case "&&":
                                if self.estado == CONDICIONAL_ESPERANDO_OPERADOR_PARENTESE_DIREITA:
                                    novo_token = model_token.Token("Operador lógico AND", self.linha, ["&&"])
                                    self.tokens.append(novo_token)
                                    self.estado = CONDICIONAL_ESPERANDO_VARIAVEL_VALOR
                                    self.continua = True
                                    continue

                            case "||":
                                if self.estado == CONDICIONAL_ESPERANDO_OPERADOR_PARENTESE_DIREITA:
                                    novo_token = model_token.Token("Operador lógico OR", self.linha, ["||"])
                                    self.tokens.append(novo_token)
                                    self.estado = CONDICIONAL_ESPERANDO_VARIAVEL_VALOR
                                    self.continua = True
                                    continue

                            case "!":
                                if self.estado == CONDICIONAL_ESPERANDO_OPERADOR_PARENTESE_DIREITA:
                                    novo_token = model_token.Token("Operador lógico NOT", self.linha, ["!"])
                                    self.tokens.append(novo_token)
                                    self.estado = CONDICIONAL_ESPERANDO_VARIAVEL_VALOR
                                    self.continua = True
                                    continue


                    case "ATRIBUICAO":
                        match symbol.value:
                            case "=":
                                novo_token = model_token.Token("Atribuição simples", self.linha, ["="])
                                self.tokens.append(novo_token)

                                if self.estado == ESPERANDO_ATRIBUICAO:
                                    self.estado = ATRIBUICAO_ESPERANDO_VALOR
                                    self.continua = True
                                    continue

                                if self.estado == VARIAVEL_STRING:                                    
                                    self.estado = ESPERANDO_STRING
                                    self.continua = True 
                                    continue

                                if self.estado == VARIAVEL_NUMBER:                                    
                                    self.estado = ESPERANDO_NUMBER
                                    self.continua = True
                                    continue

                                if self.estado == VARIAVEL_LOGICA:                                    
                                    self.estado = ESPERANDO_LOGICO
                                    self.continua = True
                                    continue


                            case "+=":
                                if self.estado == ESPERANDO_ATRIBUICAO:
                                    novo_token = model_token.Token("Atribuição de soma", self.linha, ["+="])
                                    self.tokens.append(novo_token)
                                    self.estado = ATRIBUICAO_ESPERANDO_VALOR   
                                    self.continua = True
                            
                            case "-=":
                                if self.estado == ESPERANDO_ATRIBUICAO:
                                    novo_token = model_token.Token("Atribuição de subtração", self.linha, ["-="])
                                    self.tokens.append(novo_token)
                                    self.estado = ATRIBUICAO_ESPERANDO_VALOR   
                                    self.continua = True
                            
                            case "*=":
                                if self.estado == ESPERANDO_ATRIBUICAO:
                                    novo_token = model_token.Token("Atribuição de multiplicação", self.linha, ["*="])
                                    self.tokens.append(novo_token)
                                    self.estado = ATRIBUICAO_ESPERANDO_VALOR   
                                    self.continua = True
                            
                            case "/=":
                                if self.estado == ESPERANDO_ATRIBUICAO:
                                    novo_token = model_token.Token("Atribuição de divisão", self.linha, ["/="])
                                    self.estado = ATRIBUICAO_ESPERANDO_VALOR   
                                    self.tokens.append(novo_token)
                                    self.continua = True

                            case "++":
                                if self.estado == ESPERANDO_ATRIBUICAO:
                                    self.token = "Incremento de variável"
                                    self.estado = ESPERANDO_FIM_DE_SENTENCA
                                    self.continua = True
                            
                            case "--":
                                if self.estado == ESPERANDO_ATRIBUICAO:
                                    self.token = "Decremento de variável"
                                    self.estado = ESPERANDO_FIM_DE_SENTENCA 
                                    self.continua = True
                                

                    case "STRING":
                        if self.estado == ESPERANDO_STRING:                            
                            self.token = "Declaração de variável de tipo string"
                            self.estado = ESPERANDO_FIM_DE_SENTENCA
                            self.continua = True
                            continue

                        if self.estado == IMPRESSAO_ESPERANDO_VALOR:
                            self.estado = IMPRESSAO_ESPERANDO_PARENTESE_DIREITA
                            self.continua = True
                            continue

                        if self.estado == LEITURA_ESPERANDO_TEXTO:                            
                            self.estado = LEITURA_ESPERANDO_PARENTESE_DIREITA
                            self.continua = True
                            continue

                        if self.estado == CONDICIONAL_ESPERANDO_VARIAVEL_VALOR:
                            self.estado = CONDICIONAL_ESPERANDO_OPERADOR_PARENTESE_DIREITA
                            self.continua = True
                            continue

                        if self.estado == ATRIBUICAO_ESPERANDO_VALOR:
                            self.estado = ESPERANDO_FIM_DE_SENTENCA
                            self.continua = True
                            continue


                    case "INT":
                        if self.estado == ESPERANDO_NUMBER:     
                            if (
                                self.token != "Declaração de variável de tipo real" and 
                                self.token != "Declaração de variável de tipo number"
                                ):                       
                                self.token = "Declaração de variável de tipo inteiro"
                                
                            self.estado = ESPERANDO_FIM_DE_SENTENCA
                            self.continua = True
                            continue

                        if self.estado == ATRIBUICAO_ESPERANDO_VALOR:
                            self.estado = ESPERANDO_FIM_DE_SENTENCA
                            self.continua = True
                            continue

                        if self.estado == CONDICIONAL_ESPERANDO_VARIAVEL_VALOR:
                            self.estado = CONDICIONAL_ESPERANDO_OPERADOR_PARENTESE_DIREITA
                            self.continua = True
                            continue


                    case "FLOAT":
                        if self.estado == ESPERANDO_NUMBER:                            
                            self.token = "Declaração de variável de tipo real"
                            self.estado = ESPERANDO_FIM_DE_SENTENCA
                            self.continua = True
                            continue

                        if self.estado == ATRIBUICAO_ESPERANDO_VALOR:
                            self.estado = ESPERANDO_FIM_DE_SENTENCA
                            self.continua = True
                            continue

                        if self.estado == CONDICIONAL_ESPERANDO_VARIAVEL_VALOR:
                            self.estado = CONDICIONAL_ESPERANDO_OPERADOR_PARENTESE_DIREITA
                            self.continua = True
                            continue


                    case "PARENTESE_ESQUERDA":
                        if self.estado == IMPRESSAO_ESPERANDO_PARENTESE_ESQUERDA:                            
                            self.estado = IMPRESSAO_ESPERANDO_VALOR
                            self.continua = True
                            continue

                        if self.estado == LEITURA_ESPERANDO_PARENTESE_ESQUERDA:                            
                            self.estado = LEITURA_ESPERANDO_TEXTO
                            self.continua = True
                            continue

                        if self.estado == CONDICIONAL_ESPERANDO_PARENTESE_ESQUERDA:
                            self.estado = CONDICIONAL_ESPERANDO_VARIAVEL_VALOR
                            self.continua = True
                            continue


                    case "PARENTESE_DIREITA":
                        if self.estado == IMPRESSAO_ESPERANDO_PARENTESE_DIREITA:                            
                            self.estado = ESPERANDO_FIM_DE_SENTENCA
                            self.continua = True
                            continue

                        if self.estado == LEITURA_ESPERANDO_PARENTESE_DIREITA:                            
                            self.estado = ESPERANDO_FIM_DE_SENTENCA
                            self.continua = True
                            continue

                        if self.estado == CONDICIONAL_ESPERANDO_OPERADOR_PARENTESE_DIREITA:
                            self.estado = CONDICIONAL_ESPERANDO_ABERTURA_DE_BLOCO
                            self.continua = True
                            continue

                    
                    case "CHAVE_ESQUERDA":
                        if self.estado == CONDICIONAL_ESPERANDO_ABERTURA_DE_BLOCO:
                            self.if_aberto = True
                            novo_token = model_token.Token("Abertura de bloco condicional", self.linha, self.symbols_token)
                            self.tokens.append(novo_token)
                            self.symbols_token = []
                            self.token = ""
                            self.estado = INICIAL
                            self.continua = True
                            continue

                    case "CHAVE_DIREITA":
                        if self.if_aberto:
                            self.if_aberto = False
                            novo_token = model_token.Token("Fechamento de bloco condicional", self.linha, self.symbols_token)
                            self.tokens.append(novo_token)
                            self.symbols_token = []
                            self.token = ""
                            self.estado = INICIAL
                            self.continua = True
                            continue

                    case "PONTO_E_VIRGULA":
                        if self.estado == ESPERANDO_FIM_DE_SENTENCA:
                            if self.token != "":
                                novo_token = model_token.Token(self.token, self.linha, self.symbols_token)
                                self.tokens.append(novo_token)
                            self.symbols_token = []
                            self.token = ""
                            self.estado = INICIAL
                            self.continua = True
                            continue


                    case "NOVA_LINHA":
                        if self.estado == ESPERANDO_FIM_DE_SENTENCA:
                            if self.token != "": 
                                novo_token = model_token.Token(self.token, self.linha, self.symbols_token)
                                self.tokens.append(novo_token)
                            self.symbols_token = []
                            self.token = ""
                            self.estado = INICIAL
                            self.continua = True

                        if self.estado == INICIAL:
                            self.continua = True    

                        self.linha += 1
                        continue
            else:
                print(f"ERRO LÉXICO!!!!!".center(75, '-'))
                print(f"ESTADO -> {self.estado}")
                print(f"LINHA -> {self.linha}")
                print("ERRO NO SIMBOLO -> ", end="")
                if len(self.symbols_token) > 0:
                    print(f"{self.symbols_token[len(self.symbols_token)-1]}")
                else:
                    ultimo_token = self.tokens[len(self.tokens)-1]
                    print(ultimo_token.__dict__())
                    print(f"{ultimo_token.symbols_token[len(ultimo_token.symbols_token)-1]}")

                print("".center(75, '-'))
                return False
            

    def mostrar_tokens(self):
        print(f"{"TOKENS".center(75, '-')}")

        for token in self.tokens:
            print(f"|LINHA {token.linha} -> {token.token} |")
            print(f"|CONTEÚDO: '", end="")

            for symbol in token.symbols_token:
                print(symbol, end="")
            print("'|")
            print(f"{"".center(60, '-')}")

        print(f"{"".center(75, '-')}")
