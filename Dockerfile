# Archi assistan
FROM python:slim
LABEL maekind.archi.name="archi" \
      maekind.archi.maintainer="Marco Espinosa" \
      maekind.archi.version="1.0" \
      maekind.archi.description="AI Assitant" \
      maekind.archi.email="hi@marcoespinosa.es"

# Install  programs
RUN apt update && apt install -y \ 
      gcc \ 
      swig \ 
      libpulse-dev \ 
      pulseaudio \  
      libportaudio2 \ 
      libportaudiocpp0 \ 
      libasound-dev \
      libsndfile1-dev \ 
      portaudio19-dev \
      python-all-dev \
      python3-all-dev \
      && apt autoremove \
      && rm -Rf /var/cache/apt/* \
      && rm -Rf /var/lib/apt/lists/* 


# Change working dir to app and copy requirements
WORKDIR /app
COPY requirements.txt requirements.txt

# Install requirements
RUN pip3 install -r requirements.txt

# Copy application into app dir
#COPY ./src/*.* .
#COPY ./data/*.* .

# Set working dir to path
ENV PATH="/app/archi/src:${PATH}"

# Entry command for docker image
ENTRYPOINT [ "main.py" ]







      

