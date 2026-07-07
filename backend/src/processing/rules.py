from dataclasses import dataclass

import filetype


@dataclass(frozen=True)
class ScanContext:
    extension: str
    declared_mime: str
    size: int
    scan_max_bytes: int
    detected_extension: str | None = None


def detect_extension(header: bytes) -> str | None:
    kind = filetype.guess(header)
    return None if kind is None else kind.extension


def suspicious_extension(ctx: ScanContext) -> str | None:
    if ctx.extension in {".exe", ".bat", ".cmd", ".sh", ".js"}:
        return f"suspicious extension {ctx.extension}"
    return None


def _human_size(n: int) -> str:
    return next(
        (
            f"{n // factor} {label}"
            for label, factor in (
                ("GB", 1 << 30),
                ("MB", 1 << 20),
                ("KB", 1 << 10),
            )
            if n >= factor and n % factor == 0
        ),
        f"{n} bytes",
    )


def oversized_file(ctx: ScanContext) -> str | None:
    if ctx.size <= ctx.scan_max_bytes:
        return None
    return f"file is larger than {_human_size(ctx.scan_max_bytes)}"


def pdf_mime_mismatch(ctx: ScanContext) -> str | None:
    if ctx.extension == ".pdf" and ctx.declared_mime not in {
        "application/pdf",
        "application/octet-stream",
    }:
        return "pdf extension does not match mime type"
    return None


def magic_bytes_mismatch(ctx: ScanContext) -> str | None:
    if not ctx.detected_extension or not ctx.extension:
        return None
    file_ext = ctx.extension.lstrip(".").lower()
    if ctx.detected_extension.lower() != file_ext:
        return f"file content looks like .{ctx.detected_extension}, not .{file_ext}"
    return None


RULES = [suspicious_extension, oversized_file, pdf_mime_mismatch, magic_bytes_mismatch]


def run_scan(ctx: ScanContext) -> tuple[str, str, bool, list[str]]:
    reasons = [reason for rule in RULES if (reason := rule(ctx))]
    if reasons:
        return "suspicious", ", ".join(reasons), True, reasons
    return "clean", "no threats found", False, []
