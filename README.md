# Setup Database using Docker
### a. Pull MySQL image
`docker pull mysql:latest`
### b. Run MySQL Container
`docker run --name task-db -e MYSQL_ROOT_PASSWORD=admin1234 -e MYSQL_DATABASE=task -p 3306:3306 -d mysql:latest`

# Setup virtual environment
### a. Create virtual environment
`python -m venv [folder name]`
### b. Activate virtual environment
Windows `.\[folder name]\Scripts\activate`
### c. Install requirements.txt
`pip install -r requirements.txt`

# Run the application
`python .\main.py`