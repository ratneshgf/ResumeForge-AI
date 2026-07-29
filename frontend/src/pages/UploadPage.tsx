import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { NavBar, Button, GlassPanel, Loader } from "../components/shared/ui";
import { api } from "../api/client";
import { useSession } from "../hooks/useSession";

export default function UploadPage() {
  const navigate = useNavigate();
  const { setUpload, setJobDescription, jobDescription } = useSession();
  const [file, setFile] = useState<File | null>(null);
  const [jdText, setJdText] = useState(jobDescription);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit() {
    if (!file || !jdText.trim()) {
      setError("Please attach a resume and paste the target job description.");
      return;
    }
    setError(null);
    setLoading(true);
    try {
      const uploadRes = await api.uploadResume(file);
      setUpload(uploadRes.session_id, uploadRes.resume_id, uploadRes.file_type, uploadRes.sections);
      setJobDescription(jdText);
      await api.analyzeJD(uploadRes.session_id, jdText);
      navigate("/analysis");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen">
      <NavBar />
      <main className="max-w-2xl mx-auto px-6 py-16">
        <h1 className="text-2xl font-semibold mb-8">Upload your resume</h1>

        <GlassPanel className="mb-6">
          <label className="block text-sm text-gray-400 mb-2">Resume (PDF or DOCX)</label>
          <input
            type="file"
            accept=".pdf,.docx"
            onChange={(e) => setFile(e.target.files?.[0] ?? null)}
            className="block w-full text-sm text-gray-300 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-accent-500 file:text-white hover:file:bg-accent-400"
          />
          {file && <p className="mt-2 text-xs text-gray-500">{file.name}</p>}
        </GlassPanel>

        <GlassPanel className="mb-6">
          <label className="block text-sm text-gray-400 mb-2">Target job description</label>
          <textarea
            rows={8}
            value={jdText}
            onChange={(e) => setJdText(e.target.value)}
            placeholder="Paste the job description here..."
            className="w-full bg-base-900 border border-white/10 rounded-lg p-3 text-sm text-gray-200 focus:outline-none focus:ring-1 focus:ring-accent-500"
          />
        </GlassPanel>

        {error && <p className="text-sm text-red-400 mb-4">{error}</p>}

        <div className="flex items-center gap-4">
          <Button onClick={handleSubmit} disabled={loading}>
            {loading ? "Analyzing..." : "Analyze Resume"}
          </Button>
          {loading && <Loader label="Parsing resume and analyzing job description" />}
        </div>
      </main>
    </div>
  );
}
