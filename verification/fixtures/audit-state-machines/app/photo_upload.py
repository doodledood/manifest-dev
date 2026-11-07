class PhotoUpload:
    """Proof-of-delivery photo. The driver app shows a spinner while uploading or an error."""

    def __init__(self) -> None:
        self.uploading = False
        self.failed = False

    def start(self) -> None:
        self.uploading = True
        self.failed = False

    def on_error(self) -> None:
        self.uploading = False
        self.failed = True

    def retry(self) -> None:
        self.uploading = True

    def on_done(self) -> None:
        self.uploading = False

    def banner(self) -> str:
        if self.uploading:
            return "Uploading..."
        if self.failed:
            return "Upload failed - tap to retry"
        return ""
