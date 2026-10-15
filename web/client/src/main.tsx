import { FormEvent, KeyboardEvent, useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import "./style.css";

type Citation = { id: string; title: string; provision: string | null; url: string; excerpt: string; verified: boolean; status: string };
type Message = { role: "user" | "assistant"; content: string; citations?: Citation[] };
type Conversation = { id: string; title: string; updated_at: string; jurisdiction?: string };
type User = { id: string; name: string; email: string };

const DISCLAIMER = "General legal information only — not legal advice or representation. Laws and procedures can depend on facts, date, state, and jurisdiction.";
const EXAMPLES = ["My landlord will not return my security deposit.", "My employer has not paid my salary for two months.", "I bought a defective product and the seller refuses a refund."];
const JURISDICTIONS = ["India", "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal", "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu", "Delhi", "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry"];
function inferJurisdiction(message: string, selected: string) {
  const normalized = message.toLowerCase();
  return JURISDICTIONS.find((place) => place !== "India" && normalized.includes(place.toLowerCase())) || selected;
}

async function api(path: string, options: RequestInit = {}, token = "") {
  const response = await fetch(path, { ...options, headers: { "Content-Type": "application/json", ...(token ? { Authorization: `Bearer ${token}` } : {}), ...(options.headers || {}) } });
  const body = await response.json().catch(() => ({}));
  if (!response.ok) throw Object.assign(new Error(body.message || body.error || "Request failed"), { code: body.error });
  return body;
}

function App() {
  const [token, setToken] = useState(() => localStorage.getItem("nyaya-token") || "");
  const [user, setUser] = useState<User | null>(null);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [conversationId, setConversationId] = useState<string | undefined>();
  const [jurisdiction, setJurisdiction] = useState(() => localStorage.getItem("nyaya-jurisdiction") || "India");
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [working, setWorking] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const [authMode, setAuthMode] = useState<"login" | "register">("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [error, setError] = useState("");

  const initials = useMemo(() => (user?.name || "I").split(" ").map((part) => part[0]).join("").slice(0, 2).toUpperCase(), [user]);
  const refreshConversations = async () => {
    const items = await api("/api/conversations", {}, token) as Conversation[];
    setConversations(items);
    return items;
  };

  const openConversation = async (id: string) => {
    try {
      const item = await api(`/api/conversations/${id}`, {}, token);
      setConversationId(item.id);
      setJurisdiction(item.jurisdiction || "India");
      localStorage.setItem("nyaya-jurisdiction", item.jurisdiction || "India");
      setMessages(item.messages.map((message: { role: "user" | "assistant"; content: string; citations: Citation[] }) => ({ role: message.role, content: message.content, citations: message.citations })));
      localStorage.setItem("nyaya-active-conversation", id);
      setMenuOpen(false);
    } catch (cause: any) { setError(cause.message); }
  };

  useEffect(() => {
    if (!token) return;
    Promise.all([api("/api/auth/me", {}, token), refreshConversations()]).then(async ([profile, items]) => {
      setUser(profile);
      const saved = localStorage.getItem("nyaya-active-conversation");
      if (saved && items.some((item) => item.id === saved)) await openConversation(saved);
      else if (items[0]) await openConversation(items[0].id);
    }).catch(() => { localStorage.removeItem("nyaya-token"); setToken(""); });
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [token]);

  async function authenticate(event: FormEvent) {
    event.preventDefault(); setError("");
    try {
      const payload = authMode === "login" ? { email, password } : { name, email, password };
      const result = await api(`/api/auth/${authMode}`, { method: "POST", body: JSON.stringify(payload) });
      localStorage.setItem("nyaya-token", result.token); setToken(result.token);
    } catch (cause: any) { setError(cause.message); }
  }

  async function send() {
    const text = input.trim(); if (!text || working) return;
    setInput(""); setError(""); setMessages((current) => [...current, { role: "user", content: text }]); setWorking(true);
    try {
      const result = await api("/api/chat", { method: "POST", body: JSON.stringify({ message: text, conversationId, jurisdiction: inferJurisdiction(text, jurisdiction) }) }, token);
      setConversationId(result.conversationId); localStorage.setItem("nyaya-active-conversation", result.conversationId);
      setMessages((current) => [...current, { role: "assistant", content: result.answer, citations: result.citations }]);
      await refreshConversations();
    } catch (cause: any) { setMessages((current) => [...current, { role: "assistant", content: `I could not complete this request: ${cause.message}` }]); }
    finally { setWorking(false); }
  }

  function onComposerKeyDown(event: KeyboardEvent<HTMLTextAreaElement>) {
    if (event.key === "Enter" && !event.shiftKey) { event.preventDefault(); send(); }
  }

  if (!token) return <main className="min-h-screen bg-[radial-gradient(circle_at_top_left,_#e7f0e7,_#f6f7f4_45%)] px-6 py-10 text-ink lg:grid lg:place-items-center"><div className="mx-auto grid max-w-5xl items-center gap-12 lg:grid-cols-[1fr_420px]"><section><div className="mb-6 grid h-12 w-12 place-items-center rounded-2xl bg-ink text-xl text-gold">⚖</div><p className="text-xs font-bold tracking-[.2em] text-emerald-800">INDIAN LEGAL INFORMATION</p><h1 className="mt-3 text-5xl leading-tight">Clarity for the questions that matter.</h1><p className="mt-5 max-w-lg text-lg leading-8 text-slate-600">Research Indian legal sources in plain language, with uncertainty and sources made visible.</p><div className="mt-8 flex gap-5 text-sm text-slate-500"><span>✓ Source-grounded</span><span>✓ Privacy-aware</span></div></section><form onSubmit={authenticate} className="rounded-3xl border border-white bg-white p-8 shadow-soft"><p className="text-xs font-bold tracking-[.16em] text-emerald-800">{authMode === "login" ? "WELCOME BACK" : "CREATE ACCOUNT"}</p><h2 className="mt-2 text-3xl">{authMode === "login" ? "Continue your research" : "Start your legal research"}</h2>{authMode === "register" && <input className="field" placeholder="Full name" value={name} onChange={(event) => setName(event.target.value)} required />}{error && <p className="mt-4 rounded-xl bg-rose-50 p-3 text-sm text-rose-700">{error}</p>}<input className="field" type="email" placeholder="Email address" value={email} onChange={(event) => setEmail(event.target.value)} required /><input className="field" type="password" minLength={10} placeholder="Password (10+ characters)" value={password} onChange={(event) => setPassword(event.target.value)} required /><button className="primary mt-5 w-full">{authMode === "login" ? "Sign in" : "Create account"}</button><button className="mt-5 w-full text-sm font-semibold text-emerald-800" type="button" onClick={() => { setAuthMode(authMode === "login" ? "register" : "login"); setError(""); }}>{authMode === "login" ? "New here? Create an account" : "Already have an account? Sign in"}</button></form></div></main>;

  return <div className="min-h-screen bg-paper text-ink"><header className="sticky top-0 z-20 flex items-center justify-between border-b border-emerald-950/10 bg-paper/90 px-5 py-4 backdrop-blur lg:hidden"><div className="flex items-center gap-3"><div className="grid h-9 w-9 place-items-center rounded-xl bg-ink text-gold">⚖</div><b>Indian Legal Assistant</b></div><button className="rounded-lg border border-emerald-900/15 px-3 py-2" onClick={() => setMenuOpen(!menuOpen)}>History</button></header><div className="mx-auto flex max-w-[1600px]"><aside className={`${menuOpen ? "fixed inset-x-0 top-[65px] z-30 block h-[calc(100vh-65px)]" : "hidden"} w-full shrink-0 border-r border-emerald-950/10 bg-white p-5 lg:sticky lg:top-0 lg:block lg:h-screen lg:w-[300px]`}><div className="mb-7 hidden items-center gap-3 lg:flex"><div className="grid h-10 w-10 place-items-center rounded-xl bg-ink text-gold">⚖</div><div><b className="block">Indian Legal Assistant</b><span className="text-xs text-slate-500">Legal information & research</span></div></div><button className="primary w-full" onClick={() => { setConversationId(undefined); setMessages([]); localStorage.removeItem("nyaya-active-conversation"); setMenuOpen(false); }}>＋ New conversation</button><div className="mt-7"><div className="mb-3 flex items-center justify-between"><span className="text-xs font-bold tracking-[.14em] text-slate-500">RECENT RESEARCH</span><span className="rounded-full bg-sage px-2 py-0.5 text-xs">{conversations.length}</span></div><div className="space-y-1">{conversations.length === 0 && <p className="px-3 py-4 text-sm text-slate-500">Your saved conversations will appear here.</p>}{conversations.map((conversation) => <button key={conversation.id} className={`w-full rounded-xl px-3 py-3 text-left text-sm transition ${conversation.id === conversationId ? "bg-emerald-950 text-white shadow" : "text-slate-600 hover:bg-sage"}`} onClick={() => openConversation(conversation.id)}><span className="block truncate font-medium">{conversation.title}</span><span className={`mt-1 block text-xs ${conversation.id === conversationId ? "text-emerald-100" : "text-slate-400"}`}>{new Date(conversation.updated_at).toLocaleDateString()}</span></button>)}</div></div><div className="mt-auto border-t border-emerald-950/10 pt-5 lg:absolute lg:bottom-5 lg:left-5 lg:right-5"><div className="flex items-center gap-3"><div className="grid h-9 w-9 place-items-center rounded-full bg-gold text-sm font-bold">{initials}</div><div className="min-w-0"><b className="block truncate text-sm">{user?.name}</b><span className="block truncate text-xs text-slate-500">{user?.email}</span></div></div><button className="mt-4 text-sm font-semibold text-emerald-800" onClick={() => { localStorage.removeItem("nyaya-token"); localStorage.removeItem("nyaya-active-conversation"); setToken(""); }}>Sign out</button></div></aside><main className="flex min-h-screen min-w-0 flex-1 flex-col"><section className="mx-auto w-full max-w-4xl px-5 pb-4 pt-10 lg:px-12 lg:pt-14"><div className="flex flex-wrap items-start justify-between gap-5"><div><p className="text-xs font-bold tracking-[.18em] text-emerald-800">SOURCE-FIRST LEGAL RESEARCH</p><h1 className="mt-2 text-4xl">How can I help today?</h1><p className="mt-2 text-slate-600">Describe what happened in your own words.</p></div><div className="rounded-full border border-emerald-700/15 bg-white px-3 py-2 text-xs font-semibold text-emerald-800">● Verified-source workflow</div></div><div className="mt-7 rounded-2xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm leading-6 text-amber-950"><b>Important:</b> {DISCLAIMER}</div></section><section className="mx-auto flex w-full max-w-4xl flex-1 flex-col px-5 pb-40 lg:px-12">{messages.length === 0 ? <div className="my-auto py-12"><div className="max-w-2xl"><span className="inline-flex rounded-full bg-sage px-3 py-1 text-xs font-bold tracking-wide text-emerald-800">START WITH YOUR SITUATION</span><h2 className="mt-4 text-3xl">You don’t need to know the law to begin.</h2><p className="mt-3 text-lg leading-8 text-slate-600">Tell us what happened. We’ll identify legal areas that may be relevant and show the available sources.</p></div><div className="mt-8 grid gap-3 md:grid-cols-3">{EXAMPLES.map((example) => <button key={example} className="rounded-2xl border border-emerald-950/10 bg-white p-4 text-left text-sm leading-6 shadow-sm transition hover:-translate-y-0.5 hover:border-gold hover:shadow" onClick={() => setInput(example)}>{example}<span className="mt-3 block text-xs font-bold text-emerald-800">Use this example →</span></button>)}</div></div> : <div className="space-y-7 py-5">{messages.map((message, index) => <article key={`${message.role}-${index}`} className={`flex gap-4 ${message.role === "user" ? "justify-end" : "justify-start"}`}><div className={`${message.role === "user" ? "order-2 bg-ink text-white" : "bg-gold text-ink"} grid h-9 w-9 shrink-0 place-items-center rounded-full text-xs font-bold`}>{message.role === "user" ? initials : "⚖"}</div><div className={`${message.role === "user" ? "order-1 bg-ink text-white" : "border border-emerald-950/10 bg-white"} max-w-[82%] rounded-2xl px-5 py-4 text-[15px] leading-7 shadow-sm whitespace-pre-wrap`}>{message.content}{message.citations?.length ? <div className="mt-4 border-t border-emerald-950/10 pt-3"><p className="text-xs font-bold tracking-wider text-emerald-800">SOURCES</p>{message.citations.map((citation) => <a key={citation.id} href={citation.url} className="mt-2 block text-sm font-semibold text-emerald-800 underline" target="_blank" rel="noreferrer">{citation.verified ? "✓" : "!"} {citation.title}{citation.provision ? ` — ${citation.provision}` : ""}</a>)}</div> : null}</div></article>)}{working && <article className="flex gap-4"><div className="grid h-9 w-9 place-items-center rounded-full bg-gold">⚖</div><div className="rounded-2xl border border-emerald-950/10 bg-white px-5 py-4 shadow-sm"><p className="font-medium">Researching available legal sources…</p><p className="mt-1 text-sm text-slate-500">Understanding your situation · checking citations · preparing a cautious response</p></div></article>}</div>}</section><footer className="fixed bottom-0 left-0 right-0 z-10 border-t border-emerald-950/10 bg-paper/95 px-5 py-4 backdrop-blur lg:left-[300px]"><div className="mx-auto max-w-4xl"><div className="flex items-end gap-3 rounded-2xl border border-emerald-950/15 bg-white p-2 shadow-soft"><textarea className="min-h-[56px] flex-1 resize-none border-0 bg-transparent px-3 py-2 outline-none" value={input} onChange={(event) => setInput(event.target.value)} onKeyDown={onComposerKeyDown} placeholder="Describe your situation or ask about a legal source…" /><button className="primary h-11 shrink-0" disabled={working || !input.trim()} onClick={send}>Send <span aria-hidden>↑</span></button></div>{error && <p className="mt-2 text-sm text-rose-700">{error}</p>}<p className="mt-2 text-center text-xs text-slate-500">{DISCLAIMER}</p></div></footer></main></div></div>;
}

createRoot(document.getElementById("root")!).render(<App />);
