"use client";

import { ChangeEvent, useCallback, useEffect, useState } from "react";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

type DocumentItem = {
  id: number;
  filename: string;
  status: string;
  created_at: string;
};

function getStatusClass(status: string) {
  switch (status.toLowerCase()) {
    case "ready":
      return "bg-green-100 text-green-800";
    case "processing":
      return "bg-blue-100 text-blue-800";
    case "failed":
      return "bg-red-100 text-red-800";
    default:
      return "bg-slate-100 text-slate-700";
  }
}

export default function DocumentsPage() {
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [deletingId, setDeletingId] = useState<number | null>(null);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const loadDocuments = useCallback(async (showLoading = true) => {
    if (showLoading) setLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/documents/all`, {
        cache: "no-store",
      });

      if (!response.ok) {
        throw new Error(`Could not load documents (HTTP ${response.status}).`);
      }

      const data: DocumentItem[] = await response.json();
      setDocuments(data);
      setError("");
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Could not connect to the backend."
      );
    } finally {
      if (showLoading) setLoading(false);
    }
  }, []);

  useEffect(() => {
    void loadDocuments();

    const intervalId = window.setInterval(() => {
      void loadDocuments(false);
    }, 3000);

    return () => window.clearInterval(intervalId);
  }, [loadDocuments]);

  async function handleUpload(event: ChangeEvent<HTMLInputElement>) {
    const input = event.currentTarget;
    const file = input.files?.[0];

    if (!file) return;

    if (!/\.(pdf|txt)$/i.test(file.name)) {
      setError("Only PDF and TXT files are supported.");
      input.value = "";
      return;
    }

    setUploading(true);
    setError("");
    setMessage("");

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(`${API_BASE_URL}/documents/upload`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        let detail = `Upload failed (HTTP ${response.status}).`;

        try {
          const data = await response.json();
          detail = data.detail ?? detail;
        } catch {
          // Keep the fallback message.
        }

        throw new Error(detail);
      }

      const uploaded: DocumentItem = await response.json();

      setMessage(
        `${uploaded.filename} uploaded successfully. Processing may still be running.`
      );

      await loadDocuments(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload failed.");
    } finally {
      setUploading(false);
      input.value = "";
    }
  }

  async function handleDelete(document: DocumentItem) {
    if (
      !window.confirm(
        `Delete "${document.filename}"? This action cannot be undone.`
      )
    ) {
      return;
    }

    setDeletingId(document.id);
    setError("");
    setMessage("");

    try {
      const response = await fetch(
        `${API_BASE_URL}/documents/${document.id}`,
        { method: "DELETE" }
      );

      if (!response.ok) {
        let detail = `Delete failed (HTTP ${response.status}).`;

        try {
          const data = await response.json();
          detail = data.detail ?? detail;
        } catch {
          // Keep the fallback message.
        }

        throw new Error(detail);
      }

      setMessage(`"${document.filename}" was deleted.`);
      await loadDocuments(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Delete failed.");
    } finally {
      setDeletingId(null);
    }
  }

  return (
    <main className="min-h-screen bg-slate-50 text-slate-900">
      <div className="mx-auto max-w-5xl px-5 py-10">
        <nav className="mb-8 flex gap-5 text-sm font-medium">
          <a href="/" className="text-slate-600 hover:text-blue-700">
            Chat Assistant
          </a>
          <a href="/documents" className="text-blue-700">
            Documents
          </a>
        </nav>

        <header className="mb-8">
          <p className="text-sm font-semibold uppercase tracking-widest text-blue-700">
            Knowledge Base
          </p>
          <h1 className="mt-2 text-3xl font-bold">Document Management</h1>
          <p className="mt-3 text-slate-600">
            Upload and manage documents used by your AI assistant.
          </p>
        </header>

        <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="text-lg font-semibold">Upload a document</h2>
          <p className="mt-2 text-sm text-slate-600">
            Supported formats: PDF and TXT.
          </p>

          <label className="mt-5 inline-flex cursor-pointer items-center rounded-xl bg-blue-700 px-5 py-3 font-semibold text-white hover:bg-blue-800">
            {uploading ? "Uploading..." : "Choose file"}
            <input
              type="file"
              accept=".pdf,.txt,application/pdf,text/plain"
              disabled={uploading}
              onChange={handleUpload}
              className="sr-only"
            />
          </label>

          {uploading && (
            <p role="status" className="mt-3 text-sm text-slate-500">
              Uploading document...
            </p>
          )}
        </section>

        {message && (
          <p
            role="status"
            className="mt-5 rounded-xl border border-green-200 bg-green-50 p-4 text-sm text-green-800"
          >
            {message}
          </p>
        )}

        {error && (
          <div
            role="alert"
            className="mt-5 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700"
          >
            {error}
            <button
              onClick={() => void loadDocuments()}
              className="ml-3 font-semibold underline"
            >
              Retry
            </button>
          </div>
        )}

        <section className="mt-8">
          <div className="mb-4 flex items-center justify-between gap-3">
            <h2 className="text-xl font-bold">
              Your documents ({documents.length})
            </h2>
            <button
              onClick={() => void loadDocuments()}
              className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm hover:bg-slate-100"
            >
              Refresh
            </button>
          </div>

          {loading ? (
            <p className="rounded-xl bg-white p-6 text-slate-500">
              Loading documents...
            </p>
          ) : documents.length === 0 ? (
            <div className="rounded-2xl border border-dashed border-slate-300 bg-white p-10 text-center">
              <p className="font-semibold">No documents yet</p>
              <p className="mt-2 text-sm text-slate-500">
                Upload a PDF or TXT file to get started.
              </p>
            </div>
          ) : (
            <ul className="divide-y divide-slate-200 overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
              {documents.map((document) => (
                <li
                  key={document.id}
                  className="flex flex-col gap-4 p-5 sm:flex-row sm:items-center sm:justify-between"
                >
                  <div className="min-w-0 flex-1">
                    <p className="break-words font-semibold">
                      {document.filename}
                    </p>
                    <p className="mt-1 text-xs text-slate-500">
                      ID: {document.id}
                    </p>
                    <p className="mt-1 text-xs text-slate-500">
                      Created: {new Date(document.created_at).toLocaleString()}
                    </p>
                  </div>

                  <div className="flex items-center gap-3">
                    <span
                      className={`rounded-full px-3 py-1 text-xs font-semibold ${getStatusClass(document.status)}`}
                    >
                      {document.status}
                    </span>

                    <button
                      onClick={() => void handleDelete(document)}
                      disabled={deletingId === document.id}
                      className="rounded-lg border border-red-200 px-3 py-2 text-sm font-medium text-red-700 hover:bg-red-50 disabled:opacity-50"
                    >
                      {deletingId === document.id ? "Deleting..." : "Delete"}
                    </button>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </section>
      </div>
    </main>
  );
}
