# Customer interchange

The export is a JSON array in source order. Each record retains its `id` and `name` as strings.
An identifier's leading zeros are significant. An empty `note` means an explicitly cleared
note and stays an empty string. A missing `note` means no update and stays absent.
