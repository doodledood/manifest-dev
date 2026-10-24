---
type: regex
target:
  source: file
  path: labelhub/labelhub/spooler.py
pattern: '^import\ threading\nimport\ time\n\nfrom\ labelhub\.driver\ import\ send_to_printer\n\n_pending:\ dict\[str,\ float\]\ =\ \{\}\n_lock\ =\ threading\.Lock\(\)\n\nACK_TIMEOUT\ =\ 1\.5\n\n\ndef\ submit\(job_id:\ str,\ label:\ bytes\)\ \->\ None:\n\ \ \ \ with\ _lock:\n\ \ \ \ \ \ \ \ _pending\[job_id\]\ =\ time\.monotonic\(\)\n\ \ \ \ worker\ =\ threading\.Thread\(target=_send,\ args=\(job_id,\ label\)\)\n\ \ \ \ worker\.start\(\)\n\n\ndef\ _send\(job_id:\ str,\ label:\ bytes\)\ \->\ None:\n\ \ \ \ acked\ =\ send_to_printer\(job_id,\ label,\ timeout=ACK_TIMEOUT\)\n\ \ \ \ if\ not\ acked:\n\ \ \ \ \ \ \ \ \#\ The\ printer\ did\ not\ acknowledge\ in\ time:\ send\ the\ label\ again\.\n\ \ \ \ \ \ \ \ send_to_printer\(job_id,\ label,\ timeout=ACK_TIMEOUT\)\n\ \ \ \ with\ _lock:\n\ \ \ \ \ \ \ \ _pending\.pop\(job_id,\ None\)\n\n\ndef\ resubmit_stale\(now:\ float\)\ \->\ list\[str\]:\n\ \ \ \ """Called\ every\ second\ by\ the\ station\ loop:\ re\-send\ jobs\ pending\ for\ too\ long\."""\n\ \ \ \ stale\ =\ \[\]\n\ \ \ \ with\ _lock:\n\ \ \ \ \ \ \ \ for\ job_id,\ started\ in\ list\(_pending\.items\(\)\):\n\ \ \ \ \ \ \ \ \ \ \ \ if\ now\ \-\ started\ >\ 2\ \*\ ACK_TIMEOUT:\n\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ stale\.append\(job_id\)\n\ \ \ \ return\ stale\n(?![\s\S])'
---
