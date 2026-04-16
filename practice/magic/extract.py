import gdb

ge = gdb.execute
gp = gdb.parse_and_eval

class set_parm(gdb.Breakpoint):
    def __init__(self, bp_addr):
        super(set_parm, self).__init__(spec=f"*{bp_addr}")
        self.count = 0

    def stop(self):

        new_rsi = self.count
        ge(f"set $rsi = {new_rsi}")
        self.count += 1

        return False

class hook_retval(gdb.Breakpoint):
    def __init__(self, bp_addr):
        super(hook_retval, self).__init__(spec=f"*{bp_addr}")
        self.retval = []

    def stop(self):
        retval = int(gp("$rax")) & 0xFF
        self.retval.append(retval)
        return True

IMAGE_BASE = 0x555555554000
set_parm(IMAGE_BASE + 0x7ACAD)
hooker = hook_retval(IMAGE_BASE + 0x7ACB2)

INPUT_DUMMY = "0"*64
for i in range(0x100):
    ge("run <<<" + INPUT_DUMMY, to_string=True)

with open("table.txt", "w") as f:
    f.write("table = " + str(hooker.retval))
