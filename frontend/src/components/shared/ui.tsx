import React from "react";

export function GlassPanel({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return <div className={`glass-panel rounded-2xl p-6 ${className}`}>{children}</div>;
}

export function Button({
  children,
  onClick,
  disabled,
  variant = "primary",
  type = "button",
}: {
  children: React.ReactNode;
  onClick?: () => void;
  disabled?: boolean;
  variant?: "primary" | "ghost";
  type?: "button" | "submit";
}) {
  const base = "px-5 py-2.5 rounded-xl font-medium text-sm transition-all disabled:opacity-40 disabled:cursor-not-allowed";
  const styles =
    variant === "primary"
      ? "bg-accent-500 hover:bg-accent-400 text-white shadow-lg shadow-accent-500/20"
      : "border border-white/10 hover:bg-white/5 text-gray-200";
  return (
    <button type={type} onClick={onClick} disabled={disabled} className={`${base} ${styles}`}>
      {children}
    </button>
  );
}

export function Loader({ label }: { label?: string }) {
  return (
    <div className="flex items-center gap-2 text-sm text-gray-400">
      <span className="h-2 w-2 rounded-full bg-accent-400 animate-pulse" />
      {label ?? "Working..."}
    </div>
  );
}

export function NavBar() {
  return (
    <header className="border-b border-white/5">
      <div className="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between">
        <span className="font-semibold tracking-tight text-lg">
          ResumeForge <span className="text-accent-400">AI</span>
        </span>
        <nav className="flex gap-6 text-sm text-gray-400">
          <a href="/" className="hover:text-white transition-colors">Home</a>
          <a href="/upload" className="hover:text-white transition-colors">Upload</a>
          <a href="/pricing" className="hover:text-white transition-colors">Pricing</a>
        </nav>
      </div>
    </header>
  );
}
