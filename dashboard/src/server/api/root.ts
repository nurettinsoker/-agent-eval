import { createTRPCRouter } from "@/server/api/trpc";
import { evalRunRouter } from "@/server/api/routers/evalRun";
import { projectRouter } from "@/server/api/routers/project";

export const appRouter = createTRPCRouter({
  evalRun: evalRunRouter,
  project: projectRouter,
});

export type AppRouter = typeof appRouter;