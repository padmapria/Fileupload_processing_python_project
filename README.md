
## File Processing Service with CI/CD pipeline

A Flask-based REST API for uploading, processing, and storing  processing results (line count, word count) in memory of text and CSV files. The service automatically counts lines and words in uploaded files and stores the processing results in an in-memory database with comprehensive logging and error handling.

### Processing results stored in memory
<img width="607" height="239" alt="image" src="https://github.com/user-attachments/assets/6fc77799-9cb2-4194-97c9-9ae971d5ace6" />

## Data Flow
- **Upload → User uploads .txt/.csv file**
- **Process → System counts lines and words**
- **Store Results → Only analysis results stored in memory**
- **Return → User gets record ID for retrieving results**
- **Retrieve → User can fetch processing results using record ID**

## 🚀 Features

- **File Upload**: REST endpoint for uploading files
- **File Validation**: Validates file types (.txt, .csv only)
- **File Processing**: Counts lines and words in uploaded files
- **Data Storage**: In-memory storage with unique record IDs
- **Comprehensive Logging**: Structured logging with class names and timestamps
- **Error Handling**: Graceful exception handling with user-friendly messages
- **Health Checks**: API health monitoring endpoint
- **RESTful API**: Clean API design with proper HTTP status codes
- **Docker Support**: Containerized deployment with Docker
- **CICD Configured**: github actions/dockerhub

## 🛠️ Tech Stack

- **Backend**: Python 3.9, Flask
- **File Processing**: Custom line/word counting logic
- **Logging**: Python logging with custom formatters
- **Containerization**: Docker, Docker Compose
- **Testing**: unittest, pytest
- **CI/CD**: github actions/dockerhub



## 📁 Project Structure
<img width="650" height="500" alt="image" src="https://github.com/user-attachments/assets/1084e8a6-1e7e-4b52-abcb-fdc3da41f4b4" />
<br/>
Project used as reference: https://github.com/padmapria/customerchurn_prediction_mlops_project


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

upgrade pip first </br>
------------------------
python -m pip install --upgrade pip
pip install -r requirements.txt   
python app.py

expected output </br>
--------------------
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:5000
* Running on http://[your-ip]:5000

Test the application </br>
--------------------
5. Run the test_api.bat located in the project folder, to test directly
   
6. Alternatively Test the application via postman as given in the below steps


	
way 2: For deployment on docker desktop in local machine
----------------------
1. Launch docker.Ensure Docker Desktop is running if you're on Windows.  

2. Run Docker Container:   
docker-compose up -d

3. To view logs of the docker container. Run the following command     
Find the Container ID or Name  by running the following command from command prompt:  
docker ps

Access Container Logs:    
Once you have the container ID or name, you can use the docker logs command to access the logs. For ex:    
docker logs <container_id_or_name>     
    

Test the application via postman
---------------------------------
## Health Check
Method: GET

URL: http://localhost:5000/health   <br/>
 <br/>
Expected Response: <br/>
 <br/>
<img width="600" height="460" alt="image" src="https://github.com/user-attachments/assets/e79e0fd0-4535-45db-97f7-6e3a704c85b9" />




## Upload File 
Method: POST

URL: http://localhost:5000/upload   <br/>
 <br/>
Expected Response: <br/>
Body: form-data   <br/>
Key: file (type: File)   <br/>
Value: Select your .txt or .csv file   <br/>

<br/>
<b> Sample postman output </b> 
<br/>
<img width="600" height="700" alt="image" src="https://github.com/user-attachments/assets/7886490d-1cca-4b74-97c6-e3482ea771ba" />



## Get Processing Record
Method: GET
URL: http://localhost:5000/records/{record_id}   <br/>
<br/>
Replace {record_id} with the ID from upload response <br/>
<br/>
<b> Sample postman output </b>  <br/>
<br/>
<img width="612" height="500" alt="image" src="https://github.com/user-attachments/assets/6312e984-a89f-403c-b521-b3fed7de3d76" />

 <br/>


After testing stop docker and cleanup the resources
---------------------------------------------------

8. To stop the docker container:     
docker compose down  

9. Remove all containers by stopping the container:
docker ps
docker stop <container_id>
docker system prune -a

### Deployment with github actions & Dockerhub CI/CD
-----------------------------------------
I have created a workflow located at the folder .github/workflows that triggers following actions one by one   

1. Code Setup and Configuration:   
The workflow triggers on push or pull request events to the master branch.   
It runs on an Ubuntu environment and sets up Python 3.9 for execution.   
Dependencies are installed using pip based on the requirements.txt file.   
 
2. Testing and Docker Deployment:   
Unit and integration tests are run using the run_tests.py script to ensure code correctness.   
Docker container is started and application is deployed in docker.   

3. Docker Container Execution:   
Once the application is up in docker, the image is pushed to dockerhub for deployment
<img width="700" height="700" alt="image" src="https://github.com/user-attachments/assets/30807f3b-41c4-4905-ba0d-12f208b43ca9" />



### Things to improve in the project
-----------------------------------------
1) To include Iaac like Terraform to deploy in AWS.

Our application has Memory-only storage - suitable for temporary processing needs  <br/>
2) Files are NOT stored - only processing results are kept in memory, we can configure db and store results in db    <br/>
3) Data is ephemeral - all results lost on application restart    <br/>
4) No file persistence - original files are processed and discarded   <br/>

