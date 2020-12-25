import os
import sys


def main():
    if len(sys.argv) < 2:
        print("you should provide folder with images sets as a first argument")
        exit(1)

    images_sets_dir: str = sys.argv[1]
    frame_file_name: str = 'data_frame.csv'
    frame_file_path: str = os.path.join(images_sets_dir, frame_file_name)

    if os.path.exists(frame_file_path):
        os.remove(frame_file_path)

    if images_sets_dir == '' or not os.path.isdir(images_sets_dir):
        print('unknown dir "' + images_sets_dir + '"')
        exit(1)

    with open(frame_file_path, mode='w') as df:
        for folder_name in os.listdir(images_sets_dir):
            if 'set_' not in folder_name:
                continue

            set_path = os.path.join(images_sets_dir, folder_name)

            for filename in os.listdir(set_path):
                if 'stats' not in filename:
                    continue

                filepath = os.path.join(set_path, filename)
                cpus = float(filename[-2] + '.' + filename[-1])

                with open(filepath) as f:
                    data_frame_line = ';'.join([str(round(float(line.split(':')[1]), 2)) for line in f.readlines()])

                data_frame_line = data_frame_line + ';' + str(cpus) + '\n'
                df.write(data_frame_line)

    df.close()


if __name__ == '__main__':
    main()
