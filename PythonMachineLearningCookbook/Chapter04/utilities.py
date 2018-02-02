# ^_^ coding:utf-8 ^_^

import time
import requests
import numpy as np
import matplotlib.pyplot as plt
from sklearn import cross_validation

# 加载回归数据
def load_data(input_file):
    X = []
    with open(input_file, 'r') as f:
        for line in f.readlines():
            data = [float(x) for x in line.split(',')]
            X.append(data)

    return np.array(X)

# 雅虎财经数据接口
def  quotes_yahoo(ticker, begin, end):
    cookies = dict(B='79bclatd788ib&b=3&s=vt')
    crumb = 'x.eNt0GsePI'
    period1 = int(time.mktime(begin.timetuple()))
    period2 = int(time.mktime(end.timetuple()))
    url = '''https://query1.finance.yahoo.com/v7/finance/download/{0}?period1={1}&period2={2}&interval=1d&events=history&crumb={3}'''
    s = requests.Session()
    r = s.get(url.format(ticker, period1, period2, crumb), cookies=cookies)
    if r.text.startswith('{"chart":{"result":null,"error"'):
        raise IOError(r.text)

    quote = {}
    lines = r.text.split('\n')
    items = [item.lower() for item in lines[0].split(',')]
    for item in items:
        quote[item] = []
    for line in lines[1:-1]:
        i = 0
        for data in line.split(','):
            data = data.replace("'", "")
            try:
                quote[items[i]].append(float(data))
            except:
                quote[items[i]].append(data)
            i+=1
    return quote


# Plot the classifier boundaries on input data
def plot_classifier(classifier, X, y, title='Classifier boundaries', annotate=False):
    # define ranges to plot the figure 
    x_min, x_max = min(X[:, 0]) - 1.0, max(X[:, 0]) + 1.0
    y_min, y_max = min(X[:, 1]) - 1.0, max(X[:, 1]) + 1.0

    # denotes the step size that will be used in the mesh grid
    step_size = 0.01

    # define the mesh grid
    x_values, y_values = np.meshgrid(np.arange(x_min, x_max, step_size), np.arange(y_min, y_max, step_size))

    # compute the classifier output
    mesh_output = classifier.predict(np.c_[x_values.ravel(), y_values.ravel()])

    # reshape the array
    mesh_output = mesh_output.reshape(x_values.shape)

    # Plot the output using a colored plot 
    plt.figure()

    # Set the title
    plt.title(title)

    # choose a color scheme you can find all the options 
    # here: http://matplotlib.org/examples/color/colormaps_reference.html
    plt.pcolormesh(x_values, y_values, mesh_output, cmap=plt.cm.Set1)

    # Overlay the training points on the plot 
    plt.scatter(X[:, 0], X[:, 1], c=y, edgecolors='black', linewidth=2, cmap=plt.cm.Set1)

    # specify the boundaries of the figure
    plt.xlim(x_values.min(), x_values.max())
    plt.ylim(y_values.min(), y_values.max())

    # specify the ticks on the X and Y axes
    plt.xticks(())
    plt.yticks(())

    if annotate:
        for x, y in zip(X[:, 0], X[:, 1]):
            # Full documentation of the function available here: 
            # http://matplotlib.org/api/text_api.html#matplotlib.text.Annotation
            plt.annotate(
                '(' + str(round(x, 1)) + ',' + str(round(y, 1)) + ')',
                xy = (x, y), xytext = (-15, 15), 
                textcoords = 'offset points', 
                horizontalalignment = 'right', 
                verticalalignment = 'bottom', 
                bbox = dict(boxstyle = 'round,pad=0.6', fc = 'white', alpha = 0.8),
                arrowprops = dict(arrowstyle = '-', connectionstyle = 'arc3,rad=0'))

# Print performance metrics
def print_accuracy_report(classifier, X, y, num_validations=5):
    accuracy = cross_validation.cross_val_score(classifier, 
            X, y, scoring='accuracy', cv=num_validations)
    print("Accuracy: " + str(round(100*accuracy.mean(), 2)) + "%")

    f1 = cross_validation.cross_val_score(classifier, 
            X, y, scoring='f1_weighted', cv=num_validations)
    print("F1: " + str(round(100*f1.mean(), 2)) + "%")

    precision = cross_validation.cross_val_score(classifier, 
            X, y, scoring='precision_weighted', cv=num_validations)
    print("Precision: " + str(round(100*precision.mean(), 2)) + "%")

    recall = cross_validation.cross_val_score(classifier, 
            X, y, scoring='recall_weighted', cv=num_validations)
    print("Recall: " + str(round(100*recall.mean(), 2)) + "%")

