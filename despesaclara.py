"""
DespesaClara - Analisador de execução de despesa por órgão (Sprint 3)

Fluxo do programa (ver docs/Arquitetura.md):

    ENTRADA -> VALIDAÇÃO -> LEITURA -> FILTRO -> PROCESSAMENTO -> SAÍDA

Uso:
    python despesaclara.py caminho/do/arquivo.csv
    python despesaclara.py            (o programa pergunta o caminho)
"""
import csv
import os
import sys
from datetime import datetime
from decimal import Decimal, InvalidOperation

# --------------------------------------------------------------------------
# Constantes
# --------------------------------------------------------------------------
DELIMITADOR = ";"
COLUNAS_OBRIGATORIAS = [
    "Órgão Superior",
    "Valor Empenhado",
    "Valor Liquidado",
    "Valor Pago",
]
COLUNA_ORGAO = "Órgão Superior"
COLUNA_CODIGO = "Código Órgão Superior"
CABECALHO_RELATORIO = ["Órgão", "Total Empenhado", "Total Liquidado", "Total Pago"]
LARGURA_ORGAO = 50
ZERO = Decimal("0.00")


# --------------------------------------------------------------------------
# Erros do sistema
# --------------------------------------------------------------------------
class ArquivoInvalido(Exception):
    """O arquivo de entrada não pode ser usado na análise."""


class OperacaoCancelada(Exception):
    """O usuário escolheu não continuar."""


# --------------------------------------------------------------------------
# Componente 1 - Entrada (HU1 CA1 e HU2 CA1)
# --------------------------------------------------------------------------
def pegar_caminho(argumentos):
    """Devolve o caminho do CSV, vindo da linha de comando ou do terminal."""
    if argumentos:
        return argumentos[0]
    return input("Informe o caminho do arquivo CSV: ").strip()


def pedir_orgaos():
    """Pergunta quais órgãos analisar. Nomes ou códigos separados por ';'."""
    texto = input("Órgãos (nomes ou códigos separados por ';', vazio = todos): ")
    return [parte.strip() for parte in texto.split(";") if parte.strip()]


# --------------------------------------------------------------------------
# Componente 2 - Validação (HU1 CA2 a CA5)
# --------------------------------------------------------------------------
def _abrir_csv(caminho):
    """Abre o CSV tentando UTF-8 e, se não der, Latin-1 (padrão do Portal)."""
    for codificacao in ("utf-8-sig", "latin-1"):
        try:
            arquivo = open(caminho, newline="", encoding=codificacao)
            arquivo.read()  # força a decodificação para detectar erro agora
            arquivo.seek(0)
            return arquivo
        except UnicodeDecodeError:
            arquivo.close()
    raise ArquivoInvalido("Não foi possível ler a codificação do arquivo.")


def validar_arquivo(caminho):
    """Confere extensão e colunas obrigatórias. Devolve True se estiver tudo ok."""
    if not str(caminho).lower().endswith(".csv"):
        raise ArquivoInvalido(f"O arquivo precisa ter extensão .csv: {caminho}")

    try:
        with _abrir_csv(caminho) as arquivo:
            cabecalho = next(csv.reader(arquivo, delimiter=DELIMITADOR), [])
    except FileNotFoundError:
        raise ArquivoInvalido(f"Arquivo não encontrado: {caminho}")

    faltando = [c for c in COLUNAS_OBRIGATORIAS if c not in cabecalho]
    if faltando:
        raise ArquivoInvalido(
            "CSV incompatível. Colunas faltando: " + ", ".join(faltando)
        )

    print("Arquivo válido: validação concluída com sucesso.")
    return True


# --------------------------------------------------------------------------
# Componente 3 - Leitura
# --------------------------------------------------------------------------
def ler_dados(caminho):
    """Lê o CSV e devolve uma lista de linhas (cada linha é um dicionário)."""
    with _abrir_csv(caminho) as arquivo:
        return list(csv.DictReader(arquivo, delimiter=DELIMITADOR))


# --------------------------------------------------------------------------
# Componente 4 - Filtro (HU2 CA2 a CA5)
# --------------------------------------------------------------------------
def filtrar_orgaos(dados, orgaos):
    """Mantém só as linhas dos órgãos pedidos (por nome ou código)."""
    if not orgaos:
        resposta = input("Nenhum órgão informado. Processar todos? (s/n): ")
        if resposta.strip().lower() in ("s", "sim"):
            return list(dados)
        raise OperacaoCancelada("Operação cancelada pelo usuário.")

    resultado = []
    for pedido in orgaos:
        busca = pedido.strip().lower()
        encontradas = [
            linha
            for linha in dados
            if linha.get(COLUNA_ORGAO, "").strip().lower() == busca
            or linha.get(COLUNA_CODIGO, "").strip().lower() == busca
        ]
        if not encontradas:
            print(f"Aviso: órgão não encontrado no arquivo: {pedido}")
        for linha in encontradas:
            if linha not in resultado:
                resultado.append(linha)
    return resultado


