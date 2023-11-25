from crypt import methods
from datetime import datetime
import json
from flask import Flask

from src.db.database import Database

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Kenken-gen API"


@app.route("/puzzle/<selected_date>", methods=["GET"])
def puzzle(selected_date):
    database = Database("./src/db/db.json")
    selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
    puzzle = database.get(selected_date)
    return json.dumps(puzzle)
