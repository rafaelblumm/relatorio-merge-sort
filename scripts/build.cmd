@echo off
cd ..
docker build -t jupyter-notebook .
docker run --name relatorio-sort -p 8888:8888 jupyter-notebook
echo.
echo ** INFORMA��ES SOBRE O CONTAINER
echo.
docker stats --no-stream
cd scripts
