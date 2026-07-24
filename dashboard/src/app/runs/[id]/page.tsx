"use client";

import { useParams } from "next/navigation";
import { trpc } from "@/utils/trpc";
import { Tabs, TabList, Tab, TabPanels, TabPanel } from "@/components/Tabs";
import { TraceViewer } from "./TraceViewer";
import { formatDistanceToNow } from "date-fns";

export default function RunDetailPage() {
  const params = useParams();
  const id = params.id as string;

  const { data: run, isLoading, error } = trpc.evalRun.get.useQuery(
    { id },
    { enabled: !!id }
  );

  if (isLoading) return <div className="p-8 text-center">Loading run details...</div>;
  if (error || !run) return <div className="p-8 text-center text-red-600">Run not found</div>;

  const passRate = run.totalTests > 0 ? (run.passedTests / run.totalTests) * 100 : 0;

  return (
    <div className="p-6">
      <div className="mb-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Run {run.id.slice(0, 8)}
          </h1>
          <p className="text-gray-500 dark:text-gray-400 mt-1">
            {formatDistanceToNow(new Date(run.createdAt), { addSuffix: true })}
          </p>
        </div>
        <div className="flex items-center gap-4">
          <span className={`px-3 py-1 rounded-full text-sm font-medium ${
            run.status === "COMPLETED" ? "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400" :
            run.status === "RUNNING" ? "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400" :
            run.status === "FAILED" ? "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400" :
            "bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300"
          }`}>
            {run.status}
          </span>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-4 mb-6">
        <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-5">
          <p className="text-sm text-gray-500 dark:text-gray-400">Total Tests</p>
          <p className="text-3xl font-bold text-gray-900 dark:text-white">{run.totalTests}</p>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-5">
          <p className="text-sm text-gray-500 dark:text-gray-400">Passed</p>
          <p className="text-3xl font-bold text-green-600 dark:text-green-400">{run.passedTests}</p>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-5">
          <p className="text-sm text-gray-500 dark:text-gray-400">Pass Rate</p>
          <p className="text-3xl font-bold text-blue-600 dark:text-blue-400">{passRate.toFixed(1)}%</p>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-5">
          <p className="text-sm text-gray-500 dark:text-gray-400">Total Cost</p>
          <p className="text-3xl font-bold text-gray-900 dark:text-white">${run.totalCost.toFixed(4)}</p>
        </div>
      </div>

      <Tabs defaultTab="results">
        <TabList>
          <Tab tab="results">Results ({run.results?.length || 0})</Tab>
          <Tab tab="config">Agent Config</Tab>
          <Tab tab="stats">Statistics</Tab>
        </TabList>

        <TabPanels className="mt-4">
          <TabPanel tab="results">
            <TraceViewer results={run.results || []} />
          </TabPanel>

          <TabPanel tab="config">
            <div className="bg-gray-100 dark:bg-gray-800 rounded-lg p-4 overflow-x-auto">
              <pre className="text-sm font-mono">{(() => {
                try { return JSON.stringify(JSON.parse(run.agentConfig), null, 2); }
                catch { return run.agentConfig; }
              })()}</pre>
            </div>
          </TabPanel>

          <TabPanel tab="stats">
            <div className="grid gap-4 md:grid-cols-2">
              <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-5">
                <h3 className="font-medium mb-3">Timing</h3>
                <dl className="space-y-2 text-sm">
                  <div className="flex justify-between"><dt className="text-gray-500">Total Latency</dt><dd className="font-medium">{run.results?.reduce((a: number, r: any) => a + (r.latencyMs || 0), 0)}ms</dd></div>
                  <div className="flex justify-between"><dt className="text-gray-500">Avg Latency</dt><dd className="font-medium">{run.totalTests ? Math.round((run.results?.reduce((a: number, r: any) => a + (r.latencyMs || 0), 0) || 0) / run.totalTests) : 0}ms</dd></div>
                </dl>
              </div>
              <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-5">
                <h3 className="font-medium mb-3">Token Usage</h3>
                <dl className="space-y-2 text-sm">
                  <div className="flex justify-between"><dt className="text-gray-500">Total Tokens</dt><dd className="font-medium">{run.totalTokens}</dd></div>
                  <div className="flex justify-between"><dt className="text-gray-500">Total Cost</dt><dd className="font-medium">${run.totalCost.toFixed(4)}</dd></div>
                </dl>
              </div>
            </div>
          </TabPanel>
        </TabPanels>
      </Tabs>
    </div>
  );
}
