from statistics import mean, stdev
import matplotlib.pyplot as plt
import matplotlib.ticker as tck
from matplotlib.mlab import normpdf
import numpy as np
import datetime

### draw_graph
# filename - string. Can save different types of files based on filename ending.
# values - list of numbers between and including 0 to 100
# timestamps - optional list of numbers, same dimension as values. Without this, values will be evenly spaced.
# min - optional minimum moisture threshold, int between and including 0 to 100. None draws nothing.
# max - optional maximum moisture threshold, int between and including 0 to 100. None draws nothing.
# figsize - optional tuple of (width, height) of graph in inches. Defaults to 6.4, 4.8 with the default library style.
# dpi - optional dpi of graph, defaults to 100.
def draw_graph(filename, values, timestamps=None, min=None, max=None, figsize = None, dpi=None):
    assert(min is None or min >= 0 or min <= 100)
    assert(max is None or max >= 0 or max <= 100)
    assert(timestamps is None or len(values) == len(timestamps))

    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)

    ax.plot()

    if max is not None:
        plt.axhline(y=max, color='orange', label=f"Max: {max}%", linestyle='dotted')

    if min is not None:
        plt.axhline(y=min, color='orange', label=f"Min: {min}%", linestyle='dashed')


    if timestamps is None:
        plt.tick_params(
            axis='x',  # changes apply to the x-axis
            which='both',  # both major and minor ticks are affected
            bottom='off',  # ticks along the bottom edge are off
            top='off',  # ticks along the top edge are off
            labelbottom='off')  # labels along the bottom edge are off

        plt.plot(np.linspace(1, len(values) + 1, len(values)), values)
    else:
        lowest = np.amin(timestamps)
        highest = np.amax(timestamps)
        if highest - lowest < 60*60: # Hour
            time = lambda x, pos: datetime.datetime.fromtimestamp(x + lowest).strftime('%M:%S')
        elif highest - lowest < 60 * 60 * 24: # Day
            time = lambda x, pos: datetime.datetime.fromtimestamp(x + lowest).strftime('%H:%M:%S')
        elif highest - lowest < 60 * 60 * 24 * 31: # Month
            time = lambda x, pos: datetime.datetime.fromtimestamp(x + lowest).strftime('%a %d.')
        elif highest - lowest < 60 * 60 * 24 * 365: # Year
            time = lambda x, pos: datetime.datetime.fromtimestamp(x + lowest).strftime('%b-%d')
        else:
            time = lambda x, pos: datetime.datetime.fromtimestamp(x + lowest).strftime('%Y-%b')

        # Numpy magic. Numpy array <operator> number will apply that operation to every element in the array.
        timestamps = np.array(timestamps) - lowest
        ax.xaxis.set_major_formatter(tck.FuncFormatter(time))
        plt.plot(timestamps, values)

    plt.xlabel("Time")
    plt.ylabel("Humidity %")
    plt.legend(frameon=False)
    plt.ylim(0, 100)
    plt.savefig(filename, bbox_inches='tight')
    pass

#f = open("aksjekurser.txt")
#values = list(map(lambda l: l.strip(), f.readlines()))
#Yt = np.array([float(x)*100 for x in values])
#Xt = np.append(np.append(np.linspace(0, 100, 100), np.linspace(100, 160, 100)),(np.linspace(160, 30000000, 10000000)))

#print(values)

#draw_graph("figtest.png", Yt, timestamps=Xt[0:len(Yt)], min=20, max=80, figsize=(12.8, 4.8))
