import time
from RPLCD import CharLCD
from RPLCD import Alignment, CursorMode, ShiftMode
from RPLCD import cursor, cleared
c = CharLCD(0x27, rows=2, cols=16)
c.write_string('Raspberry Pi HD44780')
c.cursor_pos = (2, 0)
c.write_string('http://github.com/\n\rdbrgn/RPLCD')
c.close()
