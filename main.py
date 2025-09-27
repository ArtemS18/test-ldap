from uvicorn import run
from app.web.app import setup_app


def main():
    app = setup_app()
    run(app, host=app.config.web.host, port=app.config.web.port)


if __name__ == "__main__":
    main()
