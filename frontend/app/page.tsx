type Video = {
  id: string;
  title: string;
  channel: string;
  status: string;
  description: string;
};

async function getVideos(): Promise<Video[]> {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
  try {
    const response = await fetch(`${apiUrl}/api/videos`, { next: { revalidate: 30 } });
    if (!response.ok) return [];
    return response.json();
  } catch {
    return [];
  }
}

export default async function Home() {
  const videos = await getVideos();

  return (
    <main className="shell">
      <section className="hero">
        <p className="eyebrow">Self-hosted video sovereignty</p>
        <h1>Projector projects truth, one frame at a time.</h1>
        <p className="lede">
          A Docker-first, privacy-respecting video platform foundation with a FastAPI backend,
          Next.js command deck, and space for the transcoding pipeline to ignite.
        </p>
        <div className="actions">
          <a href="http://localhost:8000/docs">Open API docs</a>
          <a href="#videos" className="secondary">View bootstrap feed</a>
        </div>
      </section>

      <section id="videos" className="panel">
        <div>
          <p className="eyebrow">MVP feed</p>
          <h2>Ready for uploads and HLS playback</h2>
        </div>
        <div className="grid">
          {videos.map((video) => (
            <article className="card" key={video.id}>
              <span>{video.status}</span>
              <h3>{video.title}</h3>
              <p>{video.description}</p>
              <small>{video.channel}</small>
            </article>
          ))}
          {videos.length === 0 && <p>Start the backend to load the bootstrap feed.</p>}
        </div>
      </section>
    </main>
  );
}
