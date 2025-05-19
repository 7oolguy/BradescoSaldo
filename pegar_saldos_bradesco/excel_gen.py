import pandas as pd
import os
import openpyxl
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.worksheet.table import Table, TableStyleInfo

def salvar_como_excel(dados: list[dict[str, float]], nome_arquivo: str = "output.xlsx"):
    if not dados:
        print("Nenhum dado fornecido!")
        return

    # Verificar se o arquivo existe e está aberto
    if os.path.exists(nome_arquivo):
        try:
            with open(nome_arquivo, "r+") as f:
                pass  # Tentar abrir em modo leitura/escrita para verificar se está aberto
        except IOError:
            input(f"O arquivo '{nome_arquivo}' está aberto. Feche-o e pressione Enter para continuar...")

    # Converter lista de dicionários para DataFrame
    df = pd.DataFrame(dados)

    # Criar um novo arquivo Excel e planilha
    wb = Workbook()
    ws = wb.active
    ws.title = "Contas"

    # Adicionar dados do DataFrame à planilha
    for r in dataframe_to_rows(df, index=False, header=True):
        ws.append(r)

    # Definir o intervalo da tabela
    table_ref = f"A1:{chr(65 + len(df.columns) - 1)}{len(df) + 1}"
    tabela = Table(displayName="TabelaContas", ref=table_ref)

    # Aplicar estilo à tabela
    estilo = TableStyleInfo(name="TableStyleMedium9", showFirstColumn=False, showLastColumn=False,
                            showRowStripes=True, showColumnStripes=False)
    tabela.tableStyleInfo = estilo
    ws.add_table(tabela)

    # Ajustar automaticamente a largura das colunas
    for col in ws.columns:
        max_length = max((len(str(cell.value)) for cell in col if cell.value))
        col_letter = col[0].column_letter
        ws.column_dimensions[col_letter].width = max_length + 2

    # Salvar o arquivo Excel
    wb.save(nome_arquivo)
    print(f"Arquivo Excel salvo como {nome_arquivo}")
    # Abrir o arquivo automaticamente após salvar
    if os.name == 'nt':  # Windows
        os.startfile(nome_arquivo)
    elif os.name == 'posix':  # macOS or Linux
        import subprocess
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, nome_arquivo])
