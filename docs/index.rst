.. python-colorspace documentation master file, created by
   sphinx-quickstart on Fri Aug 31 21:18:17 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
   .. automodule:: imageio


Welcome to python-colorspace's documentation!
=============================================

``python-colorspace`` is a python package to create and handle colors and color
palettes in python. Based on the Hue-Chroma-Luminance (HCL) color space
effective color palettes can be designed and implemented in your own daily
workflow.

This package is based on the code and ideas of the
`R colorspace <https://cran.r-project.org/package=colorspace>`_ package
as it has often been requested by python enthusiasts. More information
and an interactive interface can also be found on
`HCLwizard.org <https://hclwizard.org>`_.

The package itself can be found on
`github <https://github.com/retostauffer/python-colorspace>`_ this documentation
is also available on `ReadTheDocs <https://python-colorspace.readthedocs.io>`_.




Contents
--------

.. toctree::
    :maxdepth: 2
    
    sec_gettingstarted
    sec_examples
    sec_reference
    sec_developer


Other Packages and Further Reading
----------------------------------

More information and further reading:

* `hclwizard.org <http://hclwizard.org>`_: more information about the HCL color
  space, introduction to the colorspace packages (in R and python), and some
  interactive tools to define effective HCL-based color palettes, pick colors,
  and check existing plots and figures for possible problems in terms of color
  vision deficiencies.
* `A list of scientific articles <http://www.hclwizard.org/references/>`_
  which provide more detailed insights, e.g.

* `The end of the rainbow <http://www.climate-lab-book.ac.uk/2014/end-of-the-rainbow/>`_:
  an open letter to the climate science community by 
  Ed Hawkins, Doug McNeall, David Stephenson, Jonny Williams & Dave Carlson.
* `Better Figures <https://betterfigures.org/>`_: Constructive criticism of the
  graphics of climate science by Doug McNeall.

Scientific articles with more detailed insights:

* Stauffer, R., Mayr, G. J., Dabernig, M., & Zeileis, A. (2015).  `Somewhere
  Over the Rainbow: How to Make Effective Use o f Colors in Meteorological
  Visualizations <http://doi.org/10.1175/BAMS-D-13-00155.1>`_.  Bulletin of the
  American Meteorological Society, 96(2), 203–216, doi:
  `10.1175/BAMS-D-13-00155.1 <http://doi.org/10.1175/BAMS-D-13-00155.1>`_.

* Zeileis, A., Hornik, K., & Murrell, P. (2009). `Escaping RGBland: Selecting
  colors for statistical graphics <http://doi.org/10.1016/j.csda.2008.11.033>`_.
  Computational Statistics &Amp; Data
  Analysis , 53(9), 3259–3270,
  doi:`10.1016/j.csda.2008.11.033 <http://doi.org/10.1016/j.csda.2008.11.033>`_.
* Ihaka, R., 2003.  `Colour for presentation graphics
  <http://www.ci.tuwien.ac.at/Conferences/DSC-2003/Proceedings/Ihaka.pdf>`_.  In:
  Hornik, K., Leisch, F., Zeileis, A. (Eds.), Proceedings of the 3rd
  International Workshop on Distributed Statistical Computing, Vienna, Austria,
  ISSN 1609-395X, URL:
  `<http://www.ci.tuwien.ac.at/Conferences/DSC-2003/Proceedings/Ihaka.pdf>`_.
* `And others <http://www.hclwizard.org/references/>`_ 
  (`hclwizard.org <http://hclwizard.org>`_ reference list).

Some other packages providing color maps in python (on top of the default color
maps) wich might be of interest:

* `seaborn <https://seaborn.pydata.org>`_:
  statistical data visualization. The package also provides access to a
  range of (mostly) well specified.
  `color palettes <https://seaborn.pydata.org/tutorial/color_palettes.html>`_.
* `palettable <https://jiffyclub.github.io/palettable>`_: color palettes for python.
  Formely known as ``brewer2mpl``. Provides a range of color palettes including
  "Brewer2" and "Carto" palettes.
* `ColorBrewer2.org <http://colorbrewer2.org>`_: the source of the brewer colors,
  interactive webpage by Cynthia Brewer, Mark Harrower and The Pennsylvania State University.

Known issues
------------

.. _index-known-issues:

.. warning::
    White point implemented but might require some additional testing.


TODO's
------

.. todolist::



