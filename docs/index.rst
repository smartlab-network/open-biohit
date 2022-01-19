Welcome to the biohit-pipettor documentation!
=============================================

.. toctree::
   :maxdepth: 2

This module is an unofficial Python interface for out Biohit Roboline devices.

Installation
------------

To install the package, execute ``pip install git+https://gitlab.gwdg.de/niklas.mertsch/biohit-pipettor-python``.
You will be prompted to enter your credentials for `gitlab.gwdg.de <https://gitlab.gwdg.de>`_.

Usage
-----

To control the pipetting robot, use the :py:class:`biohit_pipettor.Pipettor` class.

The following exceptions can occur:

    - :py:class:`biohit_pipettor.errors.NotConnected`: The device is not connected
    - :py:class:`biohit_pipettor.errors.CommandFailed`: The command failed to execute

Details about the errors are currently not provided. If you encounter errors and would like to receive more details, please let the maintainer know.

It is strongly recommended to use the Pipettor class as a `context manager <https://book.pythontips.com/en/latest/context_managers.html#context-managers>`_:

.. code-block::

    from biohit_pipettor import Pipettor

    with Pipettor() as p:
        p.initialize()
        p.move_xy(10, 10)
        ...

The Pipettor class
------------------

.. autoclass:: biohit_pipettor.Pipettor
