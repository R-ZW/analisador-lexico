import os
import models.AnalisadorLexico as model_analisador_lexico


def main():
    print("ANALISADOR LEXICO DE TYPESCRIPT".center(75, "="))
    print("O arquivo a ser analisado deve estar na pasta ts/test/".center(75, "-"))

    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_name = input("Insira o nome do arquivo que deseja analisar: ")
    file_path = os.path.join(dir_path, "..", "ts", "test", file_name)

    try:
        with open(file_path, "r") as file:
            codigo = file.read()
    except FileNotFoundError:
        print("Arquivo não encontrado em ts/test/!!!")
        return

    analisador_lexico = model_analisador_lexico.AnalisadorLexico()
    analisador_lexico.le_token(codigo)


if __name__ == "__main__":
    main()
