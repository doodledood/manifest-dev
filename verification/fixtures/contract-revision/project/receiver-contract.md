# Receiver contract

The receiver accepts a UTF-8 JSON array of objects with exactly the keys id and label, both
strings. Its payload limit is 256 bytes. It imports the supplied records in array order.
No compression, references to another file, omitted fields, or abbreviated values are supported.
