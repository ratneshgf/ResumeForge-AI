import { NavBar, Button, GlassPanel } from "../components/shared/ui";
import { api } from "../api/client";
import { useSession } from "../hooks/useSession";

export default function DownloadPage() {
  const { sessionId, fileType } = useSession();

  return (
    <div className="min-h-screen">
      <NavBar />
      <main className="max-w-md mx-auto px-6 py-24 text-center">
        <GlassPanel>
          <div className="text-4xl mb-4">📄</div>
          <h1 className="text-xl font-semibold mb-2">Your resume is ready</h1>
          <p className="text-sm text-gray-400 mb-6">
            Same design, optimized content — download your{" "}
            {fileType?.toUpperCase() ?? "resume"} below.
          </p>
          {sessionId ? (
            <a href={api.downloadUrl(sessionId)}>
              <Button>Download {fileType?.toUpperCase()}</Button>
            </a>
          ) : (
            <p className="text-sm text-red-400">No session found — start over from Upload.</p>
          )}
        </GlassPanel>
      </main>
    </div>
  );
}
