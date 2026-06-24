"use client";

import { FormEvent, useState } from "react";

type UploadState = "idle" | "uploading" | "success" | "error";

export function UploadPanel() {
  const [state, setState] = useState<UploadState>("idle");
  const [message, setMessage] = useState("Queue a creator upload for the future FFmpeg worker.");

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setState("uploading");
    setMessage("Sending upload metadata and file to the Projector API...");

    const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
    const form = new FormData(event.currentTarget);

    try {
      const response = await fetch(`${apiUrl}/api/videos/upload`, {
        method: "POST",
        body: form,
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: "Upload failed" }));
        throw new Error(error.detail ?? "Upload failed");
      }

      const video = await response.json();
      setState("success");
      setMessage(`Queued “${video.title}” as ${video.id}. Refresh the feed to see it in this in-memory MVP.`);
      event.currentTarget.reset();
    } catch (error) {
      setState("error");
      setMessage(error instanceof Error ? error.message : "Upload failed");
    }
  }

  return (
    <section className="panel upload-panel" id="upload">
      <div>
        <p className="eyebrow">Creator deck</p>
        <h2>Queue a video upload</h2>
        <p className="muted">This MVP validates video files and returns a queued record while storage, database persistence, and transcoding land next.</p>
      </div>
      <form onSubmit={handleSubmit}>
        <label>
          Title
          <input name="title" required maxLength={120} placeholder="Projector field report" />
        </label>
        <label>
          Channel
          <input name="channel" required maxLength={80} defaultValue="Projector Creator" />
        </label>
        <label>
          Description
          <textarea name="description" maxLength={500} placeholder="What should viewers know?" />
        </label>
        <label>
          Video file
          <input name="file" required type="file" accept="video/*" />
        </label>
        <button type="submit" disabled={state === "uploading"}>{state === "uploading" ? "Queuing..." : "Queue upload"}</button>
      </form>
      <p className={`notice ${state}`}>{message}</p>
    </section>
  );
}
