from typing import Callable, Literal, Tuple

from biohit_pipettor.clr_wrapping.instrument import InstrumentCls
from biohit_pipettor.errors import CommandFailed, CommandNotAccepted, NotConnected

MovementSpeed = Literal[1, 2, 3, 4, 5, 6, 7, 8, 9]
PistonSpeed = Literal[1, 2, 3, 4, 5, 6]


class Pipettor:
    __instrument: InstrumentCls

    def __init__(self):
        """
        Wraps the InstrumentLib .NET interface.

        CAUTION: If you use the bare initializer like `instrument = Pipettor()` and an exception occurs related to the
        instrument, the cleanup will fail and the program cannot close gracefully. Use it as a context manager instead:
        `with Pipettor() as instrument: ...`.
        """
        self.__instrument = InstrumentCls()

    @property
    def is_connected(self) -> bool:
        """True if the device is connected, False otherwise"""
        return self.__instrument.IsConnected() != 0

    @property
    def aspirate_speed(self) -> PistonSpeed:
        """The aspirate speed (1 to 6)"""
        return self.__instrument.Control.PollSpeed("P", inwards=True)

    @aspirate_speed.setter
    def aspirate_speed(self, aspirate_speed: PistonSpeed) -> None:
        self.__instrument.SetAspirateSpeed(aspirate_speed)

    @property
    def dispense_speed(self) -> PistonSpeed:
        """The dispense speed (1 to 6)"""
        return self.__instrument.Control.PollSpeed("P", inwards=False)

    @dispense_speed.setter
    def dispense_speed(self, dispense_speed: PistonSpeed) -> None:
        self.__instrument.SetDispenseSpeed(dispense_speed)

    @property
    def x_speed(self) -> MovementSpeed:
        """The X speed (1 to 9)"""
        return self.__instrument.Control.PollSpeed("X", False)

    @x_speed.setter
    def x_speed(self, x_speed: Literal[1, 2, 3, 4, 5, 6, 7, 8, 9]):
        self.__instrument.SetActuatorSpeed("X", x_speed)

    @property
    def y_speed(self) -> MovementSpeed:
        """The Y speed (1 to 9)"""
        return self.__instrument.Control.PollSpeed("Y", False)

    @y_speed.setter
    def y_speed(self, y_speed: Literal[1, 2, 3, 4, 5, 6, 7, 8, 9]):
        self.__instrument.SetActuatorSpeed("Y", y_speed)

    @property
    def z_speed(self) -> MovementSpeed:
        """The Z speed (1 to 9)"""
        return self.__instrument.Control.PollSpeed("Z", False)

    @z_speed.setter
    def z_speed(self, z_speed: Literal[1, 2, 3, 4, 5, 6, 7, 8, 9]):
        self.__instrument.SetActuatorSpeed("Z", z_speed)

    @property
    def x_position(self) -> float:
        """The X position, in millimeters"""
        return self.__instrument.PollPosition("X")

    @property
    def y_position(self) -> float:
        """The Y position, in millimeters"""
        return self.__instrument.PollPosition("Y")

    @property
    def z_position(self) -> float:
        """The Z position, in millimeters"""
        return self.__instrument.PollPosition("Z")

    @property
    def xy_position(self) -> Tuple[float, float]:
        """The X and Y position, in millimeters"""
        return self.x_position, self.y_position

    @property
    def piston_position(self) -> float:
        """The piston position, in millimeters"""
        return self.__instrument.PollPistonPosition()

    def initialize(self) -> None:
        """Initializes the instrument: reset errors, refresh slaves, initialize actuators"""
        self.__run(self.__instrument.InitializeInstrument)

    def move_z(self, z: float, wait: bool = True) -> None:
        """
        Move to the given Z position.

        :param z: The target Z position
        :param wait: if False, returns after sending the command to the device,
            else waits until target position is reached.
        """
        self.__run_with_wait(lambda wait: self.__instrument.MoveZ(z, wait), wait)

    def move_xy(self, x: float, y: float, wait: bool = True) -> None:
        """
        Move to the given X and Y position.

        :param x: The target X position
        :param y: The target Y position
        :param wait: if False, returns after sending the command to the device,
            else waits until target position is reached.
        """
        self.__run_with_wait(lambda wait: self.__instrument.MoveXY(x, y, wait), wait)

    def move_to_surface(self, limit: float, distance_from_surface: float) -> None:
        """
        Move Z in direction of `limit`, until either a surface was detected, or the `limit` was reached.
        If moving upwards, stops below the surface, else above it.

        :param limit: Direction and target position if no surface was detected
        :param distance_from_surface: Target distance from detected surface
        """
        self.__run(lambda: self.__instrument.MoveToSurface(limit, distance_from_surface))

    def move_piston(self, position: int) -> None:
        """
        Move piston to given position

        :param position: Target piston position, in steps
        """
        self.__run(lambda: self.__instrument.MovePistonToPosition(position))

    def aspirate(self, volume: float, wait: bool = True) -> None:
        """
        Aspirate the given volume

        :param volume: Volume, in milliliters
        :param wait: if False, returns after sending the command to the device,
            else waits until target position is reached.
        """
        self.__run_with_wait(lambda wait: self.__instrument.Aspirate(volume, wait), wait)

    def dispense(self, volume: float, wait: bool = True) -> None:
        """
        Dispense the given volume

        :param volume: Volume, in milliliters
        :param wait: if False, returns after sending the command to the device,
            else waits until target position is reached.
        """
        self.__run_with_wait(lambda wait: self.__instrument.Dispense(volume, wait), wait)

    def dispense_all(self) -> None:
        """Dispense all liquid from the tip"""
        self.__run(self.__instrument.DispenseAll)

    def pick_tip(self, limit: float) -> None:
        """
        Move downwards until a tip is picked up, or the `limit` is reached

        :param limit: Z limit
        """
        self.__run(lambda: self.__instrument.PickTip(limit))

    def eject_tip(self) -> None:
        """Eject the current tip"""
        self.__run(self.__instrument.EjectTip)

    def __run_with_wait(self, func: Callable[[bool], bool], wait: bool) -> None:
        """
        Run a InstrumentLib method with the wait parameter that returns True on success and False otherwise.

        :param func: The method, usually wrapped in a lambda
        :param wait: The wait parameter
        :raises NotConnected: If the device is not connected
        :raises CommandNotAccepted: If wait was False and the wrapped method returned False
        :raises CommandFailed: If wait was True and the wrapped method returned False
        """
        if not self.is_connected:
            raise NotConnected
        if func(wait):
            return
        if wait:
            raise CommandNotAccepted
        raise CommandFailed

    def __run(self, func: Callable[[], bool]) -> None:
        """
        Run a InstrumentLib method that returns True on success and False otherwise.

        :param func: The method, usually wrapped in a lambda
        :raises NotConnected: If the device is not connected
        :raises CommandFailed: If the wrapped method returned False
        """
        if not self.is_connected:
            raise NotConnected
        if not func():
            raise CommandFailed

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # when no exceptions occur, no explicit deletion is required
        # when a exception occurs, it has a reference to `self`, so the wrapped instrument is not disposed
        # by removing the instrument reference from `self`, its __del__ is called, and thus its Dispose() method
        del self.__instrument
