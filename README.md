# machine_learning_introduction
Build the image:   
`cd face_recognition`  
`docker build -t 'face_recognition' .`  
Run the script:  
`docker run -v /home/jasiek/Pulpit/doktorat/machine_learning_introduction/faces_images:/images/ face_recognition /images/ -f > /home/jasiek/Pulpit/doktorat/machine_learning_introduction/faces_images/stats/time.txt`