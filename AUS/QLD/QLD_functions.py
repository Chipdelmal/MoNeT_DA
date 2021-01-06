
###############################################################################
# Save Figure
###############################################################################
def quickSaveFig(filename, fig, dpi=750, transparent=True):
    fig.savefig(
         filename,
         dpi=dpi, facecolor=None, edgecolor=None,
         orientation='portrait', papertype=None, format='png',
         transparent=transparent, bbox_inches='tight', pad_inches=.02
     )