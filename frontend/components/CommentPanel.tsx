"use client";

import { FormEvent, useState } from "react";

type Comment = {
  id: string;
  author: string;
  body: string;
  parent_id?: string | null;
  created_at: string;
};

type CommentPanelProps = {
  videoId: string;
  initialComments: Comment[];
};

type CommentState = "idle" | "posting" | "success" | "error";

export function CommentPanel({ videoId, initialComments }: CommentPanelProps) {
  const [comments, setComments] = useState(initialComments);
  const [state, setState] = useState<CommentState>("idle");
  const [message, setMessage] = useState("Keep the discussion transparent, local, and accountable to this instance.");

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setState("posting");
    setMessage("Publishing comment to the Projector API...");

    const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
    const form = new FormData(event.currentTarget);
    const payload = {
      author: String(form.get("author") ?? "Projector Viewer"),
      body: String(form.get("body") ?? ""),
    };

    try {
      const response = await fetch(`${apiUrl}/api/videos/${videoId}/comments`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: "Comment failed" }));
        throw new Error(error.detail ?? "Comment failed");
      }

      const comment = await response.json();
      setComments((current) => [...current, comment]);
      setState("success");
      setMessage("Comment published. The local conversation is updated instantly.");
      event.currentTarget.reset();
    } catch (error) {
      setState("error");
      setMessage(error instanceof Error ? error.message : "Comment failed");
    }
  }

  return (
    <section className="panel comments-panel" id="comments">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Community signals</p>
          <h2>Threaded comment foundation</h2>
        </div>
        <p className="muted">{comments.length} comment{comments.length === 1 ? "" : "s"}</p>
      </div>

      <div className="comment-list">
        {comments.map((comment) => (
          <article className="comment-card" key={comment.id}>
            <div>
              <strong>{comment.author}</strong>
              <time dateTime={comment.created_at}>{new Date(comment.created_at).toLocaleString()}</time>
            </div>
            <p>{comment.body}</p>
          </article>
        ))}
        {comments.length === 0 && <p className="muted">No comments yet. Start the local thread without third-party trackers.</p>}
      </div>

      <form onSubmit={handleSubmit} className="comment-form">
        <label>
          Display name
          <input name="author" maxLength={80} defaultValue="Projector Viewer" />
        </label>
        <label>
          Comment
          <textarea name="body" required maxLength={500} placeholder="Add context, corrections, or encouragement..." />
        </label>
        <button type="submit" disabled={state === "posting"}>{state === "posting" ? "Posting..." : "Post comment"}</button>
      </form>
      <p className={`notice ${state}`}>{message}</p>
    </section>
  );
}
