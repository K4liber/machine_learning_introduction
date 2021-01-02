import subprocess
import sys


def main():
    cpus_set = {x/2 for x in range(10) if x != 0}

    if len(sys.argv) < 2:
        print("you should provide folder with images as a first argument")
        exit(1)

    images_dir: str = sys.argv[1]

    if images_dir[-1] != '/':
        images_dir = images_dir + '/'

    for cpus in cpus_set:
        cmd: str = 'sudo docker run -v ' + images_dir + ':/images/' \
                   ' --cpus="' + str(cpus) + '" face_recognition /images/ -f > ' + images_dir + \
                   'stats' + str(cpus).replace('.', '')
        print(cmd)
        return_code = subprocess.call(cmd, shell=True)
        print(return_code)


if __name__ == '__main__':
    main()
