SYMBOLS = [
    (
        "PALAVRA_CHAVE",
        r"\b(break|case|class|const|console|continue|debugger|default|delete|do|else|enum|export|extends|false|finally|for|function|if|import|in|instanceof|new|null|number|return|super|switch|this|throw|true|try|typeof|var|void|while|with|yield|interface|type|public|private|protected|readonly)\b",
    ),
    ("IDENFICADOR", r"[A-Za-z_$][A-Za-z0-9_$]*"),  # Identificadores
    ("NUMBER", r"\b\d+(\.\d*)?\b"),  # Números inteiros e flutuantes
    ("STRING", r"'[^'\\]*(\\.[^'\\]*)*'"),  # Strings
    ("TEMPLATE_STRING", r"`[^`\\]*(\\.[^`\\]*)*`"),  # Template literals
    ("OPERADOR", r"[+\-*/%&|^!=<>]=?|&&|\|\||\?\?|\?|:|\.{1,3}"),  # Operadores
    ("ATRIBUICAO", r"="),  # Atribuição
    ("PARENTESE_ESQUERDA", r"\("),  # Parêntese esquerdo
    ("PARENTESE_DIREITA", r"\)"),  # Parêntese direito
    ("CHAVE_ESQUERDA", r"\{"),  # Chave esquerda
    ("CHAVE_DIREITA", r"\}"),  # Chave direita
    ("COLCHETE_ESQUERDA", r"\["),  # Colchete esquerdo
    ("COLCHETE_DIREITA", r"\]"),  # Colchete direito
    ("VIRGULA", r","),  # Vírgula
    ("PONTO_VIRGULA", r";"),  # Ponto e vírgula
    ("DOIS_PONTOS", r":"),  # Dois pontos
    ("PONTO", r"\."),  # Ponto
    ("COMENTARIO", r"//.*"),  # Comentários de linha única
    (
        "COMENTARIO_MULTIPLAS_LINHAS",
        r"/\*[^*]*\*+(?:[^/*][^*]*\*+)*/",
    ),  # Comentários de múltiplas linhas
    ("NOVA_LINHA", r"\n"),  # Nova linha
    ("ESPACO_OU_TAB", r"[ \t]+"),  # Espaços e tabulações
]


class Symbol:
    def __init__(self, value, symbol_name, line):
        self.value = value
        self.symbol_name = symbol_name
        self.line = line

    def __str__(self):
        return f"SYMBOL->[{self.symbol_name}] | LINHA->[{self.line}] | VALUE->[{self.value}]"

    def get_symbol_name(self):
        return self.symbol_name
