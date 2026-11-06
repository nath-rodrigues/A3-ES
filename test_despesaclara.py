"""
Testes automatizados - DespesaClara (Sprint 2)

Escolhidos historias 1, 2 e 4

Cada teste verifica UM critério de aceitação de uma história de usuário.
Nome do teste:  test_hu<N>_ca<M>_<o_que_o_teste_confere>
    hu<N> = História de Usuário N
    ca<M> = Critério de Aceitação M dessa história


"""
import csv
from decimal import Decimal
from pathlib import Path

import pytest

try:
    import despesaclara as dc
except ImportError:  # Sprint 2: o código ainda não foi escrito

    class _ModuloAusente:
        """Faz cada teste falhar sozinho, com mensagem clara."""

        def __getattr__(self, nome):
            if nome.startswith("__"):
                raise AttributeError(nome)
            pytest.fail(f"Ainda não implementado: despesaclara.{nome} (Sprint 3)")

    dc = _ModuloAusente()

COLUNAS_OBRIGATORIAS = [
    "Órgão Superior",
    "Valor Empenhado",
    "Valor Liquidado",
    "Valor Pago",
]


# --------------------------------------------------------------------------
# Funções de apoio
# --------------------------------------------------------------------------
def _criar_csv(caminho, colunas, linhas=()):
    with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo, delimiter=";")
        escritor.writerow(colunas)
        escritor.writerows(linhas)
    return str(caminho)


def _linha(codigo, orgao, empenhado="0,00", liquidado="0,00", pago="0,00"):
    return {
        "Código Órgão Superior": codigo,
        "Órgão Superior": orgao,
        "Valor Empenhado": empenhado,
        "Valor Liquidado": liquidado,
        "Valor Pago": pago,
    }


def _dados_exemplo():
    return [
        _linha("26000", "Ministério da Educação", "100,00", "80,00", "50,00"),
        _linha("36000", "Ministério da Saúde", "200,00", "150,00", "120,00"),
        _linha("25000", "Ministério da Fazenda", "300,00", "250,00", "200,00"),
    ]


def _resumo_exemplo():
    return {
        "Ministério da Educação": {
            "empenhado": Decimal("1500250.00"),
            "liquidado": Decimal("1000000.00"),
            "pago": Decimal("900000.50"),
        },
        "Ministério da Saúde": {
            "empenhado": Decimal("2000.00"),
            "liquidado": Decimal("1500.00"),
            "pago": Decimal("1000.25"),
        },
    }


# ==========================================================================
# HU1 - Validação do Arquivo de Entrada
# ==========================================================================
def test_hu1_ca1_aceita_caminho_na_linha_de_comando():
    """HU1 CA1: o sistema recebe o caminho do arquivo pela linha de comando."""
    assert dc.pegar_caminho(["dados.csv"]) == "dados.csv"


def test_hu1_ca1_pede_caminho_no_terminal_se_nao_vier_argumento(monkeypatch):
    """HU1 CA1: sem argumento, o sistema pergunta o caminho no terminal."""
    monkeypatch.setattr("builtins.input", lambda *_: "dados.csv")
    assert dc.pegar_caminho([]) == "dados.csv"


def test_hu1_ca2_rejeita_arquivo_que_nao_e_csv(tmp_path):
    """HU1 CA2: rejeita o arquivo e mostra erro se a extensão não for .csv."""
    caminho = _criar_csv(tmp_path / "dados.txt", COLUNAS_OBRIGATORIAS)
    with pytest.raises(dc.ArquivoInvalido) as erro:
        dc.validar_arquivo(caminho)
    assert ".csv" in str(erro.value)


def test_hu1_ca3_aceita_csv_com_todas_as_colunas(tmp_path):
    """HU1 CA3: aceita o CSV quando todas as colunas obrigatórias existem."""
    caminho = _criar_csv(tmp_path / "ok.csv", COLUNAS_OBRIGATORIAS)
    assert dc.validar_arquivo(caminho) is True


def test_hu1_ca3_rejeita_csv_com_coluna_faltando(tmp_path):
    """HU1 CA3: rejeita o CSV quando falta alguma coluna obrigatória."""
    colunas = [c for c in COLUNAS_OBRIGATORIAS if c != "Valor Pago"]
    caminho = _criar_csv(tmp_path / "faltando.csv", colunas)
    with pytest.raises(dc.ArquivoInvalido):
        dc.validar_arquivo(caminho)


def test_hu1_ca4_erro_diz_quais_colunas_faltam(tmp_path):
    """HU1 CA4: a mensagem de erro diz exatamente quais colunas estão faltando."""
    caminho = _criar_csv(
        tmp_path / "faltando.csv", ["Órgão Superior", "Valor Empenhado"]
    )
    with pytest.raises(dc.ArquivoInvalido) as erro:
        dc.validar_arquivo(caminho)
    mensagem = str(erro.value)
    assert "Valor Liquidado" in mensagem
    assert "Valor Pago" in mensagem
    assert "Valor Empenhado" not in mensagem


def test_hu1_ca5_mostra_mensagem_de_sucesso(tmp_path, capsys):
    """HU1 CA5: arquivo válido mostra mensagem de sucesso e segue para a próxima etapa."""
    caminho = _criar_csv(tmp_path / "ok.csv", COLUNAS_OBRIGATORIAS)
    resultado = dc.validar_arquivo(caminho)
    texto = capsys.readouterr().out.lower()
    assert resultado is True
    assert "sucesso" in texto or "válido" in texto


