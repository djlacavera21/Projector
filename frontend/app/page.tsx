import { UploadPanel } from "../components/UploadPanel";

type Video = {
  id: string;
  title: string;
  channel: string;
  status: string;
  description: string;
  hls_url?: string | null;
  created_at: string;
};

type InstancePolicy = {
  name: string;
  tagline: string;
  viewing_requires_account: boolean;
  trackers_allowed: boolean;
  monetization_default: string;
  federation_phase: string;
  principles: { title: string; summary: string }[];
};

type InstanceStats = {
  total_videos: number;
  ready_videos: number;
  queued_videos: number;
  processing_videos: number;
  channels: number;
};

const fallbackPolicy: InstancePolicy = {
  name: "Projector Sovereign Instance",
  tagline: "Projecting truth, one frame at a time.",
  viewing_requires_account: false,
  trackers_allowed: false,
  monetization_default: "creator-direct",
  federation_phase: "planned",
  principles: [
    {
      title: "Privacy by default",
      summary: "No mandatory account for viewing, no third-party trackers, and self-hostable data ownership.",
    },
  ],
};

const fallbackStats: InstanceStats = {
  total_videos: 0,
  ready_videos: 0,
  queued_videos: 0,
  processing_videos: 0,
  channels: 0,
};

async function getJson<T>(path: string, fallback: T): Promise<T> {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
  try {
    const response = await fetch(`${apiUrl}${path}`, { next: { revalidate: 30 } });
    if (!response.ok) return fallback;
    return response.json();
  } catch {
    return fallback;
  }
}

export default async function Home() {
  const [videos, policy, stats] = await Promise.all([
    getJson<Video[]>("/api/videos", []),
    getJson<InstancePolicy>("/api/instance/policy", fallbackPolicy),
    getJson<InstanceStats>("/api/instance/stats", fallbackStats),
  ]);

  return (
    <main className="shell">
      <section className="hero">
        <p className="eyebrow">Self-hosted video sovereignty</p>
        <h1>{policy.name} projects truth, one frame at a time.</h1>
        <p className="lede">
          A Docker-first, privacy-respecting video platform foundation with a FastAPI backend,
          Next.js command deck, transparent instance policy, and a creator upload queue ready for the transcoding pipeline to ignite.
        </p>
        <div className="actions">
          <a href="http://localhost:8000/docs">Open API docs</a>
          <a href="#upload" className="secondary">Queue upload</a>
          <a href="#charter" className="secondary">Read instance charter</a>
        </div>
      </section>

      <section className="panel stat-panel" aria-label="Instance statistics">
        <div><strong>{stats.total_videos}</strong><span>videos</span></div>
        <div><strong>{stats.ready_videos}</strong><span>ready</span></div>
        <div><strong>{stats.processing_videos + stats.queued_videos}</strong><span>in pipeline</span></div>
        <div><strong>{stats.channels}</strong><span>channels</span></div>
      </section>

      <section id="charter" className="panel charter-panel">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Instance charter</p>
            <h2>{policy.tagline}</h2>
          </div>
          <div className="policy-pills">
            <span>{policy.viewing_requires_account ? "Account-gated" : "Anonymous viewing"}</span>
            <span>{policy.trackers_allowed ? "Trackers allowed" : "No third-party trackers"}</span>
            <span>{policy.monetization_default}</span>
            <span>Federation: {policy.federation_phase}</span>
          </div>
        </div>
        <div className="principle-grid">
          {policy.principles.map((principle) => (
            <article className="principle-card" key={principle.title}>
              <h3>{principle.title}</h3>
              <p>{principle.summary}</p>
            </article>
          ))}
        </div>
      </section>

      <UploadPanel />

      <section id="videos" className="panel">
        <div className="section-heading">
          <div>
            <p className="eyebrow">MVP feed</p>
            <h2>Ready for uploads and HLS playback</h2>
          </div>
          <p className="muted">{videos.length} bootstrap record{videos.length === 1 ? "" : "s"}</p>
        </div>
        <div className="grid">
          {videos.map((video) => (
            <article className="card" key={video.id}>
              <div className="status-row">
                <span>{video.status}</span>
                {video.hls_url && <small>HLS ready</small>}
              </div>
              <h3>{video.title}</h3>
              <p>{video.description}</p>
              <div className="card-footer">
                <small>{video.channel}</small>
                <a href={`/watch/${video.id}`}>Watch</a>
              </div>
            </article>
          ))}
          {videos.length === 0 && <p>Start the backend to load the bootstrap feed.</p>}
        </div>
      </section>
    </main>
  );
}
