# Indian Legal Assistant

## Web workspace

The complete NyayaSetu React/TypeScript client and Node API are included in
`web/`. The direct-preview entry point is `web/client/preview.html`; it
connects to `scripts/legal_api.py` for local model-backed research intake.
The legacy `client/preview.html` remains only as the earlier static artifact.

Indian Legal Assistant is a source-grounded research tool that helps people
understand Indian laws, rights, procedures, and official legal resources that
may be relevant to a situation. It provides general legal information, not
legal representation or individualized legal advice.

## Safety and scope

- It never treats the old enterprise-support PDFs as legal authority.
- It queries a separate Chroma collection, `indian_legal_sources`, containing
  only legal documents deliberately ingested with required metadata.
- It does not fabricate Acts, provisions, cases, deadlines, authorities, or
  source links. Citations are constructed in Python only from retrieved
  document metadata.
- It prioritizes records marked `current`; unknown, repealed, and historical
  records are not used as a current-law answer.
- It asks for a state/union territory where location is material, retains only
  useful conversation context, and shows a concise disclaimer throughout.
- For immediate danger, arrest/custody, violence, serious criminal allegations,
  or urgent deadlines, seek the relevant authority, legal aid service, or a
  qualified advocate promptly.

## Architecture

```text
user situation
  → situation understanding + domain classification + jurisdiction check
  → clarification when a material fact is missing
  → legal-only semantic retrieval with status filtering
  → context builder → Gemini (optional) → validation → deterministic citations
```

The LangGraph workflow lives in `src/graph.py`. Gemini is lazy-initialized and
is optional: without `GOOGLE_API_KEY`, the app returns a truthful source-only
response instead of an uncited answer. The embedding model remains
`sentence-transformers/all-MiniLM-L6-v2`; no model change has been made.

## Run

```bash
cd Support-Bot
python -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env  # create this manually if you need Gemini synthesis
.venv/bin/streamlit run app.py
```

Set `GOOGLE_API_KEY` and optionally `GEMINI_MODEL` in your environment for
grounded synthesis. Do not commit credentials. Configuration such as `TOP_K`,
`CHUNK_SIZE`, `CHUNK_OVERLAP`, `CHROMA_PERSIST_DIRECTORY`, and `TEMPERATURE`
is centralised in `src/config.py`.

## Legal ingestion

The directory `knowledge/legal/` begins empty by design: this repository does
not invent legal documents. Add reviewed authoritative PDFs there with a
matching `.metadata.json` sidecar containing at least title, source type,
official URL, jurisdiction, and status. Then run:

```bash
.venv/bin/python scripts/ingest.py
```

See `knowledge/legal/README.md` for the metadata contract. The verified source
registry currently points to India Code, the Legislative Department, and NALSA;
it is a registry, not an indexed legal corpus.

The initial on-disk central-law corpus includes the Constitution, Bharatiya
Nyaya Sanhita, 2023, and any additional official PDFs listed in
`knowledge/legal/central/`. Run this audit before every embedding run:

```bash
.venv/bin/python scripts/audit_legal_corpus.py
```

`knowledge/legal/official_source_catalog.json` maps the authorised expansion
sources. It deliberately does not claim complete coverage: state legislation,
rules, gazette amendments, and judgments must be acquired and versioned per
source before they can be cited.

The app uses `sentence-transformers/all-MiniLM-L6-v2` for the local Chroma
adapter. A Gemini API embedding name (for example `models/gemini-embedding-2`)
is not compatible with that adapter and safely falls back to MiniLM.

## Test

```bash
.venv/bin/python -m pytest
```

Tests mock the absence of Gemini by exercising deterministic extraction,
classification, clarification routing, citation generation, and validation.
No API key or network request is required.

## Current limitations

No official statute or judgment has yet been copied into `knowledge/legal`, so
the app correctly returns "I could not verify this from the available legal
sources" for research requiring an indexed authority. To cover a topic, ingest
the current official text and preserve its version, effective-date, status,
jurisdiction, and source metadata. State legislation, regulations, case law,
OCR/DOCX/HTML extraction, hybrid keyword indexing, multilingual response
synthesis, and automatic source-update monitoring remain future work.
