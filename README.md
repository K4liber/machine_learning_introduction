# machine_learning_introduction
Build the image:   
`cd face_recognition`  
`docker build -t 'face_recognition' .`  
Run the script:  
`docker run -v /home/jasiek/Pulpit/doktorat/machine_learning_introduction/faces_images:/images/ face_recognition /images/ -f > /home/jasiek/Pulpit/doktorat/machine_learning_introduction/faces_images/stats/time.txt`  
Single set run:  
`python single_set_run.py /home/jasiek/Pulpit/doktorat/set_8`  
Load data frame:  
`python load_data_frame.py /home/jasiek/Pulpit/doktorat`  
Plot the data:  
`python plot_data.py /home/jasiek/Pulpit/doktorat/data_frame.csv`  
