@echo off
echo Testing File Upload API on Windows...

echo.
echo 1. Testing health endpoint:
curl -X GET "http://127.0.0.1:5000/health"

echo.
echo 2. Creating test files...

:: Create test.txt using copy con
echo Creating test.txt...
(
echo Hello World
echo This is a test file
echo With multiple lines
echo For testing purposes
) > test.txt

:: Create test.csv
echo Creating test.csv...
(
echo Name,Age,City
echo John,25,New York
echo Jane,30,London
echo Bob,35,Tokyo
) > test.csv

:: Verify files were created
echo.
echo Checking if files were created:
dir *.txt *.csv

echo.
echo 3. Uploading text file:
if exist test.txt (
    curl -X POST -F "file=@test.txt" "http://127.0.0.1:5000/upload"
) else (
    echo ERROR: test.txt was not created!
)

echo.
echo 4. Uploading CSV file:
if exist test.csv (
    curl -X POST -F "file=@test.csv" "http://127.0.0.1:5000/upload"
) else (
    echo ERROR: test.csv was not created!
)

echo.
echo 5. Cleaning up test files...
del test.txt
del test.csv

echo.
echo Test completed!
pause