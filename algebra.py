import argparse
import matplotlib.pyplot as plt
import math
import matplotlib as mpl
import numpy as np
import inspect
from matplotlib.widgets import TextBox

ap = argparse.ArgumentParser()
ap.add_argument('-s', '--start', help='Start of x', required=True)
ap.add_argument('-e', '--end', help='End of x', required=True)
ap.add_argument('-f', '--functions', help='List of functions', required=True)
args = vars(ap.parse_args())

###############################
# Straight from stackoverflow #
# https://stackoverflow.com/questions/4694478/center-origin-in-matplotlib
###############################

def center_spines(ax=None, centerx=0, centery=0):
    """Centers the axis spines at <centerx, centery> on the axis "ax", and
    places arrows at the end of the axis spines."""
    if ax is None:
        ax = plt.gca()

    # Set the axis's spines to be centered at the given point
    # (Setting all 4 spines so that the tick marks go in both directions)
    ax.spines['left'].set_position(('data', centerx))
    ax.spines['bottom'].set_position(('data', centery))
    ax.spines['right'].set_position(('data', centerx - 1))
    ax.spines['top'].set_position(('data', centery - 1))

    # Draw an arrow at the end of the spines
#     ax.spines['left'].set_path_effects([EndArrow()])
#     ax.spines['bottom'].set_path_effects([EndArrow()])

    # Hide the line (but not ticks) for "extra" spines
    for side in ['right', 'top']:
        ax.spines[side].set_color('none')

    # On both the x and y axes...
    for axis, center in zip([ax.xaxis, ax.yaxis], [centerx, centery]):
        # Turn on minor and major gridlines and ticks
        axis.set_ticks_position('both')
        axis.grid(True, 'major', ls='solid', lw=0.5, color='gray')
        axis.grid(True, 'minor', ls='solid', lw=0.1, color='gray')
        axis.set_minor_locator(mpl.ticker.AutoMinorLocator())

        # Hide the ticklabels at <centerx, centery>
        formatter = CenteredFormatter()
        formatter.center = center
        axis.set_major_formatter(formatter)

    # Add offset ticklabels at <centerx, centery> using annotation
    # (Should probably make these update when the plot is redrawn...)
    xlabel, ylabel = map(formatter.format_data, [centerx, centery])
    ax.annotate('(%s, %s)' % (xlabel, ylabel), (centerx, centery),
            xytext=(-4, -4), textcoords='offset points',
            ha='right', va='top')

class CenteredFormatter(mpl.ticker.ScalarFormatter):
    """Acts exactly like the default Scalar Formatter, but yields an empty
    label for ticks at "center"."""
    center = 0
    def __call__(self, value, pos=None):
        if value == self.center:
            return ''
        else:
            return mpl.ticker.ScalarFormatter.__call__(self, value, pos)

###########################
# Stackoverflow part ends #
###########################

def y(start, stop, function):
    for func in function:
        x = np.linspace(start, stop, 100)
        f = np.vectorize(func)
        y = f(x)
    
        plt.plot(x,y)
    
    center_spines()
    plt.axis('equal')
    plt.show()

def main():
    if args['start'] == None or args['end'] == None or args['functions'] == None:
        print('Error you did not set the correct flags')

    start = float(args['start'])
    end = float(args['end'])
    f = eval(args['functions'])

    y(start, end, f)

if __name__ == "__main__":
    main()