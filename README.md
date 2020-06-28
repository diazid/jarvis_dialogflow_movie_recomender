# jarvis_dialogflow_movie_recomender
Recomendador de Peliculas usando dialogflow

Elaborado por:
Andrea Faúndez
Israel Diaz
Marcelo Medel

Para el curso de Inteligencia Artificial Avanzada de la Universidad del Desarrollo. 

Instrucciones: 
1.- Crear ambiente python:
python3 -m venv nombre-del-ambiente

2.-activar el ambiente:
source nombre-del-ambiente/bin/activate

3.- Instalar flask:
pip install flask
export FLASK_APP:index.py
export FLASK_ENV:development

4.- Instalar Ngrok
Seguir las instucciones en el sitio web ngrok.com

5.- En una ventana del terminal:
flask run

6.- en otra ventana del terminal:
./ngrok http 5000
Esto generara un a dirección https la cual se usará como webhook en el área de fulfillment del bot en el dialogflow, 
la dirección deberá ser https://123dfg345df.ngrok.com/get_movie_recomendaton

7.- crear intents
se debe crear intents cuyo texto refiera al parametro @system.any:movie y el nombre de la accion del parametro será "movies".


