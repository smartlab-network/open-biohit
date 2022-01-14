import sys
from os.path import dirname, join

firmware_path = join(dirname(__file__), "include")
sys.path.append(firmware_path)

try:
    import clr

    clr.AddReference("InstrumentLib")
    from InstrumentLib import InstrumentCls

    clr_instrumentcls = InstrumentCls
finally:
    sys.path.remove(firmware_path)
