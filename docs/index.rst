Welcome to the biohit-pipettor documentation!
=============================================

.. toctree::
   :maxdepth: 2

This module is an unofficial Python interface for our Biohit Roboline devices.

Installation
------------

First, download the repository as zip file `here <https://gitlab.gwdg.de/umg-pharma-lab-automation/biohit-pipettor-python/-/archive/master/biohit-pipettor-python-master.zip>`_.
Then, execute ``pip install path\to\biohit-pipettor-python-master.zip``.

Usage
-----

To control the pipetting robot, use the :py:class:`biohit_pipettor.Pipettor` class.

The following exceptions can occur:

    - :py:class:`biohit_pipettor.errors.NotConnected`: The device is not connected
    - :py:class:`biohit_pipettor.errors.CommandFailed`: The command failed to execute

Details about the errors are currently not provided. If you encounter errors and would like to receive more details, please let the maintainer know.

All distance values are in millimeters, volumes are in microliters.
Exception: :py:func:`biohit_pipettor.Pipettor.move_piston` takes the piston position in steps of the internal step motor.

It is strongly recommended to use the Pipettor class as a `context manager <https://book.pythontips.com/en/latest/context_managers.html#context-managers>`_:

.. code-block::

    from biohit_pipettor import Pipettor

    with Pipettor(initialize=True) as p:
        p.move_xy(10, 10)
        p.pick_tip(70)
        p.move_xy(25, 160)
        ...

The Pipettor class
------------------

.. autoclass:: biohit_pipettor.Pipettor
