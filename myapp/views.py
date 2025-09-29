from myapp import app



@app.route('healtcheck')
def healthcheck():
    return "OK", 200