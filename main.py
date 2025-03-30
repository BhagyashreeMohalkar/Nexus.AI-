from app import app

# Allow gunicorn to access the app object directly
# This ensures compatibility between development and production

if __name__ == "__main__":
    # This block only runs when file is executed directly (not through gunicorn)
    app.run(host="0.0.0.0", port=5000, debug=True)