import "../database/migrate.js"; import { db } from "../database/db.js"; import { id } from "../utils.js";
const source="https://legislative.gov.in/constitution-of-india/";
const documentId="constitution-of-india";
db.prepare("INSERT OR IGNORE INTO legal_documents (id,title,source_name,source_url,act_name,jurisdiction,source_type,version,effective_date,repeal_status,metadata) VALUES (?,?,?,?,?,?,?,?,?,?,?)").run(documentId,"Constitution of India","Legislative Department, Ministry of Law and Justice",source,"Constitution of India","India","official","Official publication",null,"current",JSON.stringify({coverage:"Seed contains only limited verified starter provisions; ingest the official full text for broader coverage."}));
const entries=[
 ["preamble","Preamble","WE, THE PEOPLE OF INDIA, having solemnly resolved to constitute India into a SOVEREIGN SOCIALIST SECULAR DEMOCRATIC REPUBLIC and to secure to all its citizens: JUSTICE, social, economic and political; LIBERTY of thought, expression, belief, faith and worship; EQUALITY of status and of opportunity; and to promote among them all FRATERNITY assuring the dignity of the individual and the unity and integrity of the Nation; IN OUR CONSTITUENT ASSEMBLY this twenty-sixth day of November, 1949, do HEREBY ADOPT, ENACT AND GIVE TO OURSELVES THIS CONSTITUTION."],
 ["article-21","Article 21","No person shall be deprived of his life or personal liberty except according to procedure established by law."]
];
for(const [chunk,article,content] of entries) db.prepare("INSERT OR IGNORE INTO legal_chunks (id,document_id,content,article,keywords,metadata) VALUES (?,?,?,?,?,?)").run(chunk,documentId,content,article,`${article} constitution india fundamental rights life personal liberty preamble`,JSON.stringify({official:true}));
console.log("Seeded limited official Constitution starter material.");
