import sys
from os.path import dirname, join

firmware_path = join(dirname(__file__), "firmware")
sys.path.append(firmware_path)
try:
    import clr
    clr.AddReference("InstrumentLib")
finally:
    sys.path.remove(firmware_path)
