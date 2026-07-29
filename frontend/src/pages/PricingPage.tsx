import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { NavBar, Button, GlassPanel } from "../components/shared/ui";
import { api } from "../api/client";
import { useSession } from "../hooks/useSession";

const PLANS = [
  {
    id: "premium_single",
    name: "Single Resume",
    price: "₹199",
    features: ["Full AI rewriting", "Template preservation", "ATS scoring", "1 job description"],
  },
  {
    id: "premium_monthly",
    name: "Unlimited Monthly",
    price: "₹499/mo",
    features: ["Everything in Single", "Unlimited job descriptions", "Cover letter generator", "Interview prep"],
  },
];

export default function PricingPage() {
  const { sessionId } = useSession();
  const navigate = useNavigate();
  const [loadingPlan, setLoadingPlan] = useState<string | null>(null);

  async function handleCheckout(planId: string) {
    if (!sessionId) {
      navigate("/upload");
      return;
    }
    setLoadingPlan(planId);
    try {
      const order = await api.createOrder(sessionId, planId);
      // In production: open Razorpay Checkout with order.order_id / order.key_id here.
      // Mock mode (order.mock_mode === true) skips straight to success so the
      // flow is demoable without a real Razorpay account.
      if (order.mock_mode) {
        navigate("/payment-success");
      }
    } finally {
      setLoadingPlan(null);
    }
  }

  return (
    <div className="min-h-screen">
      <NavBar />
      <main className="max-w-3xl mx-auto px-6 py-16">
        <h1 className="text-2xl font-semibold mb-2 text-center">Unlock Premium AI Enhancement</h1>
        <p className="text-sm text-gray-400 mb-12 text-center">Full rewriting, cover letters, and interview prep.</p>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          {PLANS.map((plan) => (
            <GlassPanel key={plan.id} className="text-center">
              <h3 className="font-medium text-lg">{plan.name}</h3>
              <p className="text-3xl font-semibold my-4">{plan.price}</p>
              <ul className="text-sm text-gray-400 space-y-2 mb-6 text-left">
                {plan.features.map((f) => <li key={f}>• {f}</li>)}
              </ul>
              <Button onClick={() => handleCheckout(plan.id)} disabled={loadingPlan === plan.id}>
                {loadingPlan === plan.id ? "Redirecting..." : "Choose Plan"}
              </Button>
            </GlassPanel>
          ))}
        </div>
      </main>
    </div>
  );
}
