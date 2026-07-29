import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { NavBar, Button, GlassPanel, Loader } from "../components/shared/ui";
import { api, type ATSScoreResponse } from "../api/client";
import { useSession } from "../hooks/useSession";

function ScoreRing({ value }: { value: number }) {
  const circumference = 2 * Math.PI * 54;
  const offset = circumference - (value / 100) * circumference;
  return (
    <svg width="140" height="140" className="mx-auto">
      <circle cx="70" cy="70" r="54" stroke="#1f1f2b" strokeWidth="12" fill="none" />
      <circle
        cx="70" cy="70" r="54" stroke="#6366f1" strokeWidth="12" fill="none"
        strokeDasharray={circumference} strokeDashoffset={offset}
        strokeLinecap="round" transform="rotate(-90 70 70)"
      />
      <text x="70" y="78" textAnchor="middle" fontSize="28" fill="#f3f4f6" fontWeight="600">
        {value}
      </text>
    </svg>
  );
}

export default function AnalysisDashboardPage() {
  const navigate = useNavigate();
  const { sessionId, resumeId, jobDescription } = useSession();
  const [ats, setAts] = useState<ATSScoreResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!sessionId || !resumeId) {
      navigate("/upload");
      return;
    }
    api.getATSScore(sessionId, resumeId, jobDescription).then(setAts).finally(() => setLoading(false));
  }, [sessionId, resumeId, jobDescription, navigate]);

  if (loading) {
    return (
      <div className="min-h-screen">
        <NavBar />
        <main className="max-w-2xl mx-auto px-6 py-24 text-center"><Loader label="Scoring your resume against the job description" /></main>
      </div>
    );
  }

  if (!ats) return null;

  return (
    <div className="min-h-screen">
      <NavBar />
      <main className="max-w-3xl mx-auto px-6 py-16">
        <h1 className="text-2xl font-semibold mb-8">ATS Analysis</h1>

        <GlassPanel className="mb-6 text-center">
          <ScoreRing value={ats.score} />
          <p className="mt-2 text-sm text-gray-400">Overall ATS Score</p>
        </GlassPanel>

        <div className="grid grid-cols-2 gap-4 mb-6">
          <GlassPanel>
            <p className="text-sm text-gray-400 mb-1">Skills Match</p>
            <p className="text-2xl font-semibold">{ats.skills_match_pct}%</p>
          </GlassPanel>
          <GlassPanel>
            <p className="text-sm text-gray-400 mb-1">Keyword Match</p>
            <p className="text-2xl font-semibold">{ats.keyword_match_pct}%</p>
          </GlassPanel>
        </div>

        <GlassPanel className="mb-6">
          <p className="text-sm text-gray-400 mb-2">Matched skills</p>
          <div className="flex flex-wrap gap-2 mb-4">
            {ats.matched_skills.map((s) => (
              <span key={s} className="text-xs px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">{s}</span>
            ))}
          </div>
          <p className="text-sm text-gray-400 mb-2">Missing skills</p>
          <div className="flex flex-wrap gap-2">
            {ats.missing_skills.map((s) => (
              <span key={s} className="text-xs px-2.5 py-1 rounded-full bg-red-500/10 text-red-400 border border-red-500/20">{s}</span>
            ))}
          </div>
        </GlassPanel>

        {ats.suggestions.length > 0 && (
          <GlassPanel className="mb-6">
            <p className="text-sm text-gray-400 mb-2">Suggestions</p>
            <ul className="list-disc list-inside text-sm text-gray-300 space-y-1">
              {ats.suggestions.map((s, i) => <li key={i}>{s}</li>)}
            </ul>
          </GlassPanel>
        )}

        <Button onClick={() => navigate("/comparison")}>Continue to AI Enhancement</Button>
      </main>
    </div>
  );
}
