"""Extract declared text/page facts; inspect rasterized pages for visual clipping.

Development-only dependency: pypdf. This is not part of the installed skill.
"""

import json
import sys

from pypdf import PdfReader

reader = PdfReader(sys.argv[1])
print(
    json.dumps(
        {
            "pages": len(reader.pages),
            "text": "\n".join(page.extract_text() for page in reader.pages),
        }
    )
)
