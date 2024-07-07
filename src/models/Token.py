class Token:
    def __init__(self, token, linha, symbols_token):
        self.token = token
        self.linha = linha
        self.symbols_token = symbols_token

    def __dict__(self):
        return {
            "token": self.token,
            "linha": self.linha,
            "symbols_token": self.symbols_token,
        }

    def mostrar_conteudo(self):
        for symbol in self.symbols_token:
            print(symbol, end=" ")
