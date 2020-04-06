from flask import Flask, render_template, request, jsonify
import sentiment
from sentiment import TwitterApp
import secret
import tweepy

app = Flask(__name__)

@app.route('/')
def index():
    if request.args.get('q'):
        search = request.args.get('q')
        #search = 'donald trump'
    
        api = TwitterApp()
        public_tweets = api.get_percentage(search,100)

        #return jsonify(public_tweets)

        #public_tweets = jsonify(public_tweets)
        return render_template('home.html', tweets=public_tweets)
    else:
        return render_template('home.html')
            

if __name__=='__main__':
	app.run(debug=True)