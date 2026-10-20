"use client";

import { FormEvent, useState } from "react";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

type Source = {
  filename?: string;
  content?: string;
  score?: number;
  chunk_id?: number;
  document_id?: number;
};

type ChatResponse = {
  answer: string;
  sources: Source[];
};

export default function Home() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState<Source[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const trimmedQuestion = question.trim();
    if (!trimmedQuestion || loading) return;

    setLoading(true);
    setError("");
    setAnswer("");
    setSources([]);

    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: trimmedQuestion,
          top_k: 5,
        }),
      });

      if (!response.ok) {
        let message = `Request failed (${response.status})`;

        try {
          const errorData = await response.json();
          message = errorData.detail ?? message;
        } catch {
          // Keep the fallback message if the response is not JSON.
        }

        throw new Error(message);
      }

      const data: ChatResponse = await response.json();

      setAnswer(data.answer ?? "No answer returned.");
      setSources(data.sources ?? []);
    } catch (err) {
      setError(
        err instanceof TypeError
          ? "Cannot connect to the backend. Check that FastAPI is running and the API URL is correct."
          : err instanceof Error
            ? err.message
            : "Something went wrong. Please try again."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-slate-50 text-slate-900">
      <div className="mx-auto max-w-4xl px-5 py-12">
        <header className="mb-10">
          <p className="mb-2 text-sm font-semibold uppercase tracking-widest text-blue-700">
            AI Knowledge Assistant
          </p>
          <h1 className="text-3xl font-bold tracking-tight sm:text-4xl">
            Ask your documents
          </h1>
          <p className="mt-3 text-slate-600">
            Ask a question and get an answer grounded in your uploaded
            documents, with source references.
          </p>
        </header>

        <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-7">
          <form onSubmit={handleSubmit}>
            <label
              htmlFor="question"
              className="mb-2 block text-sm font-semibold"
            >
              Your question
            </label>

            <textarea
              id="question"
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              placeholder="Ask something about your documents..."
              rows={4}
              disabled={loading}
              className="w-full resize-y rounded-xl border border-slate-300 p-4 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100 disabled:bg-slate-100"
            />

            <div className="mt-4 flex justify-end">
              <button
                type="submit"
                disabled={loading || !question.trim()}
                className="rounded-xl bg-blue-700 px-6 py-3 font-semibold text-white transition hover:bg-blue-800 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {loading ? "Thinking..." : "Ask AI"}
              </button>
            </div>
          </form>

          {loading && (
            <p role="status" className="mt-5 text-sm text-slate-500">
              Searching your documents and generating an answer...
            </p>
          )}

          {error && (
            <div
              role="alert"
              className="mt-6 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700"
            >
              {error}
            </div>
          )}
        </section>

        {answer && (
          <section className="mt-8 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-7">
            <h2 className="text-xl font-bold">Answer</h2>
            <div className="mt-4 whitespace-pre-wrap leading-7 text-slate-700">
              {answer}
            </div>

            <div className="mt-8 border-t border-slate-200 pt-5">
              <h3 className="text-lg font-semibold">
                Sources ({sources.length})
              </h3>

              {sources.length === 0 ? (
                <p className="mt-3 text-sm text-slate-500">
                  No source references were returned.
                </p>
              ) : (
                <ul className="mt-4 space-y-4">
                  {sources.map((source, index) => (
                    <li
                      key={`${source.document_id ?? "doc"}-${source.chunk_id ?? index}-${index}`}
                      className="rounded-xl bg-slate-50 p-4"
                    >
                      <div className="flex flex-wrap items-center justify-between gap-2">
                        <p className="font-semibold text-slate-800">
                          {source.filename ?? `Source ${index + 1}`}
                        </p>
                        {typeof source.score === "number" && (
                          <span className="text-xs text-slate-500">
                            Similarity: {source.score.toFixed(3)}
                          </span>
                        )}
                      </div>

                      {source.content && (
                        <p className="mt-2 whitespace-pre-wrap text-sm leading-6 text-slate-600">
                          {source.content}
                        </p>
                      )}
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </section>
        )}

        <footer className="mt-10 text-center text-sm text-slate-500">
          AI Knowledge Assistant · FastAPI · RAG · Ollama
        </footer>
      </div>
    </main>
  );
}