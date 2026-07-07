from src.processing.rules import ScanContext, run_scan

SCAN_MAX = 10_485_760


def test_clean_text_file() -> None:
    ctx = ScanContext(
        extension=".txt",
        declared_mime="text/plain",
        size=100,
        scan_max_bytes=SCAN_MAX,
    )
    status, details, attention = run_scan(ctx)
    assert status == "clean"
    assert details == "no threats found"
    assert attention is False


def test_suspicious_extension() -> None:
    ctx = ScanContext(
        extension=".exe",
        declared_mime="application/octet-stream",
        size=100,
        scan_max_bytes=SCAN_MAX,
    )
    status, details, attention = run_scan(ctx)
    assert status == "suspicious"
    assert "suspicious extension .exe" in details
    assert attention is True


def test_oversized_file() -> None:
    ctx = ScanContext(
        extension=".txt",
        declared_mime="text/plain",
        size=SCAN_MAX + 1,
        scan_max_bytes=SCAN_MAX,
    )
    status, details, attention = run_scan(ctx)
    assert status == "suspicious"
    assert "larger than 10 MB" in details
    assert attention is True


def test_pdf_mime_mismatch() -> None:
    ctx = ScanContext(
        extension=".pdf",
        declared_mime="text/plain",
        size=100,
        scan_max_bytes=SCAN_MAX,
    )
    status, details, attention = run_scan(ctx)
    assert status == "suspicious"
    assert "pdf extension does not match mime type" in details
    assert attention is True
