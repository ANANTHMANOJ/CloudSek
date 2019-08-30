from flask import Flask                                #api for flask
from flask import request
from flask_limiter import Limiter 
from flask_limiter.util import get_remote_address 
from hurry.filesize import size
from postgres_connector_multi_threaded import PostgresConnector,ConnectionType            #api to connect to POSTGRESQL
                                       #api for connecting with POSTGRESQL
from views import Download, DownloadStatus              #importing the python script having required classes
                                           

#initializing for rate limits
app = Flask(__name__)
limiter= Limiter(                                       
        app,
        key_func=get_remote_address,
        default_limits=["200 per day","50 per hour"])

#The following funtion to download the file from given url
#It take the url from the form in html  through POST method, assigns the unique id and enters it into database
did=0
@app.route('/download',methods=["POST"])      # the code shown in the video uses POST method in HTML                               
def user_download():
    global did
    url = request.args['url']           # getting the url
    res_con=PostgresConnector(ConnectionType.RESEARCHER)
    query1="select count(*) from download_datas"
    rows=res_con.get(query1)['count']  
                # getting the number of rows already in database so that unique_id can be generated accordingly
    u_id=rows+1
    did=u_id
    query2 = '''insert into download_datas (uid) values (%s)'''
    res_con.execute (query2, str(u_id))     #inserting the id into the database
    msg = f"<h2>your file is downloaded and file Uid is : {u_id}</h2>"
    download_obj = Download(u_id, url)  
    download_obj.downloads()
    return msg

#function to display the status of download
@app.route('/status')
def download_status():
    u_id = request.args['id']        #getting the id of the download from the url, sent using get method
    status_obj = DownloadStatus(u_id)   
    status_dict = status_obj.status()    #initializing and calling the status() to get the status of the download of given id
    total=int(status_dict['finished'])+int(status_dict['remaining'])#calculating the total size of the file
    status="downloading..." if status_dict['remaining'] != 0 else "downloaded"
    invalid_msg= ''' <!DOCTYPE html>
    <html>
        <head>
        <style>
            .displaying
            {
             margin-top: 10%;
                margin-left: 25%;
                margin-right:25%;
              padding: 12px 6px;   
              border: 2px solid #ccc;
              border-radius: 4px;
              background-color: #f8f8f8;
              box-shadow: 0 8px 12px 0 rgba(0,0,0,0.24), 0 17px 50px 0 rgba(0,0,0,0.19);  
            }
        </style>
        </head>
    <body>
        <div class="displaying" >
             Invalid Id...Please close the tab
             </br>
         </div> 
   </body>
 </html>
'''
    msg1=  ''' <!DOCTYPE html>
                <html>
                    <head>
                        <style>
                        
                        
                        .displaying
                         {
                            margin-top: 10%;
                            margin-left: 25%;
                            margin-right:25%;
                            padding: 12px 6px;
                              border: 2px solid #ccc;
                              border-radius: 4px;
                              background-color: #f8f8f8;
                              box-shadow: 0 8px 12px 0 rgba(0,0,0,0.24), 0 17px 50px 0 rgba(0,0,0,0.19);
                         }
                        .msg{
                         margin-top: 5%;
                            margin-left: 20%;
                            font-size: 20px;
                        }
                        
                        .info{
                         margin-top: 5%;
                            margin-left:7%;
                            font-size: 25px;
                        }
                        button{
                            margin-left:40%;
                            
                            padding: 14px 40px;
                            border-radius: 12px;
                            border: 2px solid #4CAF50;
                        }
                        
                        .button2:hover {
                          box-shadow: 0 12px 16px 0 rgba(0,0,0,0.24), 0 17px 50px 0 rgba(0,0,0,0.19);
                        }
                        
                        
                        </style>
                        
                    </head>
                <body>
                  <div class="displaying" >
                      <div class="msg">
                          Status: '''+status+'''
                           </br>
                      </div> 
                  <div class="info"> '''+size(status_dict['finished'])+''' bytes of '''+size(total)+''' bytes ( remaining: '''+size(status_dict['remaining'])+''' )
                   </div>
                   </br>
                  <button class= "button2" type="submit"  onClick="refresh()">Refresh </button>
                  </div>
                <script type="text/javascript">
                  function refresh(){
                  window.location.reload();
                  }
                </script>
                </body>
                </html>
''' 
    if total==0:
        return invalid_msg
    else:
        return msg1







@app.route('/index')
def index():
    res_con=PostgresConnector(ConnectionType.RESEARCHER)
    query3="select count(*) from download_datas"
    rows=res_con.get(query3)['count']
    msg1=''' <!DOCTYPE html>
            <html>
            <head>
            <style>
            body
            {
             margin-top: 10%;
                margin-left: 25%;
                margin-right:25%;
              padding: 12px 6px;   
              border: 2px solid #ccc;
              border-radius: 4px;
              background-color: #f8f8f8;
              box-shadow: 0 8px 12px 0 rgba(0,0,0,0.24), 0 17px 50px 0 rgba(0,0,0,0.19);  
            }
            .inpt
            {
                margin-top: 2%;
                margin-left:20%;
                padding: 12px 20px;
                
                border-radius: 12px;
                box-sizing: border-box;
            }
            .btn
            {
               
                margin-left:3%;
                padding: 12px 20px;
                border-radius: 12px;
                border: 2px solid #4CAF50;
            }
            
            </style>
            </head>
            <body>
              <h1 style="margin-left:27%">Download Manager</h1>
             <form action="/download?url=" method="POST" target="_blank" id="my-form">
              <input type="text" name="reference-number" class="inpt" id="reference-number" placeholder="Enter the url" />
              
              <input type="submit" value="download" class="btn"/>
             </form>'''

    msg2='''</br><div class="msg" style="font-size:12px;margin-left:8%">
                ( There are '''+str(rows)+''' downloads.
                 Please enter the id (serial number) to view the status ``)
            </div>
              <form action="/status?id=" method="get" target="_blank" id="status" >
              <input type="number" name="id" id="status-number" class="inpt" placeholder="Enter the id" />
              
              <input type="submit" value="search" class="btn"/>
            </form>'''

    msg3='''<script type="text/javascript">
               var form1      = document.querySelector('#status'),
                  text_field1 = document.querySelector('#status-number'),
                 form       = document.querySelector('#my-form'),
                  text_field = document.querySelector('#reference-number');
            
              function submitHandler(){
              
                // build the new url and open a new window
                var url = form.action +  text_field.value;
                window.open(url);
            
                // prevent form from being submitted because we already 
                // called the request in a new window
               // return false;
              }
              
              function submitHandlerstatus(){
             
                // build the new url and open a new window
                var url1 = form1.action +  text_field1.value;
                window.open(url1);
            
                // prevent form from being submitted because we already 
                // called the request in a new window
               // return false;
              }
            
              // attach custom submit handler
              form.onsubmit = submitHandler;
              form1.onsubmit= submitHandlerstatus;
            </script>
            
            </body>
            </html>
            '''
    if rows ==0:
        return msg1+msg3
    else:
        return msg1+msg2+msg3

@app.errorhandler(500)
def not_found(error):
    if error==200:
        return
    else:
        res_con=PostgresConnector(ConnectionType.RESEARCHER)
        query4='''delete from download_datas where uid= (%s)'''                # connecting to database
        res_con.execute(query4,str(did))
        return '''<h2>Error: No file to download / permission not granted</h2>'''#+ repr(error)  
    
 
if __name__ == '__main__':  #main function
    app.run(host='0.0.0.0', port=5000)
