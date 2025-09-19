from uvicorn import run
from app.web.app import setup_app


def main():
    app = setup_app()
    run(app, host="localhost", port=8082)


if __name__ == "__main__":
    main()
