import { z } from "zod";
import { createTRPCRouter, publicProcedure } from "@/server/api/trpc";

export const evalRunRouter = createTRPCRouter({
  create: publicProcedure
    .input(
      z.object({
        projectId: z.string(),
        agentConfig: z.any(),
        testCases: z.array(z.any()).optional(),
        results: z.array(z.any()),
      })
    )
    .mutation(async ({ ctx, input }) => {
      const run = await ctx.db.evalRun.create({
        data: {
          projectId: input.projectId,
          agentConfig: JSON.stringify(input.agentConfig),
          status: "COMPLETED",
          totalTests: input.results.length,
          passedTests: input.results.filter((r: any) => r.passed).length,
          totalCost: input.results.reduce((sum: number, r: any) => sum + (r.costUsd || 0), 0),
          totalTokens: input.results.reduce((sum: number, r: any) => sum + (r.tokens || 0), 0),
          startedAt: new Date(),
          completedAt: new Date(),
          results: {
            create: input.results.map((result: any) => ({
              testCaseId: result.testCaseId || "",
              testCaseName: result.testCaseName || "",
              agentOutput: result.agentOutput || "",
              passed: result.passed || false,
              score: result.score || 0,
              latencyMs: result.latencyMs || 0,
              costUsd: result.costUsd || 0,
              tokens: result.tokens || 0,
              error: result.error || null,
              grades: {
                create: (result.grades || []).map((grade: any) => ({
                  graderName: grade.graderName || "",
                  graderType: grade.graderType || "",
                  score: grade.score || 0,
                  passed: grade.passed || false,
                  reasoning: grade.reasoning || null,
                  metadata: grade.metadata ? JSON.stringify(grade.metadata) : null,
                })),
              },
            })),
          },
        },
        include: { results: { include: { grades: true } } },
      });
      return run;
    }),

  get: publicProcedure
    .input(z.object({ id: z.string() }))
    .query(async ({ ctx, input }) => {
      return ctx.db.evalRun.findUnique({
        where: { id: input.id },
        include: {
          results: { include: { grades: true }, orderBy: { createdAt: "asc" } },
        },
      });
    }),

  list: publicProcedure
    .input(
      z.object({
        projectId: z.string().optional(),
        limit: z.number().min(1).max(100).default(20),
        cursor: z.string().optional(),
        status: z.string().optional(),
      })
    )
    .query(async ({ ctx, input }) => {
      const where: any = {};
      if (input.projectId) where.projectId = input.projectId;
      if (input.status) where.status = input.status;

      const items = await ctx.db.evalRun.findMany({
        where,
        take: input.limit + 1,
        cursor: input.cursor ? { id: input.cursor } : undefined,
        orderBy: { createdAt: "desc" },
        include: { results: true },
      });

      let nextCursor: typeof input.cursor = undefined;
      if (items.length > input.limit) {
        const nextItem = items.pop();
        nextCursor = nextItem!.id;
      }

      return { items, nextCursor };
    }),

  delete: publicProcedure
    .input(z.object({ id: z.string() }))
    .mutation(async ({ ctx, input }) => {
      return ctx.db.evalRun.delete({ where: { id: input.id } });
    }),
});
