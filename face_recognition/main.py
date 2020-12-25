import sys
import time
import face_recognition
import matplotlib
from matplotlib import pyplot, patches
import os

start_time = time.time()
all_files = 0
avg_size = 0.0
max_size = 0.0
total_size = 0.0
cpus = "0"

processed_part: str = '_processed.'


def faces_coords(filepath: str):
    image = face_recognition.load_image_file(filepath)
    return face_recognition.face_locations(image)


def main():
    if len(sys.argv) < 3:
        print("you should provide folder with images as a first argument")
        print("you should provide cpus fraction as a second argument")
        exit(1)

    photo_dir: str = sys.argv[1]
    global cpus
    cpus = sys.argv[2]

    if photo_dir == '' or not os.path.isdir(photo_dir):
        print('unknown dir "' + photo_dir + '"')
        exit(1)

    global all_files
    global max_size
    global total_size

    for photo_name in os.listdir(photo_dir):
        if processed_part in photo_name:
            continue

        if os.path.isdir(photo_dir + photo_name):
            continue

        if len(photo_name.split('.')) != 2:
            continue

        faced_photo_name = photo_name.split('.')[0] + processed_part + photo_name.split('.')[1]
        photo_path = photo_dir + photo_name
        faced_photo_path = photo_dir + faced_photo_name
        coords = faces_coords(photo_path)
        img = matplotlib.image.imread(photo_path)
        figure, ax = pyplot.subplots(1)
        ax.imshow(img)

        for i in range(len(coords)):
            x_start = coords[i][3]
            y_start = coords[i][0]
            x_width = (coords[i][1] - coords[i][3])
            y_height = (coords[i][2] - coords[i][0])
            rect = patches.Rectangle((x_start, y_start), x_width, y_height,
                                     edgecolor='r', facecolor="none")
            ax.add_patch(rect)

        pyplot.savefig(fname=faced_photo_path)
        file_size = os.path.getsize(photo_path)
        all_files += 1
        total_size += file_size

        if file_size > max_size:
            max_size = file_size

        pyplot.close(fig=figure)


if __name__ == "__main__":
    main()
    print("time: %s" % (time.time() - start_time))
    print("all_files: %s" % all_files)
    print("total_size: %s" % total_size)
    print("max_size: %s" % max_size)
    print("avg_size: %s" % str(total_size/float(all_files)))
    print("cpus: %s" % cpus)
