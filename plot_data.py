import math
import sys

import pandas as pd
import numpy
import matplotlib.pyplot as plt
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV


def main():
    if len(sys.argv) < 2:
        print("you should provide data frame path as a first argument")
        exit(1)

    data_frame_path: str = sys.argv[1]
    headers = ['time', 'elements', 'total_size', 's3', 's4', 'cpus']
    df = pd.read_csv(data_frame_path, names=headers, sep=';')
    x = df['cpus']
    y = df['total_size']
    z = [math.log(time) for time in df['time']]
    print(df)
    # x, y = numpy.meshgrid(x, y)
    # plot
    ax = plt.axes(projection='3d')
    ax.plot_trisurf(x, y, z)
    # plt.plot(x, y, 'bo')
    # beautify the x-labels
    # ML
    svr = GridSearchCV(SVR(kernel='poly'),
                       param_grid={
                           "degree": [3],
                           "epsilon": [1e-2, 1e-1, 1e0],
                           # "C": [1e-3, 1e-2, 1e-1, 1e0, 1e1, 1e2, 1e3],
                           # "gamma": np.logspace(-2, 2, 5)
                       })
    X = df[['total_size', 'cpus']]
    svr.fit(X, z)
    z_svr = svr.predict(X)
    ax.plot_trisurf(x, y, z_svr)
    #ML end
    plt.gcf().autofmt_xdate()
    plt.show()


if __name__ == '__main__':
    main()




