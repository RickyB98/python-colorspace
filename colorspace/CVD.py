# All matrices in this file are adapted from https://github.com/njsmith/colorspacious/blob/master/colorspacious/cvd.py

#' Color Vision Deficiency (CVD) Conversion Tables
#' 
#' Conversion tables for simulating different types of color vision deficiency (CVD):
#' Protanomaly, deutanomaly, tritanomaly.
#' 
#' Machado et al. (2009) have established a novel model, that allows to handle normal color
#' vision, anomalous trichromacy, and dichromacy in a unified way. They also provide conversion
#' formulas along with tables of certain constants that allow to simulate various types of
#' CVD. See \code{\link{simulate_cvd}} for the corresponding simulation functions.
#' 

def deutan(cols, severity = 1.):

    from .CVD import CVD

    CVD = CVD(cols, "deutan", severity)
    return CVD.colors()

def protan(cols, severity = 1.):

    from .CVD import CVD

    CVD = CVD(cols, "deutan", severity)
    return CVD.colors()

def tritan(cols, severity = 1.):

    from .CVD import CVD

    CVD = CVD(cols, "deutan", severity)
    return CVD.colors()


class CVD(object):

    ALLOWED = ["protan", "tritan", "deutan"]
    
    def __init__(self, cols, type_, severity = 1):

        # Getting severity
        if severity < 0.:   severity = 0.
        elif severity > 1.: severity = 1.

        # Checking type
        if not type_.lower() in self.ALLOWED:
            raise ValueError("inpyt type_ to {:s} wrong. ".format(self.__class__.__name__) + \
                    "has to be one of: {:s}".format(", ".join(self.ALLOWED)))
        self._type_     = type_.lower()
        self._severity_ = severity

        # Convert
        from copy import deepcopy
        self._colors_   = deepcopy(cols)

    def _tomat_(self, x):
        from numpy import reshape, asarray
        return asarray(x, dtype = float).reshape((3,3))

    def protan(self, s):
        # Protan CVD
        x = []
        x.append(self._tomat_(( 1.000000,  0.000000, -0.000000, 0.000000,  1.000000,  0.000000, -0.000000, -0.000000,  1.000000)))
        x.append(self._tomat_(( 0.856167,  0.182038, -0.038205, 0.029342,  0.955115,  0.015544, -0.002880, -0.001563,  1.004443)))
        x.append(self._tomat_(( 0.734766,  0.334872, -0.069637, 0.051840,  0.919198,  0.028963, -0.004928, -0.004209,  1.009137)))
        x.append(self._tomat_(( 0.630323,  0.465641, -0.095964, 0.069181,  0.890046,  0.040773, -0.006308, -0.007724,  1.014032)))
        x.append(self._tomat_(( 0.539009,  0.579343, -0.118352, 0.082546,  0.866121,  0.051332, -0.007136, -0.011959,  1.019095)))
        x.append(self._tomat_(( 0.458064,  0.679578, -0.137642, 0.092785,  0.846313,  0.060902, -0.007494, -0.016807,  1.024301)))
        x.append(self._tomat_(( 0.385450,  0.769005, -0.154455, 0.100526,  0.829802,  0.069673, -0.007442, -0.022190,  1.029632)))
        x.append(self._tomat_(( 0.319627,  0.849633, -0.169261, 0.106241,  0.815969,  0.077790, -0.007025, -0.028051,  1.035076)))
        x.append(self._tomat_(( 0.259411,  0.923008, -0.182420, 0.110296,  0.804340,  0.085364, -0.006276, -0.034346,  1.040622)))
        x.append(self._tomat_(( 0.203876,  0.990338, -0.194214, 0.112975,  0.794542,  0.092483, -0.005222, -0.041043,  1.046265)))
        x.append(self._tomat_(( 0.152286,  1.052583, -0.204868, 0.114503,  0.786281,  0.099216, -0.003882, -0.048116,  1.051998)))
        return x[s]


    # deutan CVD
    def deutan(self, s):
        x = []
        x.append(self._tomat_(( 1.000000,  0.000000, -0.000000, 0.000000,  1.000000,  0.000000, -0.000000, -0.000000,  1.000000)))
        x.append(self._tomat_(( 0.866435,  0.177704, -0.044139, 0.049567,  0.939063,  0.011370, -0.003453,  0.007233,  0.996220)))
        x.append(self._tomat_(( 0.760729,  0.319078, -0.079807, 0.090568,  0.889315,  0.020117, -0.006027,  0.013325,  0.992702)))
        x.append(self._tomat_(( 0.675425,  0.433850, -0.109275, 0.125303,  0.847755,  0.026942, -0.007950,  0.018572,  0.989378)))
        x.append(self._tomat_(( 0.605511,  0.528560, -0.134071, 0.155318,  0.812366,  0.032316, -0.009376,  0.023176,  0.986200)))
        x.append(self._tomat_(( 0.547494,  0.607765, -0.155259, 0.181692,  0.781742,  0.036566, -0.010410,  0.027275,  0.983136)))
        x.append(self._tomat_(( 0.498864,  0.674741, -0.173604, 0.205199,  0.754872,  0.039929, -0.011131,  0.030969,  0.980162)))
        x.append(self._tomat_(( 0.457771,  0.731899, -0.189670, 0.226409,  0.731012,  0.042579, -0.011595,  0.034333,  0.977261)))
        x.append(self._tomat_(( 0.422823,  0.781057, -0.203881, 0.245752,  0.709602,  0.044646, -0.011843,  0.037423,  0.974421)))
        x.append(self._tomat_(( 0.392952,  0.823610, -0.216562, 0.263559,  0.690210,  0.046232, -0.011910,  0.040281,  0.971630)))
        x.append(self._tomat_(( 0.367322,  0.860646, -0.227968, 0.280085,  0.672501,  0.047413, -0.011820,  0.042940,  0.968881)))
        return x[s]


    # tritanomaly CVD
    def tritan(self, s):
        x = []
        x.append(self._tomat_(( 1.000000,  0.000000, -0.000000,  0.000000,  1.000000,  0.000000, -0.000000, -0.000000,  1.000000)))
        x.append(self._tomat_(( 0.926670,  0.092514, -0.019184,  0.021191,  0.964503,  0.014306,  0.008437,  0.054813,  0.936750)))
        x.append(self._tomat_(( 0.895720,  0.133330, -0.029050,  0.029997,  0.945400,  0.024603,  0.013027,  0.104707,  0.882266)))
        x.append(self._tomat_(( 0.905871,  0.127791, -0.033662,  0.026856,  0.941251,  0.031893,  0.013410,  0.148296,  0.838294)))
        x.append(self._tomat_(( 0.948035,  0.089490, -0.037526,  0.014364,  0.946792,  0.038844,  0.010853,  0.193991,  0.795156)))
        x.append(self._tomat_(( 1.017277,  0.027029, -0.044306, -0.006113,  0.958479,  0.047634,  0.006379,  0.248708,  0.744913)))
        x.append(self._tomat_(( 1.104996, -0.046633, -0.058363, -0.032137,  0.971635,  0.060503,  0.001336,  0.317922,  0.680742)))
        x.append(self._tomat_(( 1.193214, -0.109812, -0.083402, -0.058496,  0.979410,  0.079086, -0.002346,  0.403492,  0.598854)))
        x.append(self._tomat_(( 1.257728, -0.139648, -0.118081, -0.078003,  0.975409,  0.102594, -0.003316,  0.501214,  0.502102)))
        x.append(self._tomat_(( 1.278864, -0.125333, -0.153531, -0.084748,  0.957674,  0.127074, -0.000989,  0.601151,  0.399838)))
        x.append(self._tomat_(( 1.255528, -0.076749, -0.178779, -0.078411,  0.930809,  0.147602,  0.004733,  0.691367,  0.303900)))
        return x[s]

    def _interpolate_cvd_transform_(self):

        # Getting severity
        fun = getattr(self, self._type_)
        severity = self._severity_
        if severity <= 0.:
            cvd = fun(0)
        elif severity >= 1.:
            cvd = fun(10)
        else:
            from numpy import floor, ceil
            lo = int(floor(severity * 10.))
            hi = int(ceil(severity * 10.))
            if lo == hi:
                cvd = fun(lo+1) 
            else:
                cvd = (hi - severity * 10.) * fun(lo) + \
                      (severity * 10. - lo) * fun(hi)

        return cvd

    def _simulate_(self):
        """
        .. todo::
            Alpha handling in CVD._simulate_.
        """


        from copy import deepcopy
        cols = deepcopy(self._colors_)

        from .colorlib import colorobject

        if not isinstance(cols, colorobject):
            raise ValueError("input cols to {:s}".format(self.__class__.__name__) + \
                    "has to be a colorobject (e.g., CIELAB, RGB, hexcols).")

        # Convert to sRGB
        cols.to("sRGB")

        # Transform color
        from numpy import dot, vstack
        RGB = vstack([cols.get("R"), cols.get("G"), cols.get("B")])
        CVD = self._interpolate_cvd_transform_()

        [R, G, B] = dot(RGB, CVD)
        cols.set(R = R, G = G, B = B)

        return cols

    def colors(self):

        return self._simulate_()


