/** A transparent registry of official discovery sources; it is not an ingestion claim. */
export const JURISDICTIONS = [
  "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal", "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu", "Delhi", "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry",
] as const;

export type Jurisdiction = typeof JURISDICTIONS[number];
export const isJurisdiction = (value: unknown): value is Jurisdiction => typeof value === "string" && (JURISDICTIONS as readonly string[]).includes(value);

export const OFFICIAL_SOURCE_CATALOG = [
  { id: "india-code", name: "India Code", coverage: "Central Acts, rules and official legislative records", url: "https://indiacode.gov.in/", kind: "legislation", status: "official" },
  { id: "e-gazette", name: "e-Gazette of India", coverage: "Central Gazette notifications and amendments", url: "https://egazette.nic.in/", kind: "legislation", status: "official" },
  { id: "state-gazettes", name: "State and UT Gazette / legislation portals", coverage: "Jurisdiction-specific Acts, rules, notifications and local instruments", url: "https://www.india.gov.in/", kind: "state-law", status: "connector-required" },
  { id: "myscheme", name: "myScheme", coverage: "Government scheme discovery and eligibility information", url: "https://www.myscheme.gov.in/", kind: "schemes", status: "official-catalogue" },
  { id: "supreme-court", name: "Supreme Court of India", coverage: "Judgments, orders, case status and services", url: "https://www.sci.gov.in/", kind: "case-law", status: "official" },
  { id: "ecourts", name: "eCourts Services", coverage: "High Court and District Court case information", url: "https://ecourts.gov.in/", kind: "case-law", status: "official-catalogue" },
  { id: "scr", name: "Supreme Court Reports", coverage: "Reported Supreme Court decisions", url: "https://scr.sci.gov.in/scrsearch/", kind: "case-law", status: "official" },
  { id: "nalsa", name: "National Legal Services Authority", coverage: "Legal-aid services and State/District Legal Services Authorities", url: "https://nalsa.gov.in/", kind: "legal-aid", status: "official" },
] as const;

export function coverageSnapshot() {
  return { scopeNote: "The registry lists official discovery sources. It does not mean every law, scheme, or judgment is already indexed. Search results may only cite audited, indexed material.", jurisdictions: JURISDICTIONS.map((name) => ({ name, indexed: false, ingestionStatus: "official connector required" })), sources: OFFICIAL_SOURCE_CATALOG };
}
