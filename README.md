io-object-detection
====
Transfer images from field location  to houston .

Data flow :
--------

[img]
![github_saleor_readmew_header_01](https://github.com/pravin1ambre/darknet/blob/master/Blank Diagram.jpeg)


About :
--------
This project mainly used for transfer images for one location to another as well as detect the objects inside the images 


Requirements:
----------
VSFTPD SERVER : install vsftpd server with user name eogftps  
GIT   
DOCKER 



Installation:
-------------



How to Use
-------------
import library as follows:   
``
        from io_notification_api.io_notification_api import io_notifications_api
``        
2. create a notify object:  
``        notify = io_notifications_api.notify
``        
3. Create a custom function which return either True or False as per your threshold.   
```
def myvar_gt_100(myvar_param):
    print("myvar value: {}".format(myvar_param))
    return myvar_param > 100
``` 

4. Create a global variable lets say myvar (or if you are getting from somewhere, just declare it global)
            global myvar
            myvar = 94
5. Use notify object created in step 2 to get notify:  
````
notify(name="myvar is greater than 100",notify_if_true=myvar_gt_100(myvar),func=myvar_gt_100,myvar=myvar, check_interval_seconds=1)   
 ````
name: It should be unique for all the notifications otherwise it will replace with previous task while
checking in interval.  
notify_if_true : User defined function with its variable. It should return True or False.
func :  User defined function name.   
myvar = User variable name (Don't forget to make it global)
check_interval_seconds : Check interval time in seconds.
changes can be made with which and be changes information 

6. Change myvar, if not changing automatically, use loop. 

    for i in range(10): 
           myvar += 1 
      
      time.sleep(2)      
      
Examples:

    from io_notification_api.io_notification_api import io_notifications_api, RabbitMQServer
    import time
    
    
    def myvar_gt_100():
      print("myvar value: {}".format(myvar))
      return myvar > 100
    
    global myvar
    myvar = 94
    
    
    notify = io_notifications_api.notify
    notify(name="myvar is greater than 100",func=myvar_gt_100, check_interval_seconds=1,filename="name")
    for i in range(10):
          myvar += 1
          time.sleep(2)





















