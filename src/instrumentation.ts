/** Runs once per server start. On serverless hosts (empty disk) it prepares the database before the first request. */
export async function register(): Promise<void> {
  if (process.env.NEXT_RUNTIME !== "nodejs" || process.env.NEXT_PHASE === "phase-production-build") return;
  const { env } = await import("./server/env");
  if (!env.autoBootstrap) return;
  const { migrate } = await import("./server/db");
  const { syncFileCases } = await import("./server/content");
  const { ensureAdmin } = await import("./server/auth");
  await migrate();
  await syncFileCases();
  await ensureAdmin();
}
