from app import create_app
import datetime

app = create_app()


if __name__ == "__main__":
    # For development only
    app.run(debug=True, host="0.0.0.0", port=3000)
