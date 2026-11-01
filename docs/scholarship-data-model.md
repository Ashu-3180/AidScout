# Scholarship data model

`scholarships` represents the enduring opportunity identity: canonical name, provider, description, intended audience, and record status. Its UUID is internal and stable; an application cycle is not its identity.

`scholarship_cycles` stores one historical, current, or future cycle per scholarship and academic-year label. Opening date and deadline are nullable because unknown is a valid state. The scholarship/year unique constraint prevents duplicate cycles.

`source_evidence` stores multiple evidence URLs for a scholarship and/or its cycle. A URL alone is never verification: verification status, checked-at time, publisher, source type, and notes are separately retained.

`eligibility_criteria` captures structured type, operator, JSON value, optional unit, required flag, and source evidence. `value_status=unknown` is explicit; a known value must be present. This model records evidence only and does not calculate eligibility.

All tables have UUID primary keys, timestamps, referential integrity, appropriate lookup indexes, and constraints for cycle date order, unique cycle years, source association, and known criterion values.
