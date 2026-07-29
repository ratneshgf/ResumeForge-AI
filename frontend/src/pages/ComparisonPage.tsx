import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { NavBar, Button, GlassPanel, Loader } from "../components/shared/ui";
import { api } from "../api/client";
import { useSession } from "../hooks/useSession";

export default function ComparisonPage() {
  const navigate = useNavigate();
  const { sessionId, resumeId, jobDescription, changes, setChanges } = useSession();
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    if (!sessionId || !resumeId) {
      navigate("/upload");
      return;
    }
    api.enhanceFull(sessionId, resumeId, jobDescription)
      .then((res) => setChanges(res.changes))
      .finally(() => setLoading(false));
  }, [sessionId, resumeId, jobDescription, navigate, setChanges]);

  async function handleGenerate() {
    if (!sessionId) return;
    setGenerating(true);
    try {
      await api.generateDocument(sessionId);
      navigate("/download");
    } finally {
      setGenerating(false);
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen">
        <NavBar />
        <main className="max-w-2xl mx-auto px-6 py-24 text-center"><Loader label="Rewriting your resume sections" /></main>
      </div>
    );
  }

  return (
    <div className="min-h-screen">
      <NavBar />
      <main className="max-w-3xl mx-auto px-6 py-16">
        <h1 className="text-2xl font-semibold mb-2">Before &amp; After</h1>
        <p className="text-sm text-gray-400 mb-8">
          Only these sections change — your original formatting, fonts, and layout stay exactly as uploaded.
        </p>

        {changes.length === 0 && (
          <GlassPanel className="mb-6">
            <p className="text-sm text-gray-400">No changes suggested — your resume already matches the job description well.</p>
          </GlassPanel>
        )}

        <div className="space-y-4 mb-8">
          {changes.map((c, i) => (
            <GlassPanel key={i}>
              <p className="text-xs uppercase tracking-wide text-accent-400 mb-3">{c.heading}</p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <p className="text-xs text-gray-500 mb-1">Before</p>
                  <p className="text-sm text-gray-400 line-through decoration-red-500/40">{c.before}</p>
                </div>
                <div>
                  <p className="text-xs text-gray-500 mb-1">After</p>
                  <p className="text-sm text-gray-100">{c.after}</p>
                </div>
              </div>
            </GlassPanel>
          ))}
        </div>

        <Button onClick={handleGenerate} disabled={generating}>
          {generating ? "Generating..." : "Generate Final Resume"}
        </Button>
      </main>
    </div>
  );
}
