# docker que prepara un entorn basat en ubuntu amb python3, llibreries científiques
# i eines per treballar amb dades i fer peticions http
# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile

# imatge base d'Ubuntu 20.04 per l'arquitectura aarch64
FROM ghcr.io/home-assistant/aarch64-base-ubuntu:20.04
#FROM ghcr.io/home-assistant/aarch64-base-python:latest

# camí de bashio per utilitzar les funcions
ENV PATH="${PATH}:/usr/lib/bashio"

# actuatlitzem la llista de paquets
RUN apt update
RUN apt-get update

# instal·lem python3, pip i altres eines
RUN apt-get install dos2unix
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y 

#instal·lem llibreries de python per la gestió de dades i ML
#RUN apt install g++ gfortran pkgconfig cmake openblas openblas-dev
RUN pip install --upgrade pip

# Instal·la els paquets Python necessaris
RUN pip install scikit-learn psutil func_timeout requests numpy pandas pyswarms tomli

