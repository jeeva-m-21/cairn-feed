const events = [
  {
    category: "MODEL RELEASE",
    title: "Open models are getting smaller without getting quiet",
    summary: "A new family of compact reasoning models trades scale for deployability—and changes what teams can run at the edge.",
    sourceCount: 8,
    age: "18 min ago",
    relevance: "Matches your interest in inference and open source",
    signal: "MODEL SHIFT",
  },
  {
    category: "DEVELOPER TOOLS",
    title: "The agent stack is settling around durable primitives",
    summary: "Three new releases point to the same pattern: traces, permissions, and resumable work before clever autonomy.",
    sourceCount: 5,
    age: "2 hr ago",
    relevance: "You follow AI agents and developer infrastructure",
    signal: "PATTERN",
  },
  {
    category: "RESEARCH",
    title: "A benchmark result worth reading past the headline",
    summary: "The reported gain is real, but the evaluation conditions make it narrower than the first wave of coverage suggests.",
    sourceCount: 4,
    age: "5 hr ago",
    relevance: "Research depth: advanced · evidence available",
    signal: "EVIDENCE",
  },
];

export default function Home() {
  return (
    <main className="app-shell">
      <aside className="sidebar">
        <div className="brand-lockup">
          <div className="cairn-mark" aria-hidden="true"><span /><span /><span /></div>
          <span className="brand-name">cairn</span>
        </div>
        <p className="sidebar-intro">A quieter way to stay ahead of the AI and developer world.</p>
        <nav aria-label="Primary navigation">
          <a className="nav-item active" href="#feed"><span>⌂</span> Feed <b>7</b></a>
          <a className="nav-item" href="#brief"><span>◌</span> Brief</a>
          <a className="nav-item" href="#alerts"><span>⌁</span> Alerts</a>
          <a className="nav-item" href="#saved"><span>◇</span> Saved</a>
          <a className="nav-item" href="#search"><span>⌕</span> Search</a>
        </nav>
        <div className="sidebar-bottom">
          <div className="trail-note"><span className="dot" /> Last synced <strong>3 min ago</strong></div>
          <button className="profile-button" type="button"><span className="avatar">JM</span><span>Jeeva M.</span><span className="chevron">⌄</span></button>
        </div>
      </aside>

      <section className="content" id="feed">
        <header className="topbar">
          <div><p className="eyebrow">Thursday, 03 September 2026</p><h1>Good morning, Jeeva.</h1></div>
          <button className="icon-button" type="button" aria-label="Open search">⌕</button>
        </header>

        <div className="feed-heading">
          <div><h2>7 things worth knowing</h2><p>Since your last visit <span className="long-dash">—</span> filtered for signal, not volume.</p></div>
          <button className="text-button" type="button">Tune your feed <span>→</span></button>
        </div>

        <div className="section-label"><span>For you</span><span className="section-rule" /><span className="section-count">03</span></div>
        <div className="event-list">
          {events.map((event, index) => (
            <article className={`event-card ${index === 0 ? "featured" : ""}`} key={event.title}>
              <div className="event-number">0{index + 1}</div>
              <div className="event-body">
                <div className="event-meta"><span className="category">{event.category}</span><span>{event.age}</span><span>{event.sourceCount} sources</span></div>
                <h3>{event.title}</h3><p className="event-summary">{event.summary}</p>
                <div className="event-footer"><span className="relevance"><span className="spark">✦</span>{event.relevance}</span><span className="signal-chip">{event.signal}</span><button className="brief-link" type="button">Read brief <span>↗</span></button></div>
              </div>
            </article>
          ))}
        </div>

        <div className="lower-grid">
          <section><div className="section-label"><span>Deep dive</span><span className="section-rule" /><span className="section-count">01</span></div><div className="deep-dive"><span className="mini-label">DEVELOPING STORY</span><h3>What happens after the model launch?</h3><p>Follow the evidence as it accumulates across papers, code, and real-world use.</p><button className="text-button" type="button">Open thread <span>→</span></button></div></section>
          <section><div className="section-label"><span>Reading note</span><span className="section-rule" /></div><blockquote>“The best feed is the one that lets you close it.”</blockquote><p className="note-caption">— Cairn principle / 04</p></section>
        </div>
      </section>

      <aside className="right-rail"><div className="rail-heading"><span>Field notes</span><span className="live-indicator"><i /> LIVE</span></div><div className="rail-card"><p className="rail-kicker">YOUR SIGNAL</p><div className="signal-score">82<span>/100</span></div><p>Signal-to-noise this week</p><div className="score-bar"><span /></div><small>Up 9 points from last week</small></div><div className="rail-card next-up"><p className="rail-kicker">NEXT UP</p><div className="next-item"><span className="next-icon">◈</span><div><strong>5 papers</strong><p>in your research queue</p></div><span>→</span></div><div className="next-item"><span className="next-icon">◌</span><div><strong>2 topics</strong><p>need your attention</p></div><span>→</span></div></div><div className="trail-marker"><div className="marker-stones"><span /><span /><span /></div><p>Keep moving<br /><em>the path gets clearer.</em></p></div></aside>
    </main>
  );
}
