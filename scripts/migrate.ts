import { migrate } from "../src/server/db";
const done = await migrate();
console.log(done.length ? `applied: ${done.join(", ")}` : "database up to date");
