[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/TbD6-EHn)

## Details of the assignment are mentioned in "assignment no 2.pdf"

create virtual environment using
`python -m venv .venv`

source this environment
`Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process`
`.\.venv\Scripts\Activate.ps1`

install all the dependencies
`pip install -r requirements.txt`

Test the application
`pytest test.py`

Build the docker image
`docker build -t anas-farooq8/flask-calculator-app .`

Run the Docker image
`docker run -d -p 5001:5001 anas-farooq8/flask-calculator-app`

Exposing the Jenkins using ngrok
`ngrok http 8080`

Testing Web-hook
