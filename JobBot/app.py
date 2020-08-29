from datetime import datetime
from flask import Flask, render_template, request

from pymongo import MongoClient

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

app = Flask(__name__)

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.jobbot #Le nom de la base de données
conv = db.conv #Le nom de la collection
applicant = db.applicant
recruiter = db.recruiter
offre = db.offre

now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M")

bot = ChatBot("JobBot", read_only=True)


# =========================================================================================================
# 		Trainer du bot
# =========================================================================================================
conversation = [
	"Bonjour",
	"Bienvenue sur le site carrière d'Orange, quel est l'expérience dont vous bénéficiez pour le poste de community manager ?",
	"J'ai deux ans d'expérience à ce poste",
	"C'est noté, et quel est votre diplôme le plus haut concernant ce poste ?",
	"J'ai validé un Master en gestion de communauté",
	"Très bien, je ferai part de cette information au recruteur, souhaitez-vous nous informer d'autre chose ?",
	"Non, c'est bon pour moi",
	"Alors il ne me reste plus qu'à vous souhaiter une excellente journée, je transmet toutes les informations de notre échange au recruteur.",
]
trainer = ListTrainer(bot)
trainer.train(conversation)

# =========================================================================================================
# 		Routes
# =========================================================================================================


# Home -----------------------------------------------------------------------------------------------------

@app.route("/")
def home():
	return render_template("home.html")

# Bot -----------------------------------------------------------------------------------------------------

@app.route("/bot")
def index():
	return render_template("bot.html")

@app.route("/get")
def get_bot_response():

	userText = request.args.get('msg')
	botResponse = str(bot.get_response(userText))

	return botResponse

@app.route("/save")
def save():

	conv.insert_one({"cand":userText, "bot":botResponse, "date":dt_string})


# Recruteur ------------------------------------------------------------------------------------------------

@app.route("/recruiter")
def recruiter():

	convs = conv.find()
	recruiters = db.recruiter.find()[0]

	return render_template("recruiter.html", convs=convs, recruiters=recruiters)

# Nouvelles questions du Recruteur ------------------------------------------------------------------------------------------------

@app.route("/recruiter_new_questions")
def recruiter_new_questions():

	return render_template("questions.html")

# Postulant ------------------------------------------------------------------------------------------------

@app.route("/applicant")
def applicant():

	convs = conv.find()
	applicants = db.applicant.find()[0]

	return render_template("applicant.html", convs=convs, applicants=applicants)

# joblist ------------------------------------------------------------------------------------------------

@app.route("/joblist")
def joblist():

	offres = db.offre.find()[0]

	return render_template("joblist.html", offres=offres)

# offre ------------------------------------------------------------------------------------------------

@app.route("/offre")
def offre():

	offres = db.offre.find()[0]

	return render_template("offre.html", offres=offres)


# =========================================================================================================
# 		App
# =========================================================================================================

if __name__ == "__main__" :
	app.run(debug=True)
