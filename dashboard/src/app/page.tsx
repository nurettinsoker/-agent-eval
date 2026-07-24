import Link from "next/link";

export default function HomePage() {
  return (
    <div className="min-h-screen bg-white dark:bg-gray-950">
      {/* Nav */}
      <nav className="border-b border-gray-200 dark:border-gray-800">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 items-center justify-between">
            <div className="flex items-center space-x-2">
              <svg className="h-8 w-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
              <span className="text-xl font-bold text-gray-900 dark:text-white">Agent Eval</span>
            </div>
            <div className="flex items-center space-x-4">
              <Link href="https://github.com/nurettinsoker/-agent-eval" target="_blank" className="text-sm text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white">
                GitHub
              </Link>
              <Link href="/auth/signin" className="text-sm text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white">
                Sign In
              </Link>
              <Link href="/auth/signup" className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700">
                Get Started Free
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 pt-20 pb-16 text-center">
        <div className="inline-flex items-center px-3 py-1 rounded-full bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-400 text-sm font-medium mb-6">
          Open Source + Free CLI
        </div>
        <h1 className="text-5xl sm:text-6xl font-bold text-gray-900 dark:text-white tracking-tight">
          Evaluate Your AI Agents<br />
          <span className="text-blue-600">Before They Ship</span>
        </h1>
        <p className="mt-6 text-xl text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
          Test LLM agents across multiple cases with 5 grader types.
          Catch regressions, measure quality, ship with confidence.
        </p>
        <div className="mt-10 flex items-center justify-center gap-4">
          <Link href="/auth/signup" className="px-6 py-3 text-base font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 shadow-lg shadow-blue-600/25">
            Start Free Trial
          </Link>
          <Link href="https://github.com/nurettinsoker/-agent-eval" target="_blank" className="px-6 py-3 text-base font-medium text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-800 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700">
            View on GitHub
          </Link>
        </div>

        {/* Terminal Preview */}
        <div className="mt-16 mx-auto max-w-3xl">
          <div className="bg-gray-900 dark:bg-gray-950 rounded-xl border border-gray-700 shadow-2xl overflow-hidden">
            <div className="flex items-center px-4 py-3 border-b border-gray-700">
              <div className="flex space-x-2">
                <div className="w-3 h-3 rounded-full bg-red-500"></div>
                <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
                <div className="w-3 h-3 rounded-full bg-green-500"></div>
              </div>
              <span className="ml-3 text-sm text-gray-400 font-mono">terminal</span>
            </div>
            <pre className="p-6 text-sm text-green-400 font-mono overflow-x-auto text-left">
{`$ agent-eval run suite.yaml --agent agent.yaml --push

Running eval: my-agent on 3 test cases

  Test Case        | Status | Score | Latency
  -----------------+--------+-------+--------
  basic_math       |  PASS  | 100%  |   45ms
  capital_france   |  PASS  | 100%  |   38ms
  code_fibonacci   |  PASS  |  95%  |  120ms
  SUMMARY          | 100%   |  98%  |  203ms

Results pushed to dashboard`}
            </pre>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-20 bg-gray-50 dark:bg-gray-900">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center text-gray-900 dark:text-white mb-12">
            Everything You Need to Evaluate Agents
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            <FeatureCard
              title="5 Grader Types"
              description="Exact match, semantic similarity, LLM judge, regex, and code execution graders out of the box."
              icon="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
            />
            <FeatureCard
              title="Multi-Agent Support"
              description="Test OpenAI, Anthropic, custom HTTP endpoints, or mock agents. Same interface for all."
              icon="M13 10V3L4 14h7v7l9-11h-7z"
            />
            <FeatureCard
              title="Async & Parallel"
              description="Run hundreds of test cases concurrently. Results in seconds, not hours."
              icon="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
            />
            <FeatureCard
              title="Visual Dashboard"
              description="Track runs, compare versions, spot regressions. Beautiful UI with dark mode."
              icon="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
            />
            <FeatureCard
              title="Push to Dashboard"
              description="CLI results sync to your team dashboard with one flag. No manual uploads."
              icon="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"
            />
            <FeatureCard
              title="Open Source"
              description="CLI is fully open source. Host it yourself or use our managed dashboard."
              icon="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"
            />
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section id="pricing" className="py-20">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center text-gray-900 dark:text-white mb-4">
            Simple, Transparent Pricing
          </h2>
          <p className="text-center text-gray-600 dark:text-gray-400 mb-12">
            Start free. Upgrade when you need more.
          </p>
          <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            {/* Free */}
            <div className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-8">
              <h3 className="text-xl font-bold text-gray-900 dark:text-white">Free</h3>
              <p className="mt-2 text-gray-500 dark:text-gray-400">For individual developers</p>
              <div className="mt-6">
                <span className="text-4xl font-bold text-gray-900 dark:text-white">$0</span>
                <span className="text-gray-500 dark:text-gray-400">/month</span>
              </div>
              <ul className="mt-8 space-y-4">
                <PricingFeature>Unlimited CLI evals</PricingFeature>
                <PricingFeature>50 dashboard runs/month</PricingFeature>
                <PricingFeature>3 projects</PricingFeature>
                <PricingFeature>All 5 grader types</PricingFeature>
                <PricingFeature>Community support</PricingFeature>
              </ul>
              <Link href="/auth/signup" className="mt-8 block w-full py-3 text-center text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors">
                Get Started
              </Link>
            </div>

            {/* Pro */}
            <div className="bg-white dark:bg-gray-800 rounded-2xl border-2 border-blue-600 p-8 relative">
              <div className="absolute -top-3 left-1/2 -translate-x-1/2 px-3 py-1 bg-blue-600 text-white text-xs font-bold rounded-full">
                POPULAR
              </div>
              <h3 className="text-xl font-bold text-gray-900 dark:text-white">Pro</h3>
              <p className="mt-2 text-gray-500 dark:text-gray-400">For teams shipping AI products</p>
              <div className="mt-6">
                <span className="text-4xl font-bold text-gray-900 dark:text-white">$29</span>
                <span className="text-gray-500 dark:text-gray-400">/month</span>
              </div>
              <ul className="mt-8 space-y-4">
                <PricingFeature>Unlimited CLI evals</PricingFeature>
                <PricingFeature>Unlimited dashboard runs</PricingFeature>
                <PricingFeature>Unlimited projects</PricingFeature>
                <PricingFeature>All 5 grader types</PricingFeature>
                <PricingFeature>Team collaboration (up to 5)</PricingFeature>
                <PricingFeature>API access</PricingFeature>
                <PricingFeature>Priority support</PricingFeature>
              </ul>
              <Link href="/auth/signup?plan=pro" className="mt-8 block w-full py-3 text-center text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors">
                Start 14-Day Free Trial
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 bg-gray-50 dark:bg-gray-900">
        <div className="mx-auto max-w-3xl px-4 text-center">
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white">
            Ready to Ship Better AI?
          </h2>
          <p className="mt-4 text-lg text-gray-600 dark:text-gray-400">
            Start evaluating your agents in 5 minutes. No credit card required.
          </p>
          <div className="mt-8 flex items-center justify-center gap-4">
            <Link href="/auth/signup" className="px-6 py-3 text-base font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700">
              Start Free
            </Link>
            <span className="text-gray-400">or</span>
            <code className="px-4 py-2 text-sm bg-gray-900 dark:bg-gray-800 text-green-400 rounded-lg font-mono">
              pip install agent-eval
            </code>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 border-t border-gray-200 dark:border-gray-800">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 flex items-center justify-between text-sm text-gray-500 dark:text-gray-400">
          <span>2025 Agent Eval. Open source under MIT.</span>
          <div className="flex space-x-6">
            <a href="https://github.com/nurettinsoker/-agent-eval" target="_blank" className="hover:text-gray-900 dark:hover:text-white">GitHub</a>
            <a href="#pricing" className="hover:text-gray-900 dark:hover:text-white">Pricing</a>
            <a href="https://github.com/nurettinsoker/-agent-eval/issues" target="_blank" className="hover:text-gray-900 dark:hover:text-white">Support</a>
          </div>
        </div>
      </footer>
    </div>
  );
}

function FeatureCard({ title, description, icon }: { title: string; description: string; icon: string }) {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-6">
      <div className="w-10 h-10 rounded-lg bg-blue-50 dark:bg-blue-900/20 flex items-center justify-center mb-4">
        <svg className="h-5 w-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={icon} />
        </svg>
      </div>
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white">{title}</h3>
      <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">{description}</p>
    </div>
  );
}

function PricingFeature({ children }: { children: React.ReactNode }) {
  return (
    <li className="flex items-start">
      <svg className="h-5 w-5 text-green-500 mt-0.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
      </svg>
      <span className="ml-3 text-sm text-gray-700 dark:text-gray-300">{children}</span>
    </li>
  );
}
