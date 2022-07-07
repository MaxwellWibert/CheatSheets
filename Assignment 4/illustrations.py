import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection
import matplotlib


BACKERSTYLE = mpatches.ArrowStyle('Simple', head_length=.25, head_width=.25, tail_width=.1)
TRACKERSTYLE = mpatches.ArrowStyle('Fancy', head_length=0.4, head_width=0.4, tail_width=0.2)

def heatmap(data, row_labels, col_labels, ax=None,
            cbar_kw={}, cbarlabel="", **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Parameters
    ----------
    data
        A 2D numpy array of shape (M, N).
    row_labels
        A list or array of length M with the labels for the rows.
    col_labels
        A list or array of length N with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if not ax:
        ax = plt.gca()

    ax.grid(which="minor", color="black", linestyle='-', linewidth=2)
    plt.rc('axes', axisbelow=True)
    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # Create colorbar
    #cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    #cbar.ax.set_ylabel(cbarlabel, rotation=0, va="bottom")

    # Show all ticks and label them with the respective list entries.
    ax.set_xticks(np.arange(data.shape[1]), labels=col_labels)
    ax.set_yticks(np.arange(data.shape[0]), labels=row_labels)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=0, ha="right",
             rotation_mode="anchor")

    # Turn spines off and create white grid.
    ax.spines[:].set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im#, cbar


def annotate_heatmap(im, data=None, valfmt="{x:.2f}",
                     textcolors=("red", "red"),
                     threshold=None, **textkw):
    """
    A function to annotate a heatmap.

    Parameters
    ----------
    im
        The AxesImage to be labeled.
    data
        Data used to annotate.  If None, the image's data is used.  Optional.
    valfmt
        The format of the annotations inside the heatmap.  This should either
        use the string format method, e.g. "$ {x:.2f}", or be a
        `matplotlib.ticker.Formatter`.  Optional.
    textcolors
        A pair of colors.  The first is used for values below a threshold,
        the second for those above.  Optional.
    threshold
        Value in data units according to which the colors from textcolors are
        applied.  If None (the default) uses the middle of the colormap as
        separation.  Optional.
    **kwargs
        All other arguments are forwarded to each call to `text` used to create
        the text labels.
    """

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max())/2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)

    return texts

def make_diagram(seq1, seq2, data, index, label="dummy", tracker_arrow=False, backer_arrows=None):
    #dot diagram data
    match_data = np.zeros((len(seq1)+1, len(seq2)+1))
    seq1 = " " + seq1
    seq2 = "_" + seq2
    for i, base1 in enumerate(seq1):
        for j, base2 in enumerate(seq2):
            if base1 == base2:
                match_data[i, j] = 1
    #dot diagram
    i, j = index
    plt.xticks(range(len(seq2)), labels=seq2)
    plt.yticks(range(len(seq1)), labels=seq1)
    fig, ax = plt.subplots()
    #im, cbar = heatmap(match_data, seq1, seq2, ax=ax, cmap='binary')
    im = heatmap(match_data, seq1, seq2, ax=ax, cmap='binary')
    texts = annotate_heatmap(im, data=data, valfmt="{x:.0f}", fontsize = 'xx-large')
    plt.gca().xaxis.tick_top()
    #tracker_arrow shows current cell.
    if(tracker_arrow):
        plt.annotate(' ', fontsize=20, 
        xy=(j,i), xycoords="data",
        xytext=(50,50), textcoords="offset points",
        arrowprops = dict(arrowstyle='simple', linewidth=5, color='blue'))
    #backer_arrows show shows backtracking path.
    if(backer_arrows is None):
        backer_arrows = []
    
    collection = PatchCollection(backer_arrows)
    plt.gca().add_collection(collection)

    plt.savefig(f'./illustrations/{label}.png')

    plt.close(fig)



UL = 0
U = 1
L = 2

match_score = 1
mismatch_score = -1
gap_penalty = -1

def s(a, b):
    if(a == b):
        return match_score
    else:
        return mismatch_score


seq1 = "GTTACC"
seq2 = "GTTGAC"

n = len(seq1)
m = len(seq2)
#matrix initialization
M = np.zeros(shape=(n+1, m+1, 2), dtype=np.int8)
arg_max = (0,0)
max_val = 0

make_diagram(seq1, seq2, data=M[:,:,0], index=(0,0), label="initializing_grid")

#matrix filling
for i in range(1, n+1):
    for j in range(1, m+1):
        ul = M[i-1][j-1][0] + s(seq1[i-1], seq2[j-1])
        l = M[i-1][j][0] + gap_penalty
        u = M[i][j-1][0] + gap_penalty
        
        M[i][j][0] = max(0, ul, u, l)
        tracker = np.argmax([ul, u, l])
        M[i][j][1] = tracker
        if(M[i][j][0] > max_val):
            max_val = M[i][j][0]
            arg_max = (i,j)

        A = (j,i)
        ULB = (j-1, i-1)
        UB = (j, i-1)
        LB = (j-1, i)
        

        backer_arrows = []
        
        arrow1 = mpatches.FancyArrowPatch(A, ULB, arrowstyle=BACKERSTYLE, color="green")
        arrow2 = mpatches.FancyArrowPatch(A, UB, arrowstyle=BACKERSTYLE, color="green")
        arrow3 = mpatches.FancyArrowPatch(A, LB, arrowstyle=BACKERSTYLE, color="green")
        
        backer_arrows.extend([arrow1, arrow2, arrow3])

        make_diagram(seq1, seq2, data=M[:,:,0], label= f'matrix-filling-{(i,j)}', index=(i, j), tracker_arrow=False, backer_arrows=backer_arrows)

#backtracking:
i, j = arg_max
end_i, end_j = arg_max

match_seq1 = ""
match_seq2 = ""

while(M[i][j][0] > 0):
    make_diagram(seq1, seq2, data=M[:,:,0], label=f'backtracking-{(i,j)}', index=(i, j), tracker_arrow=True)
    back_tracker = M[i][j][1]
    if(back_tracker == UL):
        i -= 1
        j -= 1
        match_seq1 = seq1[i] + match_seq1
        match_seq2 = seq2[j] + match_seq2
    elif(back_tracker == U):
        j -= 1
        match_seq1 = "-" + match_seq1
        match_seq2 = seq2[j] + match_seq2
    elif(back_tracker == L):
        i -= 1
        match_seq1 = seq1[j] + match_seq1
        match_seq2 = "-" + match_seq2

print(match_seq1)
print(match_seq2)


    