# --------------------------------------------------------------------------
# Componente 5 - Processamento (HU3)
# --------------------------------------------------------------------------
def converter_valor(texto):
    """Converte '1.234,56' (padrão brasileiro) para Decimal. Vazio vira 0.00."""
    texto = (texto or "").replace("R$", "").strip()
    if texto == "":
        return ZERO
    try:
        valor = Decimal(texto.replace(".", "").replace(",", "."))
    except InvalidOperation:
        raise ArquivoInvalido(f"Valor monetário inválido: '{texto}'")
    return valor.quantize(Decimal("0.01"))


def somar_por_orgao(dados):
    """Soma empenho, liquidação e pagamento por órgão, cada um separado."""
    resumo = {}
    for linha in dados:
        orgao = linha[COLUNA_ORGAO].strip()
        total = resumo.setdefault(
            orgao, {"empenhado": ZERO, "liquidado": ZERO, "pago": ZERO}
        )
        total["empenhado"] += converter_valor(linha["Valor Empenhado"])
        total["liquidado"] += converter_valor(linha["Valor Liquidado"])
        total["pago"] += converter_valor(linha["Valor Pago"])
    return resumo


# --------------------------------------------------------------------------
# Componente 6 - Saída (HU4 e HU5)
# --------------------------------------------------------------------------
def _formatar_decimal(valor):
    """1500250.00 -> '1500250,00' (para o CSV)."""
    return f"{valor:.2f}".replace(".", ",")


def salvar_relatorio(resumo, pasta="."):
    """Grava relatorio_<data>.csv na pasta e devolve o caminho. Se não der
    para gravar, avisa o usuário e devolve None."""
    nome = "relatorio_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".csv"
    caminho = os.path.join(os.path.abspath(pasta), nome)
    try:
        with open(caminho, "w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.writer(arquivo, delimiter=DELIMITADOR)
            escritor.writerow(CABECALHO_RELATORIO)
            for orgao, total in resumo.items():
                escritor.writerow(
                    [
                        orgao,
                        _formatar_decimal(total["empenhado"]),
                        _formatar_decimal(total["liquidado"]),
                        _formatar_decimal(total["pago"]),
                    ]
                )
    except PermissionError:
        print(
            f"Erro: sem permissão para gravar {caminho}. "
            "Se o arquivo estiver aberto em outro programa, feche-o e tente de novo."
        )
        return None
    print(f"Relatório salvo em: {caminho}")
    return caminho


def formatar_moeda(valor):
    """1500250.00 -> 'R$ 1.500.250,00'."""
    texto = f"{valor:,.2f}"  # 1,500,250.00
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return "R$ " + texto


def abreviar_nome(nome, limite=LARGURA_ORGAO):
    """Corta nomes muito longos para a tabela não quebrar."""
    if len(nome) <= limite:
        return nome
    return nome[: limite - 3] + "..."


def imprimir_resumo(resumo):
    """Mostra a tabela comparativa no terminal, com uma linha de total."""
    largura_valor = 20
    cabecalho = (
        f"{'Órgão':<{LARGURA_ORGAO}} {'Empenhado':>{largura_valor}} "
        f"{'Liquidado':>{largura_valor}} {'Pago':>{largura_valor}}"
    )
    print(cabecalho)
    print("-" * len(cabecalho))

    total = {"empenhado": ZERO, "liquidado": ZERO, "pago": ZERO}
    for orgao, valores in resumo.items():
        print(
            f"{abreviar_nome(orgao):<{LARGURA_ORGAO}} "
            f"{formatar_moeda(valores['empenhado']):>{largura_valor}} "
            f"{formatar_moeda(valores['liquidado']):>{largura_valor}} "
            f"{formatar_moeda(valores['pago']):>{largura_valor}}"
        )
        for chave in total:
            total[chave] += valores[chave]

    print("-" * len(cabecalho))
    print(
        f"{'TOTAL':<{LARGURA_ORGAO}} "
        f"{formatar_moeda(total['empenhado']):>{largura_valor}} "
        f"{formatar_moeda(total['liquidado']):>{largura_valor}} "
        f"{formatar_moeda(total['pago']):>{largura_valor}}"
    )


# --------------------------------------------------------------------------
# Programa principal
# --------------------------------------------------------------------------
def main(argumentos=None):
    if argumentos is None:
        argumentos = sys.argv[1:]
    try:
        caminho = pegar_caminho(argumentos)
        validar_arquivo(caminho)
        dados = ler_dados(caminho)
        orgaos = pedir_orgaos()
        dados = filtrar_orgaos(dados, orgaos)
        if not dados:
            print("Nenhuma linha encontrada para os órgãos informados.")
            return 1
        resumo = somar_por_orgao(dados)
    except (ArquivoInvalido, OperacaoCancelada) as erro:
        print(f"Erro: {erro}")
        return 1

    salvar_relatorio(resumo)
    imprimir_resumo(resumo)
    return 0


if __name__ == "__main__":
    sys.exit(main())
