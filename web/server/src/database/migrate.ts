import { db } from "./db.js";
db.exec(`
CREATE TABLE IF NOT EXISTS users (id TEXT PRIMARY KEY, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL, role TEXT NOT NULL DEFAULT 'user', created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS subscriptions (id TEXT PRIMARY KEY, user_id TEXT NOT NULL REFERENCES users(id), plan TEXT NOT NULL, status TEXT NOT NULL, start_date TEXT, expiry_date TEXT, provider TEXT, provider_subscription_id TEXT);
CREATE TABLE IF NOT EXISTS usage (user_id TEXT PRIMARY KEY REFERENCES users(id), prompts_used INTEGER NOT NULL DEFAULT 0, free_prompts_used INTEGER NOT NULL DEFAULT 0, paid_prompts_used INTEGER NOT NULL DEFAULT 0, period TEXT);
CREATE TABLE IF NOT EXISTS conversations (id TEXT PRIMARY KEY, user_id TEXT NOT NULL REFERENCES users(id), title TEXT NOT NULL, created_at TEXT NOT NULL, updated_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS conversation_context (conversation_id TEXT PRIMARY KEY REFERENCES conversations(id) ON DELETE CASCADE, jurisdiction TEXT NOT NULL DEFAULT 'India', updated_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS messages (id TEXT PRIMARY KEY, conversation_id TEXT NOT NULL REFERENCES conversations(id) ON DELETE CASCADE, role TEXT NOT NULL, content TEXT NOT NULL, citations TEXT NOT NULL DEFAULT '[]', created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS legal_documents (id TEXT PRIMARY KEY, title TEXT NOT NULL, source_name TEXT NOT NULL, source_url TEXT NOT NULL, act_name TEXT, jurisdiction TEXT NOT NULL DEFAULT 'India', source_type TEXT NOT NULL, version TEXT, effective_date TEXT, repeal_status TEXT NOT NULL DEFAULT 'unknown', metadata TEXT NOT NULL DEFAULT '{}');
CREATE TABLE IF NOT EXISTS legal_chunks (id TEXT PRIMARY KEY, document_id TEXT NOT NULL REFERENCES legal_documents(id) ON DELETE CASCADE, content TEXT NOT NULL, article TEXT, section TEXT, chapter TEXT, keywords TEXT NOT NULL DEFAULT '', metadata TEXT NOT NULL DEFAULT '{}');
CREATE TABLE IF NOT EXISTS legal_uploads (id TEXT PRIMARY KEY, user_id TEXT NOT NULL REFERENCES users(id), filename TEXT NOT NULL, mimetype TEXT NOT NULL, extracted_text TEXT, status TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS payments (id TEXT PRIMARY KEY, user_id TEXT NOT NULL REFERENCES users(id), provider TEXT NOT NULL, transaction_id TEXT, amount INTEGER, currency TEXT, status TEXT NOT NULL, timestamp TEXT NOT NULL);
CREATE INDEX IF NOT EXISTS idx_chunks_document ON legal_chunks(document_id);
CREATE INDEX IF NOT EXISTS idx_conversations_user ON conversations(user_id);
`);
console.log("NyayaSetu database migration complete.");
