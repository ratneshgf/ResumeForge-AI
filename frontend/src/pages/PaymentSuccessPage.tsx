import { useNavigate } from "react-router-dom";
import { NavBar, Button, GlassPanel } from "../components/shared/ui";

export default function PaymentSuccessPage() {
  const navigate = useNavigate();
  return (
    <div className="min-h-screen">
      <NavBar />
      <main className="max-w-md mx-auto px-6 py-24 text-center">
        <GlassPanel>
          <div className="text-4xl mb-4">✓</div>
          <h1 className="text-xl font-semibold mb-2">Premium unlocked</h1>
          <p className="text-sm text-gray-400 mb-6">
            Your premium AI features are active for this session.
          </p>
          <Button onClick={() => navigate("/comparison")}>Continue</Button>
        </GlassPanel>
      </main>
    </div>
  );
}
