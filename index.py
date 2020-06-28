from flask import Flask, request, jsonify, render_template
import os
from recomender_system import Recomendacion as Recom
from filtering import Filtering

app = Flask(__name__)

#@app.route('/')
#def index():
#    return render_template('index.html')

@app.route('/get_movie_recomendation', methods=['POST'])
def get_movie_recomendation():

    global response
    data = request.get_json(silent=True, force=True)
    try:
        if data['queryResult']['action'] == str('id_usuario'):
            ## GET USER
            user = int(data['queryResult']['parameters']['id_usuario'])
            ## GET RECOMMENDATION
            get_movie_user = Filtering()
            response = get_movie_user.get_rec_movie(user)
            response = response.replace("{'", "")
            response = response.replace("'}", "")
            response = response.replace("', '", "  |  ")

        elif data['queryResult']['action'] == str('movies'):
            ## GET MOVIE
            movie = data['queryResult']['parameters']['movie']
            ## GET RECOMENDATION
            get_movie = Recom()
            response = get_movie.obten_recomendacion(movie)
            response = response.replace("['", "")
            response = response.replace("']", "")
            response = response.replace("', '", "  |  ")

    except:
        response = "En este momento no puedo entregarte una recomendación, intenta nuevamente"

    reply = {"fulfillmentText": response}
    return jsonify(reply)

# run Flask app
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get('PORT', 8080)))
