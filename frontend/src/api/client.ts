const BASE_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, options);
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`${res.status} ${res.statusText}: ${body}`);
  }
  return res.json();
}

export interface RunStyle {
  bold: boolean;
  italic: boolean;
  size_pt: number | null;
  color: string | null;
  name: string | null;
}
export interface RunModel { run_index: number; text: string; style: RunStyle }
export interface ParagraphModel { para_index: number; style_name: string; text: string; runs: RunModel[] }
export interface SectionModel { heading: string; paragraphs: ParagraphModel[] }

export interface ResumeUploadResponse {
  session_id: string;
  resume_id: string;
  file_type: string;
  sections: SectionModel[];
}

export interface JDAnalyzeResponse {
  required_skills: string[];
  preferred_skills: string[];
  keywords: string[];
}

export interface SectionChange { para_index: number; heading: string; before: string; after: string }
export interface EnhanceResponse { session_id: string; resume_id: string; changes: SectionChange[] }

export interface ATSScoreResponse {
  score: number;
  skills_match_pct: number;
  keyword_match_pct: number;
  matched_skills: string[];
  missing_skills: string[];
  suggestions: string[];
}

export const api = {
  uploadResume: (file: File) => {
    const form = new FormData();
    form.append("file", file);
    return request<ResumeUploadResponse>("/api/v1/resume/upload", { method: "POST", body: form });
  },

  analyzeJD: (session_id: string, job_description: string) =>
    request<JDAnalyzeResponse>("/api/v1/jd/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id, job_description }),
    }),

  getATSScore: (session_id: string, resume_id: string, job_description: string) =>
    request<ATSScoreResponse>("/api/v1/ats/score", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id, resume_id, job_description }),
    }),

  enhanceFull: (session_id: string, resume_id: string, job_description: string) =>
    request<EnhanceResponse>("/api/v1/enhance/full", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id, resume_id, job_description }),
    }),

  generateDocument: (session_id: string) =>
    request<{ session_id: string; file_type: string; ready: boolean }>(
      `/api/v1/document/generate?session_id=${session_id}`,
      { method: "POST" }
    ),

  downloadUrl: (session_id: string) => `${BASE_URL}/api/v1/document/download/${session_id}`,

  createOrder: (session_id: string, plan = "premium_single") =>
    request<{ order_id: string; amount: number; currency: string; key_id: string; mock_mode: boolean }>(
      "/api/v1/payment/create-order",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id, plan }),
      }
    ),
};
