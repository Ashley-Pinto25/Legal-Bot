import crypto from "node:crypto";
export const id = () => crypto.randomUUID();
export const now = () => new Date().toISOString();
