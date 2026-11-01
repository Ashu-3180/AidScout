# Scholarship data model

`scholarships` represents the enduring opportunity identity: canonical name, provider, description, intended audience, and record status. Its UUID is internal and stable; an application cycle is not its identity.

`scholarship_cycles` stores one historical, current, or future cycle per scholarship and academic-year label. Opening date and deadline are nullable because unknown is a valid state. The scholarship/year unique constraint prevents duplicate cycles.

`source_evidence` stores multiple evidence URLs for a required scholarship owner and, optionally, one of its cycles. A composite foreign key prevents a cycle from being paired with a different scholarship. Deleting a cycle cascades only to its same-scholarship cycle-specific evidence; deleting a scholarship cascades only to its owned cycles, evidence, and criteria. A URL alone is never verification: verification status, checked-at time, publisher, source type, and notes are separately retained.

`eligibility_criteria` captures structured type, operator, JSON value, optional unit, required flag, and source evidence. Its optional cycle and evidence references are composite foreign keys that must belong to the criterion's scholarship. Those scoped relationships cascade only within the same scholarship owner, allowing a scholarship and its owned records to be removed together without affecting another scholarship. `value_status=unknown` requires a null value; `known` requires a value. A separate support status distinguishes supported, unknown, and unsupported criterion types. This model records evidence only and does not calculate eligibility or verification.

All tables have UUID primary keys, timestamps, referential integrity, appropriate lookup indexes, and constraints for cycle date order, unique cycle years, cross-scholarship ownership, and criterion value/support states.
