from myapp import app



@app.route("/healthcheck")
def healthcheck():
    return "OK", 200