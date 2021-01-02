# machine_learning_introduction
Build the image:   
`cd face_recognition`  
`docker build -t 'face_recognition' .`  
Run the script:  
`docker run -v <path_to_dir_with_images>:/images/ face_recognition /images/ -f > <output_file_path>`  
Single set run:  
`python single_set_run.py <path_to_dir_with_images>`  
Load data frame:  
`python load_data_frame.py <path_to_dir_with_sets>`  
Plot the data:  
`python plot_data.py <path_to_csv_data>`  
