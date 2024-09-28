from app import create_app
from waitress import serve
from urllib.error import HTTPError

# import concurrent.futures
# import threading

app = create_app()

if __name__ == "__main__":
    try:
        host = "0.0.0.0"
        port = 8080
        print(
            "Running application server in IP address {}, port {}...".format(host, port)
        )
        serve(app, host=host, port=port)
    except HTTPError as err:
        print(err)
