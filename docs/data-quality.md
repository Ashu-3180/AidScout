# Data quality rules

The data-quality service reports, rather than silently fixes: missing scholarship name/provider, duplicate academic-year cycles, reversed dates, past deadlines on non-closed cycles, stale verified sources, missing official/provider/government sources, and conflicting values for the same claim key.

Freshness is configurable through `VERIFICATION_FRESHNESS_DAYS` (default 90). A source is only considered stale when it is marked `verified` and its `checked_at` is missing or older than that threshold. A URL never changes verification status by itself.

The service works on snapshots and is covered by database-independent unit tests. Production review policy can change severity or add rules without changing the normalized records.
