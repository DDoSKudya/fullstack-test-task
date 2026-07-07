from dataclasses import dataclass


@dataclass(frozen=True)
class ScanContext:
    extension: str
    declared_mime: str
    size: int
    scan_max_bytes: int


def suspicious_extension(ctx: ScanContext) -> str | None:
    if ctx.extension in {".exe", ".bat", ".cmd", ".sh", ".js"}:
        return f"suspicious extension {ctx.extension}"
    return None


def oversized_file(ctx: ScanContext) -> str | None:
    return "file is larger than 10 MB" if ctx.size > ctx.scan_max_bytes else None


def pdf_mime_mismatch(ctx: ScanContext) -> str | None:
    if ctx.extension == ".pdf" and ctx.declared_mime not in {
        "application/pdf",
        "application/octet-stream",
    }:
        return "pdf extension does not match mime type"
    return None


RULES = [suspicious_extension, oversized_file, pdf_mime_mismatch]


def run_scan(ctx: ScanContext) -> tuple[str, str, bool]:
    reasons = [reason for rule in RULES if (reason := rule(ctx))]
    if reasons:
        return "suspicious", ", ".join(reasons), True
    return "clean", "no threats found", False
