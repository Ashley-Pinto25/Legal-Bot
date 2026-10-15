import Database from "better-sqlite3";
import { mkdirSync } from "node:fs";
import { dirname, resolve } from "node:path";
const file = process.env.DATABASE_URL?.replace(/^file:/, "") || "./data/nyayaai.db";
mkdirSync(dirname(resolve(file)), { recursive: true });
export const db = new Database(file);
db.pragma("foreign_keys = ON");
