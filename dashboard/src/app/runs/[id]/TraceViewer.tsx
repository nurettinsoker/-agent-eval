"use client";

import { cn } from "@/lib/utils";
import { Badge } from "@/components/Badge";

interface TraceViewerProps {
  results: any[];
}

export function TraceViewer({ results }: TraceViewerProps) {
  if (!results?.length) {
    return <div className="p-8 text-center text-gray-500">No trace data available</div>;
  }

  return (
    <div className="space-y-4">
      {results.map((result, index) => (
        <div key={result.id || index} className="border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden">
          <div className="bg-gray-50 dark:bg-gray-800/50 px-4 py-3 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <span className="font-mono text-sm text-gray-500">#{index + 1}</span>
              <span className="font-medium">{result.testCaseName}</span>
              <Badge variant={result.passed ? "success" : "error"}>
                {result.passed ? "PASS" : "FAIL"}
              </Badge>
              <Badge variant="info">{result.score.toFixed(2)}</Badge>
            </div>
            <div className="flex items-center gap-4 text-sm text-gray-500">
              <span>{result.latencyMs}ms</span>
              <span>${result.costUsd.toFixed(6)}</span>
              <span>{result.tokens} tokens</span>
            </div>
          </div>
          
          <div className="p-4 space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-xs font-medium text-gray-500 mb-1">Input</label>
                <pre className="bg-gray-100 dark:bg-gray-800 p-3 rounded text-sm overflow-x-auto max-h-64 whitespace-pre-wrap">
                  {result.agentOutput || "No output"}
                </pre>
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-500 mb-1">Grades</label>
                <div className="space-y-2">
                  {result.grades?.map((grade: any, i: number) => (
                    <div key={i} className="flex items-center justify-between p-2 bg-gray-50 dark:bg-gray-800 rounded">
                      <span className="text-sm">{grade.graderName}</span>
                      <div className="flex items-center gap-2">
                        <Badge variant={grade.passed ? "success" : "error"}>{(grade.score * 100).toFixed(0)}%</Badge>
                        {grade.reasoning && (
                          <span className="text-xs text-gray-500 max-w-xs truncate">{grade.reasoning}</span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-500 mb-1">Error</label>
                <pre className="bg-red-50 dark:bg-red-900/20 p-3 rounded text-sm text-red-700 dark:text-red-300">
                  {result.error || "No error"}
                </pre>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}