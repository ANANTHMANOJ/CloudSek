# CloudSek
#### Challenge  
  
  ### Installation:
  Following are needs to be installed to run this challenge:
  * Python IDE
  * Some external APIs: (run the commands given bellow)  
   ```
pip install flask  
pip install flask_limiter  
pip install hurry.filesize  
pip install wget  
pip intall psycopg2  
pip install json  
```
 
  * POSTGRESQL: After installing postgresql run the query present in database_sql.sql
  
## Getting Started
There are three python file.  
* **_flask_app.py_**:  
This contain all the main functions that is used to run RESTful api. It can used to download the file from the url and also for getting the status of the downloading file by using the help of other 2 python files.  
Methods has been implemented to _rate the limit_.
* **_views.py_**:  
This has the script of all the class that calls the api to download the file and to upload/updates the file status in the database. Another class takes the database and displays when requested
* **_postgres_connector_multi_threaded.py_**:  
Here the _multithreads_ along with connection to the POSTGRESQL database is made which can imported in other python files to execute queries.  
  
 As you run flask_app.py, run the following url in your browser:
 ```
 http://127.0.0.1:5000/index
 ```
 
Also a docker file along with requirement text has been given as the container.
###### A Demo video is also available for understaning ######
