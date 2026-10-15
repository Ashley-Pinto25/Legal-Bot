# NyayaSetu — Indian Law Research Workspace

NyayaSetu is a React + Node.js legal-research workspace for lawyers and citizens. The Python package remains available for legal RAG and ingestion support; its Streamlit UI has been retired. The supported application is the React workspace in `client/` with the Node API in `server/`.

## What is implemented

- React + TypeScript legal-tech chat interface styled with Tailwind utilities, using a WhatsApp-like threaded-chat layout, responsive conversation sidebar, persistent account-backed history, citations, source links, legal disclaimer, and sign-up/sign-in.
- Node/Express API with bcrypt password hashes, JWT bearer sessions, rate limiting, Helmet, CORS policy, validation, authorization, ownership checks, and protected admin overview endpoint.
- SQLite local-development database schema for users, subscriptions, usage, conversations, conversation jurisdiction, messages, legal documents/chunks, uploads, and payments.
- Server-enforced lifetime allowance of exactly five successful prompts. Failed AI processing does not consume a prompt; the sixth prompt returns HTTP 402 unless an active subscription record exists.
- Agent orchestration stages for query understanding, domain classification, source retrieval, citation verification/status, and grounded response synthesis. The UI only presents high-level activity, never hidden reasoning.
- Citation-aware lexical starter retriever with metadata. It does not fabricate citations and returns an explicit no-indexed-source response if nothing reliable is found.
- A deliberately limited, official Constitution starter seed (Preamble and Article 21) pointing to the Legislative Department. This is not a claim of full Indian-law coverage.
- A 36-jurisdiction state/UT coverage registry plus official-source catalogues for central legislation, schemes, case law, and legal aid. These catalogues are intentionally kept distinct from indexed material so they cannot be misrepresented as complete legal coverage.
- Upload validation for PDF, DOCX and TXT, maximum size restriction, with truthful status: TXT is stored as ready; PDF/DOCX analysis waits for an extraction adapter rather than faking analysis.
- Payment abstraction endpoints that remain unavailable until a server-verified Razorpay/Stripe checkout and webhook implementation is configured. No payment success is simulated.

## Architecture

`client/` is Vite + React + TypeScript. `server/` is Express + TypeScript and uses SQLite locally via `better-sqlite3`. The source layer is intentionally separated from the agent layer:

`request → auth/entitlement → query understanding → legal retrieval → citation verification → grounded provider adapter → response + disclaimer`

Retrieved text is explicitly treated as untrusted quoted material in the model instruction. It cannot override system rules. The SQLite retrieval adapter is suitable for a local starter; replace it behind `server/src/retrieval/` with pgvector, Qdrant, or Pinecone in production. The AI adapter currently supports OpenAI when configured and intentionally returns a setup response for unimplemented providers instead of pretending it answered.

## Setup

Node.js 20+ is required. This repository's current execution environment did not include Node, so install it locally/CI before running these commands.

```bash
cp .env.example .env
npm install
npm run db:migrate
npm run db:seed
npm run dev
```

Open `http://localhost:5173`; the API runs at `http://localhost:4000`.

For the lightweight local preview at `client/preview.html`, start the
model-backed intake service in a second terminal:

```bash
cd Support-Bot
PYTHONPATH=. .venv/bin/python scripts/legal_api.py --port 8000
```

The preview sends a question to this local bridge only when the user selects
**Analyse**. The bridge uses the configured Gemini model for a useful research
intake, but deliberately prohibits uncited statute, case, deadline, forum, or
outcome claims. It should be paired with the audited legal corpus for
source-grounded legal conclusions.

## Commands

```bash
npm run dev
npm run build
npm run test
npm run lint
npm run db:migrate
npm run db:seed
npm run ingest:constitution
npm run ingest:acts
npm run ingest:judgments
npm run ingest:documents
```

The non-Constitution ingestion commands intentionally do not download/scrape legal data automatically. Configure authorised official source connectors and structured legal parsers first. New ingest pipelines must preserve act/article/section/subsection/clause/proviso/version/effective-date/repeal metadata before chunks are stored.

## Required configuration

See `.env.example`. At a minimum set a strong `JWT_SECRET`. To enable response synthesis set `AI_PROVIDER=openai`, `OPENAI_API_KEY`, and `OPENAI_MODEL`. Keep all secrets server-side. `DATABASE_URL` defaults to the local SQLite file. Razorpay variables are placeholders for a future verified server-side payment integration; card data must never pass through this app.

## Legal and product limitations

NyayaSetu provides legal information and source-grounded research, not legal advice, representation, or an advocate-client relationship. Laws vary by facts, date, jurisdiction and state. For deadlines, arrest/detention, threats, domestic violence, or other high-risk matters, users should consult a qualified advocate or relevant authority promptly.

Only the small declared starter Constitution seed is indexed by default. Case-law search, full statutory coverage, current-law update detection, embeddings/vector search, OCR/PDF-DOCX extraction, virus scanning, password reset email delivery, and live payment checkout require additional configured services and authorised datasets. The UI and APIs do not claim those functions are available before they are configured.

The legal source registry is at `Support-Bot/knowledge/legal/coverage_manifest.json`. It catalogues the official discovery sources for state/UT law, government schemes, Supreme Court/other court material, and legal aid; it deliberately does not represent every changing statute, notification, scheme, or judgment as already available to the model.
