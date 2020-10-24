
from TestDataTable import TDT_Core

core = TDT_Core()

try:
	core.mainloop()
except KeyboardInterrupt:
	core.on_closing()
except Exception as e:
	core.debugmsg(1, "self.Exception:", e)
	core.on_closing()
