type Video = {
  id: string;
  title: string;
  channel: string;
  status: string;
  description: string;
  hls_url?: string | null;
  created_at: string;
};

async function getVideo(id: string): Promise<Video | null> {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
  try {
    const response = await fetch(`${apiUrl}/api/videos/${id}`, { next: { revalidate: 30 } });
    if (!response.ok) return null;
    return response.json();
  } catch {
    return null;
  }
}

export default async function WatchPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const video = await getVideo(id);

  if (!video) {
    return (
      <main className="shell">
        <section className="panel">
          <p className="eyebrow">Signal missing</p>
          <h1>Video not found</h1>
          <p className="muted">The requested Projector record is not available in this MVP feed.</p>
          <a className="button-link" href="/">Return to command deck</a>
        </section>
      </main>
    );
  }

  const createdAt = new Intl.DateTimeFormat("en", { dateStyle: "medium", timeStyle: "short" }).format(
    new Date(video.created_at),
  );

  return (
    <main className="shell watch-shell">
      <section className="player-frame">
        {video.hls_url ? (
          <video controls playsInline poster="" src={video.hls_url} />
        ) : (
          <div className="processing-slate">
            <p className="eyebrow">{video.status}</p>
            <h2>Awaiting HLS renditions</h2>
            <p className="muted">This queued asset will become playable after the FFmpeg worker publishes adaptive streams.</p>
          </div>
        )}
      </section>

      <section className="panel watch-meta">
        <div>
          <p className="eyebrow">{video.status}</p>
          <h1>{video.title}</h1>
          <p className="lede">{video.description}</p>
        </div>
        <aside className="meta-card">
          <strong>{video.channel}</strong>
          <span>{createdAt}</span>
          <span>ID: {video.id}</span>
        </aside>
      </section>
    </main>
  );
}
