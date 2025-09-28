## Goal of the project
# File Processing Service

A Flask-based REST API for uploading, processing, and storing  processing results (line count, word count) in memory of text and CSV files. The service counts lines and words in uploaded files and provides a in-memory storage solution for the analysis results.

# Processing results stored in memory
{
    'id': 'uuid-record-id',
    'filename': 'example.txt',
    'line_count': 15,           # Processing result
    'word_count': 250,          # Processing result  
    'timestamp': '2024-01-15T10:30:00'
}

## Data Flow
Upload → User uploads .txt/.csv file
Process → System counts lines and words
Store Results → Only analysis results stored in memory
Return → User gets record ID for retrieving results
Retrieve → User can fetch processing results using record ID

## 🚀 Features

- **File Upload**: REST endpoint for uploading files
- **File Validation**: Validates file types (.txt, .csv only)
- **File Processing**: Counts lines and words in uploaded files
- **Data Storage**: In-memory storage with unique record IDs
- **Comprehensive Logging**: Structured logging with class names and timestamps
- **Error Handling**: Graceful exception handling with user-friendly messages
- **Docker Support**: Containerized deployment with Docker
- **Health Checks**: API health monitoring endpoint
- **RESTful API**: Clean API design with proper HTTP status codes

## 🛠️ Tech Stack

- **Backend**: Python 3.9, Flask
- **File Processing**: Custom line/word counting logic
- **Logging**: Python logging with custom formatters
- **Containerization**: Docker, Docker Compose
- **Testing**: unittest, pytest

## 📁 Project Structure
file_processing_service/
├── app.py             # Main application entry point
├── Dockerfile         # Docker configuration
├── docker-compose.yml # Docker Compose setup
├── requirements.txt   # Python dependencies
├── run_tests.py       # Test runner to run both unit & integration tests
├── utils/
│ └── logger.py        # Centralized Logging configuration
├── api/
│ ├── controllers/
│ │ └── file_upload_controller.py  # API controllers
│ └── schemas.py                   # Response schemas
├── service/
│ └── file_processing_service.py   # Business logic layer
└── tests/
	├── unit/                      # Unit tests
	    └── test_file_processing_service.py   
	    └── test_file_upload_controller.py   
	└── integration/                # Integration tests
		 └── test_file_processor_app.py   
 
#### Detailed Workflow and Steps in the project
------------------------------------------------
The entire pipelisne can be executed by installing the dependencies from requirements.txt and running a Python files, with Docker running on the machine.
   
app.py - main class.   


### How to run the project in Windows Machine or AWS EC2 that have python 3.11, docker and github installed
-------------------------------------------------------------------------------------
1) Download the code from github
Open the command prompt and clone the project's GitHub repository using the following command:    
git clone git@github.com:padmapria/Fileupload_processing_python_project.git

2. Navigate to Project Folder from command prompt or Terminal:   
cd Fileupload_processing_python_project  

way 1: For manual deployment in local machine
-------------------------------------------
3. Install python in the pc & Ensure Python is added to PATH during installation

4. Install the required dependencies from requirements.txt and start the application from cmd prompt
# Upgrade pip first
python -m pip install --upgrade pip
pip install -r requirements.txt   
python app.py

Expected output
--------------------
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:5000
* Running on http://[your-ip]:5000
	
	
way 2: For manual deployment in docker desktop
----------------------
5. Launch docker.Ensure Docker Desktop is running if you're on Windows.  

6. Run Docker Container:   
docker-compose up -d

7. To view logs of the docker container. Run the following command     
Find the Container ID or Name  by running the following command from command prompt:  
docker ps

Access Container Logs:    
Once you have the container ID or name, you can use the docker logs command to access the logs. For ex:    
docker logs <container_id_or_name>     
    

Test the application via postman
---------------------------------
##Health Check
Method: GET

URL: http://localhost:5000/health

Expected Response:
{
    "status": "healthy",
    "service": "file-processing"
}


##Upload File
Method: POST

URL: http://localhost:5000/upload

Body: form-data
Key: file (type: File)
Value: Select your .txt or .csv file

Success Response:
{
    "status": "success",
    "data": {
        "record_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "filename": "test.txt",
        "results": {
            "line_count": 5,
            "word_count": 25
        }
    },
    "message": "File processed successfully"
}

##Get Processing Record
Method: GET
URL: http://localhost:5000/records/{record_id}
Replace {record_id} with the ID from upload response


After testing stop docker and cleanup the resources
---------------------------------------------------

8. To stop the docker container:     
docker compose down  

9. Remove all containers by stopping the container:
docker ps
docker stop <container_id>
docker system prune -a

### Deployment with github actions CI/CD
-----------------------------------------
I have created a workflow located at the folder .github/workflows that triggers following actions one by one   

1. Code Setup and Environment Configuration:   
The workflow triggers on push or pull request events to the master branch.   
It runs on an Ubuntu environment and sets up Python 3.9 for execution.   
Dependencies are installed using pip based on the requirements.txt file.   
 
2. Testing and Docker Deployment:   
Unit and integration tests are run using the run_tests.py script to ensure code correctness.   
If tests pass, the application is deployed into a Docker container.   

3. Docker Container Execution:   
Once the docker is up, we can push for deployment

### Things to improve in the project
1) To include Iaac like Terraform to deploy in AWS.

Our application has Memory-only storage - suitable for temporary processing needs
2) Files are NOT stored - only processing results are kept in memory, we can configure db and store in db
3) Data is ephemeral - all results lost on application restart
4) No file persistence - original files are processed and discarded