# -------------------------------------------------------------------
# The desaturation function
# -------------------------------------------------------------------
def desaturate(col, amount = 1.):
    """Transform a vector of given colors to the corresponding colors
    with chroma reduced (by a tunable amount) in HCL space.

    The colors of the color object `col` are transformed to the HCL color
    space. In HCL, In HCL, chroma is reduced and then the color is transformed
    back to a colorobject of the same class as the input.

    Parameters:
        col (colorobject): a colorspace color object such as RGB, hexcols,
            CIELUV, ...
        amount (float): a value in [0.,1.] defining the degree of desaturation.
            `amount = 1.` removes all color, `amount = 0.` none.

    Returns:
        Returns the same object as input `col` but with desaturated color
        values.

    .. todo::
        Handling of alpha values.
    """


    if not isinstance(col, colorobject):
        import inspect
        raise ValueError("input to function {:s} ".format(inspect.stack()[0][3]) + \
                         "has to be of class colorobject (e.g., HCL, CIELUV, ...)")

    # Checking amount
    try:
        amount = float(amount)
    except Exception as e:
        import inspect
        raise ValueError("input amount to function {:s} ".format(inspect.stack()[0][3]) + \
                         "has to be a single float: {:s}".format(e))
    if amount < 0. or amount > 1.:
        import inspect
        raise ValueError("input amount to function {:s} ".format(inspect.stack()[0][3]) + \
                         "has to be in [0., 1.]")
    elif amount == 0.: return col

    # Keep original class
    original_class = col.__class__.__name__
    original_class = "hex" if original_class == "hexcols" else original_class

    from copy import deepcopy
    col = deepcopy(col)
    col.to("HCL")
    
    # Desaturation
    col.set("C", (1. - amount) * col.get("C"))

    from numpy import where, logical_or
    idx = where(logical_or(col.get("L") <= 0, col.get("L") >= 100))[0]
    if len(idx) > 0:
        C = col.get("C"); C[idx] = 0
        H = col.get("H"); H[idx] = 0
        col.set(C = C, H = H)

    col.to(original_class)

    # Return color object
    return col

