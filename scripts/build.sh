cd ..
docker build -t jupyter-notebook .
docker run --name jpynb-container -p 8888:8888 jupyter-notebook
echo.
echo "** INFORMAÇÕES SOBRE O CONTAINER"
echo.
docker stats --no-stream
cd scripts
