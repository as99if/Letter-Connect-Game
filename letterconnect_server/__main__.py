from flask import Flask

from letterconnect_server.routes.api import api

app = Flask("__name__")

api(app)

if __name__ == "__main__":
    app.run(debug=False)
