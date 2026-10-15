import "../database/migrate.js";
const target=process.argv[2]||"all";
if(target==="constitution"||target==="all") await import("./seed.js");
if(target!=="constitution"&&target!=="all") console.log(`${target} ingestion is intentionally not automatic: configure an authorised official source connector before importing data.`);
