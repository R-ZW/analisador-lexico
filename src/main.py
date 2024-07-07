import os
import models.AnalisadorLexico as model_analisador_lexico


def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))

    file_name = input("Insira o nome do arquivo que deseja analisar: ")
    file_path = os.path.join(dir_path, "..", "ts", "test", file_name)

    with open(file_path, "r") as file:
        codigo = file.read()

    analisador_lexico = model_analisador_lexico.AnalisadorLexico()
    analisador_lexico.le_token(codigo)


if __name__ == "__main__":
    main()
