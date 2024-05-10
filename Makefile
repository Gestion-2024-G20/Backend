reset: 
	rm -f -r *.db fastapi_app/__pycache__

run: 
	xdg-open http://localhost:8000/docs
	poetry run python fastapi_app/app.py
runr: 
	rm -f -r *.db fastapi_app/__pycache__
	xdg-open http://localhost:8000/docs
	poetry run python fastapi_app/app.py

