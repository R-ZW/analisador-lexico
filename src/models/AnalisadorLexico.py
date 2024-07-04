import re
import models.Symbol as model_symbol
import models.Row as model_row


class AnalisadorLexico:
    def __init__(self, symbols=model_symbol.SYMBOLS):
        self.regras = symbols
        self.regex_parts = [
            (name, re.compile(pattern)) for name, pattern in self.regras
        ]

    def le_token(self, codigo):
        symbols = self.identificar_symbols_basicos(codigo)

        for symbol in symbols:
            print(symbol)
        # rows = self.separar_rows(symbols)

        # for row in rows:
        #     row.identify()

    def identificar_symbols_basicos(self, codigo):
        linha = 1
        ponteiro = 0
        symbols = []
        while ponteiro < len(codigo):
            match = None
            for symbol_name, regex in self.regex_parts:
                match = regex.match(codigo, ponteiro)
                if match:
                    value = match.group(0)
                    symbols.append(model_symbol.Symbol(value, symbol_name, linha))
                    if symbol_name == "NOVA_LINHA":
                        linha += 1
                    break
            if not match:
                raise RuntimeError(f"Erro léxico: {codigo[ponteiro]}")
            else:
                ponteiro = match.end(0)
        return symbols

    def separar_rows(self, symbols_basicos):
        rows = []

        for symbol in symbols_basicos:
            row = model_row.Row()

            if symbol.get_symbol_name() != "NOVA_LINHA":
                row.symbols.append(symbol)
            else:
                rows.append(row)
                row = model_row.Row()

        return rows
