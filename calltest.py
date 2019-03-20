import subprocess
from commands import *

bench = Bench()
cmd = ["ping", "8.8.8.8"]

import asyncio
import sys
import time
from asyncio.subprocess import PIPE
from contextlib import suppress


class State:
    stdout = ""
    stderr = ""
    timeout_exception = False


def do_something(line):
    State.stdout += line.decode()
    print(line.decode(), end="")
    return True


def save_stderr(stderr):
    State.stderr = stderr.decode()
    print(f"stderr:{stderr.decode()}")


async def run_command(*args, timeout):
    # start child process
    # NOTE: universal_newlines parameter is not supported
    process = await asyncio.create_subprocess_exec(*args, stdout=PIPE, stderr=PIPE)

    # read line (sequence of bytes ending with b'\n') asynchronously
    endtime = time.monotonic() + timeout
    with suppress(ProcessLookupError):  # it throws if process already killed, but python try to kill it one more time
        while True:
            timeout = endtime - time.monotonic()
            try:
                line = await asyncio.wait_for(process.stdout.readline(), timeout)
            except asyncio.TimeoutError as exc:
                process.kill()
                save_stderr(await asyncio.wait_for(process.stderr.read(), timeout=1))
                State.timeout_exception = True
                break
            else:
                if not line:  # EOF
                    try:
                        process.kill()
                        save_stderr(await asyncio.wait_for(process.stderr.read(), timeout=1))
                    except TimeoutError:
                        pass
                    break
                elif do_something(line):
                    continue  # while some criterium is satisfied
            try:
                process.kill()
                save_stderr(await asyncio.wait_for(process.stderr.read(), timeout=1))
            except TimeoutError:
                pass
            process.kill()  # timeout or some criterium is not satisfied
            await process.communicate()
            break
    return await process.wait()  # wait for the child process to exit


if sys.platform == "win32":
    loop = asyncio.ProactorEventLoop()  # for subprocess' pipes on Windows
    asyncio.set_event_loop(loop)
else:
    loop = asyncio.get_event_loop()

return_code = loop.run_until_complete(run_command(*cmd, timeout=5))
print("return_code", return_code)
loop.close()
Print.debug("State.stdout", State.stdout, "State.stderr", State.stderr, "State.timeout_exception", State.timeout_exception)