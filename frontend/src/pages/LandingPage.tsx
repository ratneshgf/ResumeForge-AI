import { useNavigate } from "react-router-dom";
import { NavBar, Button, GlassPanel } from "../components/shared/ui";

export default function LandingPage() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen">
      <NavBar />
      <main className="max-w-4xl mx-auto px-6 pt-24 pb-16 text-center">
        <h1 className="text-5xl font-semibold tracking-tight leading-tight">
          Optimize your resume.
          <br />
          <span className="text-accent-400">Keep your design.</span>
        </h1>
        <p className="mt-6 text-gray-400 text-lg max-w-2xl mx-auto">
          Upload your existing resume and a target job description. ResumeForge AI
          rewrites your objective, skills, and project bullets to match the role —
          without touching your fonts, spacing, or layout.
        </p>
        <div className="mt-10 flex justify-center gap-4">
          <Button onClick={() => navigate("/upload")}>Get Started</Button>
          <Button variant="ghost" onClick={() => navigate("/pricing")}>See Pricing</Button>
        </div>

        <div className="mt-20 grid grid-cols-1 sm:grid-cols-3 gap-4 text-left">
          <GlassPanel>
            <h3 className="font-medium mb-2">Template preserved</h3>
            <p className="text-sm text-gray-400">Your original fonts, colors, and layout stay exactly as they were.</p>
          </GlassPanel>
          <GlassPanel>
            <h3 className="font-medium mb-2">ATS scored</h3>
            <p className="text-sm text-gray-400">See your match score and missing keywords before you apply.</p>
          </GlassPanel>
          <GlassPanel>
            <h3 className="font-medium mb-2">No fabrication</h3>
            <p className="text-sm text-gray-400">Content is rewritten from what's already there — nothing invented.</p>
          </GlassPanel>
        </div>
      </main>
    </div>
  );
}
