---
type: regex
target:
  source: file
  path: labelhub/labelhub/driver.py
pattern: '^import random\nimport time\n\n\ndef send_to_printer\(job_id: str, label: bytes, timeout: float\) -> bool:\n    """Stand-in for the vendor driver\."""\n    delay = random\.choice\(\[0\.2, 0\.3, 0\.4, 1\.8, 2\.6\]\)\n    time\.sleep\(min\(delay, timeout\)\)\n    return delay <= timeout\n$'
---
