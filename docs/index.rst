Welcome to the biohit-pipettor documentation!
=============================================

.. toctree::
   :maxdepth: 2

This module is an unofficial Python interface for our Biohit Roboline devices.

Installation
------------

First, download the repository as zip file `here <https://gitlab.gwdg.de/umg-pharma-lab-automation/biohit-pipettor-python/-/archive/master/biohit-pipettor-python-master.zip>`_.
Then, execute ``pip install biohit-pipettor-python-master.zip``.

Usage
-----

To control the pipetting robot, use the :py:class:`biohit_pipettor.Pipettor` class.

Details about encountered errors are currently not provided.
If you encounter errors and would like to receive more details, please let the maintainer know.

All distance values are given or expected in millimeters, volumes are in microliters.
Exception: :py:func:`biohit_pipettor.Pipettor.move_piston` takes the piston position in steps of the internal step motor.

It is strongly recommended to use the Pipettor class as a `context manager <https://book.pythontips.com/en/latest/context_managers.html#context-managers>`_:
Otherwise, background threads might not be properly stopped when errors occur, preventing the program from terminating.

.. code-block::

    from biohit_pipettor import Pipettor

    with Pipettor(tip_volume=200, multichannel=False, initialize=True) as p:
        p.move_xy(10, 10)
        p.pick_tip(70)
        p.move_xy(25, 160)
        p.aspirate(50)
        p.move_xy(100, 60)
        p.dispense_all()
        ...

The Pipettor class
------------------

.. autoclass:: biohit_pipettor.Pipettor
