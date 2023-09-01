from main import app
#from main import celery



if __name__ == "__main__":
    app.run(
        host = "0.0.0.0",
        port=5000,
        debug = True
    )