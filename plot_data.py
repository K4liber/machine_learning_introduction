import math
import sys
import copy

import pandas as pd
import numpy
import matplotlib.pyplot as plt
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from matplotlib import cm


def main():
    if len(sys.argv) < 2:
        print("you should provide data frame path as a first argument")
        exit(1)

    data_frame_path: str = sys.argv[1]
    headers = ['time', 'elements', 'total_size', 's3', 's4', 'cpus']
    df = pd.read_csv(data_frame_path, names=headers, sep=';')
    from sklearn.preprocessing import StandardScaler
    X_columns = ['elements', 'total_size', 's3', 's4', 'cpus']
    X = df[X_columns]
    Y = df[['time']]
    x = X['total_size']
    y = X['cpus']
    X_train, X_test, y_train, y_test = train_test_split(X, df[['time']], test_size=0.20, random_state=33)
    scalerX = StandardScaler().fit(X)
    scalery = StandardScaler().fit(Y)
    scaled_X_test = scalerX.transform(X_test)
    scaled_X = scalerX.transform(X)
    scaled_X_train = scalerX.transform(X_train)
    scaled_Y_train = scalery.transform(y_train)
    scaled_x_train_df = pd.DataFrame(scaled_X_train, columns=X_columns)
    scaled_y_train_df = pd.DataFrame(scaled_Y_train, columns=['time'])
    y_train_df = pd.DataFrame(y_train, columns=['time'])
    x_train = X_train['total_size']
    y_train = X_train['cpus']
    x_plot_test = X_test['total_size']
    y_plot_test = X_test['cpus']
    z_train = y_train_df['time']
    x_scaled = scaled_x_train_df['total_size']
    y_scaled = scaled_x_train_df['cpus']
    z_scaled = scaled_y_train_df['time']
    # plot
    ax = plt.axes(projection='3d')
    ax.set_xlabel('total size [B]')
    ax.set_ylabel('cpus')
    ax.set_zlabel('time [s]')
    ax.scatter(x_train, y_train, z_train, c='#2ca02c', alpha=1, label='training points')
    # ML
    svr = GridSearchCV(SVR(kernel='rbf'),
                       param_grid={
                           "gamma": [0.1],
                           "epsilon": [0.001],
                           "C": [300],
                       })
    # TODO what means this parameters above?
    svr.fit(scaled_X_train, z_scaled)
    z_svr = svr.predict(scaled_X)
    z_svr_test = svr.predict(scaled_X_test)
    z_svr_test_inverse = scalery.inverse_transform(z_svr_test)
    ax.scatter(x_plot_test, y_plot_test, z_svr_test_inverse, label='test points', c='#cc0000', alpha=1)
    y_test_list = list(y_test['time'])
    y_train_list = list(y_train)
    errors_rel = []
    errors = []

    for index, z_pred in enumerate(z_svr_test_inverse):
        z_pred = z_pred if z_pred > 0 else min(y_train_list)
        print('pred: %s' % z_pred)
        z_origin = y_test_list[index]
        print('origin: %s' % z_origin)
        error = abs(z_pred - z_origin)
        errors.append(error)
        print('error [s] = %s' % error)
        error_rel = error*100.0/z_origin
        errors_rel.append(error_rel)
        print('error relative [percentage] = %s' % error_rel)

    print('training set length: %s' % len(y_test_list))
    print('avg time [s] = %s' % str(sum(y_test_list) / len(y_test_list)))
    print('avg error [s] = %s' % str(sum(errors) / len(errors)))
    print('avg error relative [percentage] = %s' % str(sum(errors_rel) / len(errors_rel)))
    z_svr_inverse = scalery.inverse_transform(z_svr)
    print(x.shape)
    print(y.shape)
    print(z_svr_inverse.shape)
    ax.plot_trisurf(x, y, z_svr_inverse, alpha=0.5)
    #ML end
    plt.margins(tight=False)
    plt.gcf().autofmt_xdate()
    ax.legend()
    plt.show()


if __name__ == '__main__':
    main()




