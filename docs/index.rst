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

Simulation
----------

You can use the class :py:class:`biohit_pipettor.PipettorSimulator` instead of :py:class:`biohit_pipettor.Pipettor` to check your pipetting routine for common errors.

It raises a :py:class:`RuntimeError` in the following situations:

- if used without context manager (works on real device, but should not be done)
- if ``tip_volume`` was not ``200`` or ``1000``
- if ``multichannel`` was ``True`` and ``tip_volume`` was ``200``
- if ``initialize`` was ``False`` (works on the real device, but simulation must start with no tip at position (0, 0, 0))
- if ``initialize()`` is executed while the pipettor has a tip
- if ``move_to_surface()`` is executed with a multi-channel pipette
- if ``move_to_surface()`` is executed while the pipettor has no tip
- if ``aspirate()`` is executed while the pipettor has no tip
- if ``aspirate()`` is executed with too much volume
- if ``dispense()`` is executed while the pipettor has no tip
- if ``dispense()`` is executed with more volume than currently is in the tip
- if ``dispense_all()`` is executed whiel the pipettor has no tip
- if ``pick_tip()`` is executed while the pipettor has a tip
- if ``eject_tip()`` is executed while the pipettor has no tip

It emits a :py:class:`UserWarning` in the following situations:

- if the pipettor has a tip at the end of the context manager
- if ``eject_tip()`` is executed and the tip is not empty
- if ``move_to_surface()`` is executed (only works if the device has a working tip sensor)
- if ``sensor_value`` is accessed (only works if the device has a working tip sensor)

Examples
^^^^^^^^

.. code-block:: python

    from biohit_pipettor import PipettorSimulator

    # error: no context manager
    p = PipettorSimulator(tip_volume=200, multichannel=False, initialize=True)
    p.move_xy(10, 20)

    # error: initialize must be True
    with PipettorSimulator(tip_volume=200, multichannel=False, initialize=False) as p:
        ...

    # error: aspirate requires a tip
    with PipettorSimulator(tip_volume=200, multichannel=False, initialize=True) as p:
        p.aspirate(100)

Static type checking
--------------------

You can use `mypy <https://github.com/python/mypy>`_ to check your code for type errors:

- Installation: ``pip install mypy``
- Check: ``mypy path/to/your/pipetting-script.py``

The Pipettor class
------------------

.. autoclass:: biohit_pipettor.Pipettor
