"use client";

import { useState } from "react";
import Link from "next/link";

export default function PricingPage() {
  const [loading, setLoading] = useState(false);

  const handleCheckout = async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/checkout", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ plan: "pro" }),
      });
      const data = await res.json();
      if (data.url) {
        window.location.href = data.url;
      }
    } catch {
      alert("Checkout failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-white dark:bg-gray-950">
      {/* Nav */}
      <nav className="border-b border-gray-200 dark:border-gray-800">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 items-center justify-between">
            <Link href="/" className="flex items-center space-x-2">
              <svg className="h-8 w-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
              <span className="text-xl font-bold text-gray-900 dark:text-white">Agent Eval</span>
            </Link>
            <div className="flex items-center space-x-4">
              <Link href="/" className="text-sm text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white">Home</Link>
              <Link href="/auth/signin" className="text-sm text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white">Sign In</Link>
              <Link href="/auth/signup" className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700">Get Started</Link>
            </div>
          </div>
        </div>
      </nav>

      <div className="py-20">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <h1 className="text-4xl font-bold text-center text-gray-900 dark:text-white mb-4">
            Simple, Transparent Pricing
          </h1>
          <p className="text-center text-lg text-gray-600 dark:text-gray-400 mb-16">
            Start free. Upgrade when your team needs more power.
          </p>

          <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            {/* Free */}
            <div className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-8">
              <h3 className="text-xl font-bold text-gray-900 dark:text-white">Free</h3>
              <p className="mt-2 text-gray-500 dark:text-gray-400">For individual developers getting started</p>
              <div className="mt-6">
                <span className="text-5xl font-bold text-gray-900 dark:text-white">$0</span>
                <span className="text-gray-500 dark:text-gray-400">/month</span>
              </div>
              <ul className="mt-8 space-y-4">
                {["Unlimited CLI evaluations", "50 dashboard runs/month", "3 projects", "All 5 grader types", "Community support"].map((f) => (
                  <li key={f} className="flex items-start">
                    <svg className="h-5 w-5 text-green-500 mt-0.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    <span className="ml-3 text-sm text-gray-700 dark:text-gray-300">{f}</span>
                  </li>
                ))}
              </ul>
              <Link href="/auth/signup" className="mt-8 block w-full py-3 text-center text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors">
                Get Started Free
              </Link>
            </div>

            {/* Pro */}
            <div className="bg-white dark:bg-gray-800 rounded-2xl border-2 border-blue-600 p-8 relative shadow-lg shadow-blue-600/10">
              <div className="absolute -top-3 left-1/2 -translate-x-1/2 px-4 py-1 bg-blue-600 text-white text-xs font-bold rounded-full tracking-wide">
                MOST POPULAR
              </div>
              <h3 className="text-xl font-bold text-gray-900 dark:text-white">Pro</h3>
              <p className="mt-2 text-gray-500 dark:text-gray-400">For teams shipping AI products</p>
              <div className="mt-6">
                <span className="text-5xl font-bold text-gray-900 dark:text-white">$29</span>
                <span className="text-gray-500 dark:text-gray-400">/month</span>
              </div>
              <ul className="mt-8 space-y-4">
                {[
                  "Unlimited CLI evaluations",
                  "Unlimited dashboard runs",
                  "Unlimited projects",
                  "All 5 grader types",
                  "Team collaboration (up to 5 seats)",
                  "API access",
                  "Priority email support",
                  "Custom grader support",
                ].map((f) => (
                  <li key={f} className="flex items-start">
                    <svg className="h-5 w-5 text-green-500 mt-0.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    <span className="ml-3 text-sm text-gray-700 dark:text-gray-300">{f}</span>
                  </li>
                ))}
              </ul>
              <button
                onClick={handleCheckout}
                disabled={loading}
                className="mt-8 block w-full py-3 text-center text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
              >
                {loading ? "Redirecting to Stripe..." : "Start 14-Day Free Trial"}
              </button>
              <p className="mt-3 text-center text-xs text-gray-500 dark:text-gray-400">
                No credit card required for trial
              </p>
            </div>
          </div>

          {/* FAQ */}
          <div className="mt-20 max-w-2xl mx-auto">
            <h2 className="text-2xl font-bold text-center text-gray-900 dark:text-white mb-8">
              Frequently Asked Questions
            </h2>
            <div className="space-y-6">
              <Faq q="Can I use the CLI for free forever?">
                Yes! The CLI is open source (MIT license) and completely free. You only pay for the hosted dashboard.
              </Faq>
              <Faq q="What happens after the 14-day trial?">
                You&apos;ll be charged $29/month. Cancel anytime from your dashboard settings.
              </Faq>
              <Faq q="Can I self-host the dashboard?">
                Yes! The dashboard is open source. You can deploy it on your own infrastructure for free.
              </Faq>
              <Faq q="Do you offer annual billing?">
                Not yet, but it&apos;s coming soon with a 20% discount.
              </Faq>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function Faq({ q, children }: { q: string; children: React.ReactNode }) {
  return (
    <div className="bg-gray-50 dark:bg-gray-900 rounded-xl p-6">
      <h3 className="font-semibold text-gray-900 dark:text-white">{q}</h3>
      <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">{children}</p>
    </div>
  );
}
