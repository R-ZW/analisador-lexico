import re
import models.Symbol as model_symbol
import models.Tokenizador as model_tokenizador


class AnalisadorLexico:
    def __init__(self, symbols=model_symbol.SYMBOLS):
        self.regras = symbols
        self.regex_parts = [
            (name, re.compile(pattern)) for name, pattern in self.regras
        ]

    def le_token(self, codigo):
        # MOSTRANDO O CÓDIGO FONTE -----------------------------------------
        print(f"{"CÓDIGO FONTE".center(75, '=')}")
        print(codigo)
        print(f"{"".center(75, '=')}")
        # -----------------------------------------------------------------

        print(f"{"ANÁLISE".center(75, '=')}")
        symbols = self.identificar_symbols_basicos(codigo)

        if symbols != False:
            tokenizador = self.separar_symbols(symbols)
            valido = tokenizador.identificar_tokens()

            if valido != False:
                tokenizador.mostrar_tokens()

        print(f"{"".center(75, '=')}")


    def identificar_symbols_basicos(self, codigo):
        linha = 1
        ponteiro = 0
        symbols = []

        while ponteiro < len(codigo):
            correspondencia = None
            for nome_symbol, regex in self.regex_parts:
                correspondencia = regex.match(codigo, ponteiro)
                
                if correspondencia:
                    valor_symbol = correspondencia.group(0)
                    symbols.append(model_symbol.Symbol(valor_symbol, nome_symbol, linha))

                    if nome_symbol == "NOVA_LINHA":
                        linha += 1
                    break

            if not correspondencia:
                print(f"ERRO LÉXICO!!!!! -[ {codigo[ponteiro]} ]- LINHA {linha}")
                return False
            else:
                ponteiro = correspondencia.end(0)
                
        return symbols


    def separar_symbols(self, symbols_basicos):
        tokenizador = model_tokenizador.Tokenizador()

        for symbol in symbols_basicos:
            tokenizador.symbols.append(symbol)

        return tokenizador
