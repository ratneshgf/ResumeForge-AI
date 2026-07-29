import React, { createContext, useContext, useState } from "react";
import type { SectionModel, SectionChange } from "../api/client";

interface SessionState {
  sessionId: string | null;
  resumeId: string | null;
  fileType: string | null;
  sections: SectionModel[];
  jobDescription: string;
  changes: SectionChange[];
  setUpload: (sessionId: string, resumeId: string, fileType: string, sections: SectionModel[]) => void;
  setJobDescription: (jd: string) => void;
  setChanges: (changes: SectionChange[]) => void;
}

const SessionContext = createContext<SessionState | null>(null);

export function SessionProvider({ children }: { children: React.ReactNode }) {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [resumeId, setResumeId] = useState<string | null>(null);
  const [fileType, setFileType] = useState<string | null>(null);
  const [sections, setSections] = useState<SectionModel[]>([]);
  const [jobDescription, setJobDescriptionState] = useState("");
  const [changes, setChangesState] = useState<SectionChange[]>([]);

  const setUpload = (sid: string, rid: string, ft: string, secs: SectionModel[]) => {
    setSessionId(sid);
    setResumeId(rid);
    setFileType(ft);
    setSections(secs);
  };

  return (
    <SessionContext.Provider
      value={{
        sessionId,
        resumeId,
        fileType,
        sections,
        jobDescription,
        changes,
        setUpload,
        setJobDescription: setJobDescriptionState,
        setChanges: setChangesState,
      }}
    >
      {children}
    </SessionContext.Provider>
  );
}

export function useSession() {
  const ctx = useContext(SessionContext);
  if (!ctx) throw new Error("useSession must be used within SessionProvider");
  return ctx;
}
