io-object-detection
====
Transfer images from field location  to houston .

Data flow :
--------

![github_saleor_readmew_header_01](https://github.com/pravin1ambre/darknet/blob/master/Blank_Diagram.jpeg)


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
1] VSFTPD SERVER :
follow the steps in link we provided for installation of vsftpd server on machine  
https://www.digitalocean.com/community/tutorials/how-to-set-up-vsftpd-for-a-user-s-directory-on-debian-9  

2] GIT :
steps:
1. create folder with name io_object_detection  
2. clone project from git  
3. copy app folder from c: paste in io_object_detection folder


3] DOCKER :
steps:
1. Install Docker and docker-compose on machine
2. go to current directory
`` cd io_object_detection
``
3. run command on terminal/cmd
          start docker containers : docker-compose up
	  stop  docker containers : docker-compose down	

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

 
      



















