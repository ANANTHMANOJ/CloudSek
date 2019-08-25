import wget                 #wget api to download fiel from given url
from postgres_connector_multi_threaded import PostgresConnector,ConnectionType            #api to connect to POSTGRESQL
import json                 #importing api for using  JSON




STATUS_DICT = dict()

#Download class has all the required function to download file from the url
class Download(object):
    def __init__(self, u_id, url):
        self.u_id = u_id
        self.url = url
        self.status_dict = dict()
        
#bar_custom function is called iteratively when wget.download() is ran, it updates the database with size of file remaining and finished
    def bar_custom(self, current, total, width=80):
        value = {"finished": current, "remaining": total - current}  # the dictionary containing the current and remaining file size 
        try:
            STATUS_DICT[self.u_id].update(value)
            self.u_id=str(self.u_id)
            print(value)
            value=json.dumps(value)
            res_con = PostgresConnector(ConnectionType.RESEARCHER)
            query5='''update  download_datas set value=%s where uid=%s'''
            print(value,self.u_id)
            res_con.execute(query5,(value,self.u_id))
            
        except KeyError:
            # query = f"update table set value = value"
            STATUS_DICT[self.u_id] = value
            
            
#following function is used for downloading by using wget
    def downloads(self):
        wget.download(self.url, bar=self.bar_custom)
        

        
#DownloadStatus class is used for giving the status updates of the downloads
class DownloadStatus(object):
    def __init__(self, u_id):
        self.u_id = u_id

    def status(self):
        res_con=PostgresConnector(ConnectionType.RESEARCHER)
        try:
            query6='''select value from download_datas where uid=%s'''     #getting the status of the file of given id
            rows=res_con.get(query6,(self.u_id))
        except TypeError:
            query=f"select value from download_datas where uid={0}".format(self.u_id)    #getting the status of the file of given id
            rows=res_con.get(query)
        
        if rows is None:
             return {"finished": 0, "remaining": 0}
            
        else:
            print(rows)
            return rows['value']
           
        


