import type { MetadataRoute } from "next";
import { loadLabs } from "@/engine/labs";
import { loadTracks } from "@/engine/tracks";
import { loadKnowledge } from "@/engine/knowledge";
import { loadHeritage } from "@/engine/heritage";
import { loadBooks, visibleBooks, visibleConcepts } from "@/engine/books";

const BASE = "https://detectiveacademy.app";

export default function sitemap(): MetadataRoute.Sitemap {
  const now = new Date();

  // Static pages
  const statics: MetadataRoute.Sitemap = [
    { url: `${BASE}/`, lastModified: now, changeFrequency: "weekly", priority: 1.0 },
    { url: `${BASE}/cases`, lastModified: now, changeFrequency: "weekly", priority: 0.9 },
    { url: `${BASE}/season`, lastModified: now, changeFrequency: "monthly", priority: 0.8 },
    { url: `${BASE}/academy`, lastModified: now, changeFrequency: "weekly", priority: 0.9 },
    { url: `${BASE}/labs`, lastModified: now, changeFrequency: "weekly", priority: 0.9 },
    { url: `${BASE}/knowledge`, lastModified: now, changeFrequency: "weekly", priority: 0.8 },
    { url: `${BASE}/challenges`, lastModified: now, changeFrequency: "daily", priority: 0.7 },
    { url: `${BASE}/glossary`, lastModified: now, changeFrequency: "monthly", priority: 0.6 },
    { url: `${BASE}/biases`, lastModified: now, changeFrequency: "monthly", priority: 0.6 },
    { url: `${BASE}/methods`, lastModified: now, changeFrequency: "monthly", priority: 0.6 },
    { url: `${BASE}/reasoning`, lastModified: now, changeFrequency: "monthly", priority: 0.6 },
    { url: `${BASE}/rulebook`, lastModified: now, changeFrequency: "monthly", priority: 0.5 },
    { url: `${BASE}/archetypes`, lastModified: now, changeFrequency: "monthly", priority: 0.5 },
    { url: `${BASE}/atlas`, lastModified: now, changeFrequency: "monthly", priority: 0.5 },
    { url: `${BASE}/skills`, lastModified: now, changeFrequency: "monthly", priority: 0.5 },
    { url: `${BASE}/books`, lastModified: now, changeFrequency: "monthly", priority: 0.4 },
    { url: `${BASE}/heritage`, lastModified: now, changeFrequency: "monthly", priority: 0.4 },
    { url: `${BASE}/gallery`, lastModified: now, changeFrequency: "monthly", priority: 0.3 },
    { url: `${BASE}/sounds`, lastModified: now, changeFrequency: "monthly", priority: 0.2 },
    { url: `${BASE}/privacy`, lastModified: now, changeFrequency: "yearly", priority: 0.3 },
    { url: `${BASE}/credits`, lastModified: now, changeFrequency: "yearly", priority: 0.2 },
    { url: `${BASE}/sources`, lastModified: now, changeFrequency: "yearly", priority: 0.2 },
  ];

  // Dynamic: labs
  const { playable } = loadLabs();
  const labUrls: MetadataRoute.Sitemap = playable.map((lab) => ({
    url: `${BASE}/labs/${lab.id}`,
    lastModified: now,
    changeFrequency: "monthly" as const,
    priority: 0.7,
  }));

  // Dynamic: academy lessons
  const { tracks } = loadTracks();
  const lessonUrls: MetadataRoute.Sitemap = tracks.flatMap((track) =>
    track.lessons.map((lesson) => ({
      url: `${BASE}/academy/${lesson.id}`,
      lastModified: now,
      changeFrequency: "monthly" as const,
      priority: 0.7,
    }))
  );

  // Dynamic: knowledge objects
  const { kos } = loadKnowledge();
  const koUrls: MetadataRoute.Sitemap = kos.map((ko) => ({
    url: `${BASE}/knowledge/${ko.ko_id}`,
    lastModified: now,
    changeFrequency: "monthly" as const,
    priority: 0.5,
  }));

  // Dynamic: heritage texts (public domain / cc ref only)
  const { texts } = loadHeritage();
  const heritageUrls: MetadataRoute.Sitemap = texts.map((t) => ({
    url: `${BASE}/heritage/${t.id}`,
    lastModified: now,
    changeFrequency: "yearly" as const,
    priority: 0.4,
  }));

  // Dynamic: books and concepts (visible to all age bands)
  const { books, concepts } = loadBooks();
  const visBooks = visibleBooks(books, null);
  const bookUrls: MetadataRoute.Sitemap = visBooks.map((b) => ({
    url: `${BASE}/books/${b.id}`,
    lastModified: now,
    changeFrequency: "monthly" as const,
    priority: 0.4,
  }));
  const visConcepts = visibleConcepts(concepts, books, null);
  const conceptUrls: MetadataRoute.Sitemap = visConcepts.map((c) => ({
    url: `${BASE}/books/concept/${c.id}`,
    lastModified: now,
    changeFrequency: "monthly" as const,
    priority: 0.3,
  }));

  return [...statics, ...labUrls, ...lessonUrls, ...koUrls, ...heritageUrls, ...bookUrls, ...conceptUrls];
}