# ==========================================================================
# HU2 - Seleção e Filtragem de Órgãos
# ==========================================================================
def test_hu2_ca1_aceita_varios_orgaos_no_terminal(monkeypatch):
    """HU2 CA1: permite digitar vários nomes ou códigos de órgãos."""
    monkeypatch.setattr(
        "builtins.input", lambda *_: "Ministério da Educação; 36000"
    )
    assert dc.pedir_orgaos() == ["Ministério da Educação", "36000"]


def test_hu2_ca2_busca_ignora_maiuscula_e_minuscula():
    """HU2 CA2: a busca ignora diferença entre letras maiúsculas e minúsculas."""
    resultado = dc.filtrar_orgaos(_dados_exemplo(), ["MINISTÉRIO DA EDUCAÇÃO"])
    assert len(resultado) == 1
    assert resultado[0]["Órgão Superior"] == "Ministério da Educação"


def test_hu2_ca3_avisa_quando_orgao_nao_existe(capsys):
    """HU2 CA3: mostra aviso se o órgão pedido não estiver no arquivo."""
    orgao_que_nao_existe = "Ministério da Magia"
    dc.filtrar_orgaos(
        _dados_exemplo(), [orgao_que_nao_existe, "Ministério da Saúde"]
    )
    assert orgao_que_nao_existe in capsys.readouterr().out


def test_hu2_ca4_mantem_so_as_linhas_dos_orgaos_pedidos():
    """HU2 CA4: depois do filtro, ficam só as linhas dos órgãos encontrados
    (busca por nome e por código)."""
    resultado = dc.filtrar_orgaos(
        _dados_exemplo(), ["Ministério da Educação", "36000"]
    )
    orgaos = {linha["Órgão Superior"] for linha in resultado}
    assert orgaos == {"Ministério da Educação", "Ministério da Saúde"}


def test_hu2_ca5_sem_filtro_usuario_aceita_e_processa_todos(monkeypatch):
    """HU2 CA5: sem filtro, o sistema pergunta; responder 's' processa todos."""
    monkeypatch.setattr("builtins.input", lambda *_: "s")
    assert len(dc.filtrar_orgaos(_dados_exemplo(), [])) == 3


def test_hu2_ca5_sem_filtro_usuario_recusa_e_cancela(monkeypatch):
    """HU2 CA5: sem filtro, responder 'n' cancela a operação."""
    monkeypatch.setattr("builtins.input", lambda *_: "n")
    with pytest.raises(dc.OperacaoCancelada):
        dc.filtrar_orgaos(_dados_exemplo(), [])



# ==========================================================================
# HU4 - Geração de Relatório CSV
# ==========================================================================
def test_hu4_ca1_relatorio_tem_so_as_quatro_colunas(tmp_path):
    """HU4 CA1: o CSV tem apenas Órgão, Total Empenhado, Total Liquidado e Total Pago."""
    caminho = dc.salvar_relatorio(_resumo_exemplo(), pasta=tmp_path)
    with open(caminho, newline="", encoding="utf-8-sig") as arquivo:
        colunas = next(csv.reader(arquivo, delimiter=";"))
    assert colunas == [
        "Órgão",
        "Total Empenhado",
        "Total Liquidado",
        "Total Pago",
    ]


def test_hu4_ca2_arquivo_salvo_na_pasta_com_prefixo_relatorio(tmp_path):
    """HU4 CA2: o arquivo é salvo na pasta de execução com o prefixo 'relatorio_'."""
    caminho = Path(dc.salvar_relatorio(_resumo_exemplo(), pasta=tmp_path))
    assert caminho.exists()
    assert caminho.parent == tmp_path
    assert caminho.name.startswith("relatorio_")
    assert caminho.suffix == ".csv"


def test_hu4_ca3_separa_colunas_com_ponto_e_virgula(tmp_path):
    """HU4 CA3: o separador é ';' para não confundir com a vírgula dos valores."""
    caminho = dc.salvar_relatorio(_resumo_exemplo(), pasta=tmp_path)
    with open(caminho, newline="", encoding="utf-8-sig") as arquivo:
        linhas = list(csv.reader(arquivo, delimiter=";"))
    assert len(linhas) == 3  # cabeçalho + 2 órgãos
    assert all(len(linha) == 4 for linha in linhas)


def test_hu4_ca4_mostra_o_caminho_do_arquivo_salvo(tmp_path, capsys):
    """HU4 CA4: mostra no terminal o caminho completo do arquivo salvo."""
    caminho = Path(dc.salvar_relatorio(_resumo_exemplo(), pasta=tmp_path))
    texto = capsys.readouterr().out
    assert str(tmp_path) in texto
    assert caminho.name in texto


def test_hu4_ca5_sem_permissao_pede_para_fechar_o_arquivo(
    tmp_path, capsys, monkeypatch
):
    """HU4 CA5: se não der para gravar (arquivo aberto em outro programa),
    mostra mensagem pedindo para fechar o arquivo, sem travar o programa."""

    def _negar_permissao(*args, **kwargs):
        raise PermissionError("arquivo em uso")

    with monkeypatch.context() as ajuste:
        ajuste.setattr("builtins.open", _negar_permissao)
        ajuste.setattr("io.open", _negar_permissao)  # usado pelo pathlib
        dc.salvar_relatorio(_resumo_exemplo(), pasta=tmp_path)

    assert "fech" in capsys.readouterr().out.lower()

