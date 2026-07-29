import { Routes, Route } from "react-router-dom";
import { SessionProvider } from "./hooks/useSession";
import LandingPage from "./pages/LandingPage";
import UploadPage from "./pages/UploadPage";
import AnalysisDashboardPage from "./pages/AnalysisDashboardPage";
import ComparisonPage from "./pages/ComparisonPage";
import PricingPage from "./pages/PricingPage";
import PaymentSuccessPage from "./pages/PaymentSuccessPage";
import DownloadPage from "./pages/DownloadPage";

export default function App() {
  return (
    <SessionProvider>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/upload" element={<UploadPage />} />
        <Route path="/analysis" element={<AnalysisDashboardPage />} />
        <Route path="/comparison" element={<ComparisonPage />} />
        <Route path="/pricing" element={<PricingPage />} />
        <Route path="/payment-success" element={<PaymentSuccessPage />} />
        <Route path="/download" element={<DownloadPage />} />
      </Routes>
    </SessionProvider>
  );
}
