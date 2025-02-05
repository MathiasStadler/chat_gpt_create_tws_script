# FROM HERE
# https://stackoverflow.com/questions/53517779/how-to-customize-matplotlib-multicursor

from matplotlib.widgets import MultiCursor
from matplotlib.widgets import *
from matplotlib.figure import Figure
class FigureCursor(Widget):
    def __init__(self, fig, horizOn=True, vertOn=True, useblit=True, **lineprops):
        self._cidmotion = None
        self._ciddraw = None
        self.background = None
        self.needclear = False
        self.visible = True
        self.canvas = fig.canvas
        self.fig = fig
        self.horizOn = horizOn
        self.vertOn = vertOn
        self.useblit = useblit
        self.vline, = fig.axes[0].plot([1, 1], [0., 1.], visible=vertOn, transform=self.fig.transFigure,
                                       clip_on = False, **lineprops)
        self.hline, = fig.axes[0].plot([0., 1.], [-1., 0.], visible=horizOn, transform=self.fig.transFigure,
                                       clip_on=False, **lineprops)
        self.connect()

    def connect(self):
        """connect events"""
        self._cidmotion = self.canvas.mpl_connect('motion_notify_event', self.onmove)
        self._ciddraw = self.canvas.mpl_connect('draw_event', self.clear)

    def disconnect(self):
        """disconnect events"""
        self.canvas.mpl_disconnect(self._cidmotion)
        self.canvas.mpl_disconnect(self._ciddraw)

    def clear(self, event):
        """clear the cursor"""
        if self.ignore(event):
            return
        if self.useblit:
            self.background = (
                self.canvas.copy_from_bbox(self.canvas.figure.bbox))
        for line in [self.vline, self.hline]:
            line.set_visible(False)

    def onmove(self, event):
        if self.ignore(event):
            return
        if event.inaxes is None:
            return
        if not self.canvas.widgetlock.available(self):
            return
        self.needclear = True
        if not self.visible:
            return
        trans = event.inaxes.transData + self.fig.transFigure.inverted()
        x_fig, y_fig = trans.transform([event.xdata, event.ydata])
        if self.vertOn:
            self.vline.set_xdata([x_fig, x_fig])
            self.vline.set_visible(self.visible)
        if self.horizOn:
            self.hline.set_ydata([y_fig, y_fig])
            self.hline.set_visible(self.visible)
        self._update()

    def _update(self):
        if self.useblit:
            if self.background is not None:
                self.canvas.restore_region(self.background)
            if self.vertOn:
                self.fig.draw_artist(self.vline)
            if self.horizOn:
                self.fig.draw_artist(self.hline)
            self.canvas.blit(self.canvas.figure.bbox)
        else:
            self.canvas.draw_idle()