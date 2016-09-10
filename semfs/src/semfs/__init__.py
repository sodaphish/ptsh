"""Expose SemFS as a FUSE file system.
"""
from SemFS import __version__, main

__all__ = ["FileSystem", "Database", "Catalog", "Base64", "SQL", "LogFile"]