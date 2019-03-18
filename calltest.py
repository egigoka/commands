import subprocess
from commands import *

bench = Bench()
p = subprocess.Popen(["py", "sleeep.py"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)

# p
#_check_timeout
#_child_created
#_closed_child_pipe_fds
#_communicate
#_communication_started
#_execute_child
#_filter_handle_list
#_get_devnull
#_get_handles
#_handle
#_input
#_internal_poll
#_make_inheritable
#_readerthread
#_remaining_time
#_sigint_wait_secs
#_stdin_write
#_translate_newlines
#_wait
#_waitpid_lock
#args
#communicate
#encoding
#errors
#kill
#pid
#poll
#returncode
#send_signal
#stderr
#stdin
#stdout
#terminate
#text_mode
#universal_newlines
#wait

# p.stdout
#_checkClosed
#_checkReadable
#_checkSeekable
#_checkWritable
#_dealloc_warn
#_finalizing
#close
#closed - unusable
#detach
#fileno - unusable
#flush
#isatty
#mode
#name
#peek
#raw
#read
#read1
#readable - unusable
#readinto - unusable
#readinto1
#readline - unusable
#readlines - unusable
#seek - unusable
#seekable - unusable
#tell
#truncate
#writable
#write
#writelines
bench_close = Bench("timeout")
while bench_close.get() < 12:
    print(p.stdout.)
    bench.end(start_immediately=True)