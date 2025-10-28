@echo off
echo Instalando dependencias para el Books Scraper Dashboard...
echo.

:: Actualizar pip
echo Actualizando pip...
python -m pip install --upgrade pip
echo.

:: Instalar bibliotecas principales
echo Instalando requests...
pip install requests
echo.

echo Instalando beautifulsoup4...
pip install beautifulsoup4
echo.

echo Instalando pandas...
pip install pandas
echo.

echo Instalando streamlit...
pip install streamlit
echo.

echo Instalando plotly...
pip install plotly
echo.

echo Instalando matplotlib...
pip install matplotlib
echo.

echo Instalando lxml (parser alternativo)...
pip install lxml
echo.

:: Verificar instalaciones
echo Verificando instalaciones...
python -c "import requests; print('✓ requests instalado correctamente')"
python -c "import bs4; print('✓ beautifulsoup4 instalado correctamente')"
python -c "import pandas; print('✓ pandas instalado correctamente')"
python -c "import streamlit; print('✓ streamlit instalado correctamente')"
python -c "import plotly; print('✓ plotly instalado correctamente')"
python -c "import matplotlib; print('✓ matplotlib instalado correctamente')"
echo.

echo Todas las dependencias han sido instaladas correctamente.
echo.
echo Para ejecutar el dashboard, usa: streamlit run nombre_del_archivo.py
pause