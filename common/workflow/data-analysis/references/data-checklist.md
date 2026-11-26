# Data analysis detailed checklists

## 1. Data inspection
- Identify source, format, size, sensitivity, and intended grain.
- Inspect columns, types, nulls, duplicates, ranges, and representative records.
- Do not infer semantics from column names alone; preserve a read-only snapshot when the source is important.

## 2. Schema validation
- Identify the authoritative schema and intended version (or mark an observed profile as provisional).
- Validate required fields, types, nullability, ranges, uniqueness, and relationships.
- Separate schema errors from record-level quality errors and reject incompatible data at the boundary.

## 3. Data cleaning
- Preserve the original input and record every transformation.
- Handle missing, duplicate, invalid, and inconsistent values explicitly; never silently drop or impute without documenting the rule.
- Measure before/after row counts and quarantine irreconcilable records.

## 4. Reproducible analysis
- Separate ingestion, transformation, analysis, and presentation.
- Make parameters, random seeds, and execution environment explicit.
- Re-run from a clean starting point and confirm equivalent results within stated tolerance.
