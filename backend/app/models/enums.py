from enum import Enum


class RecordStatus(str, Enum):
    draft = "draft"
    active = "active"
    archived = "archived"


class CycleStatus(str, Enum):
    planned = "planned"
    open = "open"
    closed = "closed"
    archived = "archived"


class SourceType(str, Enum):
    official = "official"
    provider = "provider"
    government = "government"
    secondary = "secondary"


class VerificationStatus(str, Enum):
    unverified = "unverified"
    verified = "verified"
    disputed = "disputed"
    stale = "stale"


class CriterionValueStatus(str, Enum):
    known = "known"
    unknown = "unknown"


class CriterionSupportStatus(str, Enum):
    supported = "supported"
    unknown = "unknown"
    unsupported = "unsupported"
