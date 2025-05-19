@echo off
title Inicializando o Programa
REM Define a codificação para UTF-8 para suportar caracteres especiais
chcp 65001 > nul

REM --- Configuração ---
REM Define o diretório base como o diretório onde o .bat está localizado
set "DIRETORIO_BASE=%~dp0"
REM Define o nome do script Python a ser executado
set "PYTHON_SCRIPT=main.py"

REM --- Atualização do Python ---
echo Verificando e atualizando o Python...
REM Atualiza o Python para a versão mais recente disponível
winget upgrade python

REM --- Instalação de dependências ---
echo Instalando dependências do projeto...
REM Instala as bibliotecas listadas em requirements.txt
pip install -r "%DIRETORIO_BASE%requirements.txt"

REM --- Iniciar o Programa ---
echo Iniciando o programa...
REM Navega até o diretório do script Python
pushd "%DIRETORIO_BASE%"
REM Inicia o script Python em uma nova janela
start "" python "%PYTHON_SCRIPT%"

echo Programa iniciado com sucesso.
pause  REM Mantém a janela aberta para depuração
