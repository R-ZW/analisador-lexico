SYMBOLS = [
    ("COMENTARIO", r"//.*"),  # Comentários de linha única
    (
        "PALAVRA_RESERVADA",
        r"\b(await|boolean|break|case|class|const|console.log|continue|debugger|default|delete|do|else|enum|export|extends|false|finally|for|function|if|import|in|input|instanceof|let|new|null|number|return|string|super|switch|this|throw|true|try|typeof|var|void|while|with|yield|interface|type|public|private|protected|readonly)\b",
    ),
    (
        "IDENTIFICADOR",
        r"[A-Za-z_$][A-Za-z0-9_$]*",
    ),  # NOMES IDENTIFICADORES DE VARIAVEIS
    ("FLOAT", r"\b\d*\.\d+\b|\b\d+\.\d*\b"),  # NUMEROS DECIMAIS
    ("INT", r"\b\d+\b"),  # NUMEROS INTEIROS
    ("STRING", r'(["\'])(?:(?=(\\?))\2.)*?\1'),  # STRINGS
    ("OPERADOR_LOGICO", r"(==|!=|<=|>=|&&|\|\||[!<>])"),  # OPERADORES LOGICOS
    ("ATRIBUICAO", r"=|\+=|-=|\*=|/=|\+\+|--"),  # OPERADORES DE ATRIBUICAO
    ("OPERADOR_ARITMETICO", r"([+\-*/%])"),  # OPERADORES ARITMETICOS
    ("PARENTESE_ESQUERDA", r"\("),
    ("PARENTESE_DIREITA", r"\)"),
    ("CHAVE_ESQUERDA", r"\{"),
    ("CHAVE_DIREITA", r"\}"),
    ("COLCHETE_ESQUERDA", r"\["),
    ("COLCHETE_DIREITA", r"\]"),
    ("VIRGULA", r","),
    ("PONTO_E_VIRGULA", r";"),
    ("DOIS_PONTOS", r":"),
    ("PONTO", r"\."),
    ("NOVA_LINHA", r"\n"),
    ("ESPACO_OU_TAB", r"[ \t]+"),
]


class Symbol:
    def __init__(self, value, name, line):
        self.value = value
        self.name = name
        self.line = line

    def __str__(self):
        return f"{self.value}"

    def mostrar_conteudo(self):
        print(self.value)
