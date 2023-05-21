# Auto Emotion
## Detect faces and emotion and add into a simple sqlite db

## Steps to run
1. Create virtual environment by running `python -m venv .env`
2. Activate the virtual environment `.\.env\Scripts\activate` or `source .\.venv\bin\activate`
3. Install dependencies `pip install -r requirements.txt`
4. Add required images by creating folder in `training/<Preson name>`
5. Train the model using `python auto_emotion.py`
6. Initialize the database using `python db.py`
7. Run the project using `python app.py`
8. Goto `http://127.0.0.1:5000/` for detection 
