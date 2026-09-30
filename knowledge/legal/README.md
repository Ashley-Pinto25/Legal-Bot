# Legal knowledge corpus

This directory is intentionally empty until official materials are acquired and
reviewed. The former company-policy PDFs in `knowledge/` are preserved but are
not legal sources and are never queried by the Indian Legal Assistant.

To ingest a PDF, place it in an appropriate subdirectory and create a matching
`filename.metadata.json` sidecar. Required fields are `title`, `source_type`,
`source_url`, `official_source`, `status`, and `jurisdiction`. Add `act_name`,
`section`, `state`, `effective_from`, `effective_until`, `last_verified`, and
`document_id` whenever the source supplies them. Do not guess missing values.

Use `python scripts/ingest.py` from this directory. Ingestion refuses documents
without the required metadata and writes only to the `indian_legal_sources`
Chroma collection.
