#!/usr/bin/env node
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";

const DEFAULT_SEED =
  "https://developer.salesforce.com/docs/data/data-cloud-dev/guide/dc-get-started.html";
const DEFAULT_OUTDIR = "docs/data360/developer";
const ORIGIN = "https://developer.salesforce.com";

function argValue(name, fallback) {
  const idx = process.argv.indexOf(name);
  if (idx === -1 || idx + 1 >= process.argv.length) return fallback;
  return process.argv[idx + 1];
}

function decodeHtml(value) {
  return String(value)
    .replace(/&quot;/g, '"')
    .replace(/&#x27;/g, "'")
    .replace(/&#39;/g, "'")
    .replace(/&#x26;/g, "&")
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&nbsp;/g, " ")
    .replace(/&#(\d+);/g, (_, n) => String.fromCodePoint(Number(n)))
    .replace(/&#x([0-9a-fA-F]+);/g, (_, n) => String.fromCodePoint(parseInt(n, 16)));
}

function textFromHtml(html) {
  return decodeHtml(
    String(html)
      .replace(/<script[\s\S]*?<\/script>/gi, "")
      .replace(/<style[\s\S]*?<\/style>/gi, "")
      .replace(/<doc-content-callout[^>]*header="([^"]+)"[^>]*>/gi, "\n\n> $1: ")
      .replace(/<\/doc-content-callout>/gi, "\n\n")
      .replace(/<doc-heading[^>]*header="([^"]+)"[^>]*><\/doc-heading>/gi, "\n\n## $1\n")
      .replace(/<h([1-6])[^>]*>/gi, (_, level) => `\n\n${"#".repeat(Number(level))} `)
      .replace(/<\/h[1-6]>/gi, "\n")
      .replace(/<li[^>]*>/gi, "\n- ")
      .replace(/<\/li>/gi, "\n")
      .replace(/<br\s*\/?>/gi, "\n")
      .replace(/<\/p>/gi, "\n\n")
      .replace(/<\/tr>/gi, "\n")
      .replace(/<\/t[hd]>/gi, " | ")
      .replace(/<[^>]+>/g, "")
  )
    .replace(/[ \t]+\n/g, "\n")
    .replace(/\n{3,}/g, "\n\n")
    .replace(/[ \t]{2,}/g, " ")
    .trim();
}

function extractAttr(tag, attr) {
  const re = new RegExp(`${attr}="([^"]*)"`);
  const match = tag.match(re);
  return match ? decodeHtml(match[1]) : "";
}

function extractSidebar(html) {
  const match = html.match(/sidebar-content="([^"]*)"/s);
  if (!match) throw new Error("Could not find sidebar-content JSON");
  return JSON.parse(decodeHtml(match[1]));
}

function flattenSidebar(nodes, depth = 0, parent = null, rows = []) {
  for (const node of nodes) {
    const href = node?.link?.href || node?.name;
    if (href) {
      rows.push({
        label: node.label,
        path: href,
        url: new URL(href, ORIGIN).href,
        depth,
        parent,
      });
    }
    if (Array.isArray(node.children) && node.children.length) {
      flattenSidebar(node.children, depth + 1, node.label, rows);
    }
  }
  return rows;
}

function dedupePages(pages) {
  const seen = new Set();
  const out = [];
  for (const page of pages) {
    const key = new URL(page.url).pathname;
    if (seen.has(key)) continue;
    seen.add(key);
    out.push(page);
  }
  return out;
}

function extractContentHtml(html) {
  const layoutStart = html.indexOf("<doc-content-layout");
  const h1Start = html.indexOf("<h1", layoutStart);
  const contentEnd = html.indexOf("</doc-content-layout>", h1Start);
  if (h1Start === -1 || contentEnd === -1) {
    throw new Error("Could not isolate doc-content-layout body");
  }
  return html.slice(h1Start, contentEnd);
}

function extractTitle(contentHtml, fallback) {
  const match = contentHtml.match(/<h1[^>]*>([\s\S]*?)<\/h1>/i);
  return match ? textFromHtml(match[1]).replace(/^#\s*/, "").trim() : fallback;
}

function extractHeadings(contentHtml) {
  const headings = [];
  const re =
    /<h([1-6])[^>]*>([\s\S]*?)<\/h[1-6]>|<doc-heading[^>]*header="([^"]+)"[^>]*aria-level="([^"]+)"[^>]*><\/doc-heading>/gi;
  let match;
  while ((match = re.exec(contentHtml))) {
    if (match[2]) {
      headings.push({ level: Number(match[1]), text: textFromHtml(match[2]) });
    } else {
      headings.push({ level: Number(match[4] || 2), text: decodeHtml(match[3]).trim() });
    }
  }
  return headings.filter((h) => h.text);
}

function extractLinks(contentHtml, sourceUrl) {
  const links = [];
  const re = /<a\b[^>]*href="([^"]+)"[^>]*>([\s\S]*?)<\/a>/gi;
  let match;
  while ((match = re.exec(contentHtml))) {
    const href = decodeHtml(match[1]);
    if (!href || href.startsWith("#") || href.startsWith("mailto:")) continue;
    links.push({
      label: textFromHtml(match[2]).replace(/\s+/g, " ").trim(),
      url: new URL(href, sourceUrl).href,
    });
  }
  return links;
}

function compactSummary(markdown, headings, title) {
  const lines = markdown
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean);
  const titleLine = title.toLowerCase();
  const lead =
    lines.find(
      (line) =>
        !line.startsWith("#") &&
        !line.startsWith("- ") &&
        !line.startsWith(">") &&
        line.toLowerCase() !== titleLine
    ) || "";
  const bullets = lines
    .filter((line) => line.startsWith("- "))
    .map((line) => line.replace(/^-\s+/, ""))
    .slice(0, 8);
  const topics = headings
    .filter((h) => h.level > 1)
    .map((h) => h.text)
    .slice(0, 10);
  return {
    lead: lead.slice(0, 500),
    topics,
    bullets,
  };
}

function slugFor(url) {
  const name = path.basename(new URL(url).pathname).replace(/\.html?$/, "");
  return name.replace(/[^a-zA-Z0-9_.-]+/g, "_");
}

function mdEscape(value) {
  return String(value).replace(/\|/g, "\\|").replace(/\n/g, " ");
}

async function fetchText(url) {
  const response = await fetch(url, {
    headers: {
      "user-agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/122 Safari/537.36",
    },
  });
  if (!response.ok) throw new Error(`HTTP ${response.status} for ${url}`);
  return response.text();
}

async function main() {
  const seed = argValue("--seed", DEFAULT_SEED);
  const outdir = path.resolve(argValue("--outdir", DEFAULT_OUTDIR));
  const seedHtml = await fetchText(seed);
  const pages = dedupePages(flattenSidebar(extractSidebar(seedHtml)));
  const manifest = [];

  await mkdir(path.join(outdir, "raw"), { recursive: true });
  await mkdir(path.join(outdir, "summaries"), { recursive: true });

  for (const [index, page] of pages.entries()) {
    process.stderr.write(`Indexing ${index + 1}/${pages.length}: ${page.url}\n`);
    const html = page.url === seed ? seedHtml : await fetchText(page.url);
    const contentHtml = extractContentHtml(html);
    const title = extractTitle(contentHtml, page.label);
    const headings = extractHeadings(contentHtml);
    const links = extractLinks(contentHtml, page.url);
    const markdown = textFromHtml(contentHtml);
    const summary = compactSummary(markdown, headings, title);
    const fileBase = slugFor(page.url);
    const rawPath = path.join(outdir, "raw", `${fileBase}.md`);
    const summaryPath = path.join(outdir, "summaries", `${fileBase}.json`);
    const frontmatter = [
      "---",
      `title: ${JSON.stringify(title)}`,
      `source: ${JSON.stringify(page.url)}`,
      `guidePath: ${JSON.stringify(new URL(page.url).pathname)}`,
      `navLabel: ${JSON.stringify(page.label)}`,
      `depth: ${page.depth}`,
      `parent: ${JSON.stringify(page.parent)}`,
      `extractedAt: ${JSON.stringify(new Date().toISOString())}`,
      "---",
      "",
    ].join("\n");
    await writeFile(rawPath, frontmatter + markdown + "\n", "utf8");
    const summaryPayload = {
      title,
      source: page.url,
      guidePath: new URL(page.url).pathname,
      navLabel: page.label,
      depth: page.depth,
      parent: page.parent,
      rawPath: path.relative(process.cwd(), rawPath),
      markdownChars: markdown.length,
      headings,
      links,
      summary,
    };
    await writeFile(summaryPath, JSON.stringify(summaryPayload, null, 2) + "\n", "utf8");
    manifest.push(summaryPayload);
  }

  await writeFile(path.join(outdir, "manifest.json"), JSON.stringify(manifest, null, 2) + "\n", "utf8");

  const indexMd = [
    "# Data 360 Developer Guide Index",
    "",
    `Seed: ${seed}`,
    `Pages: ${manifest.length}`,
    "",
    "| Title | Guide Path | What It Covers | Key Topics | Source |",
    "| --- | --- | --- | --- | --- |",
    ...manifest.map((item) =>
      `| ${[
        mdEscape(item.title),
        `\`${item.guidePath}\``,
        mdEscape(item.summary.lead),
        mdEscape(item.summary.topics.join(", ")),
        item.source,
      ].join(" | ")} |`
    ),
    "",
  ].join("\n");
  await writeFile(path.join(outdir, "index.md"), indexMd, "utf8");

  const topicCounts = new Map();
  for (const item of manifest) {
    for (const heading of item.headings) {
      const key = heading.text;
      topicCounts.set(key, (topicCounts.get(key) || 0) + 1);
    }
  }
  const learningMap = [
    "# Data 360 Developer Guide Learning Map",
    "",
    "This is a local synthesis index for Data360 Beast skill updates. It is derived from official Salesforce Developer docs and should be refreshed before publishing durable guidance.",
    "",
    "## Crawl Scope",
    "",
    `- Source: ${seed}`,
    `- Pages indexed: ${manifest.length}`,
    "- Source type: developer.salesforce.com guide pages",
    "- Public repo rule: summarize learnings; do not publish raw extracted pages.",
    "",
    "## Skill Update Candidates",
    "",
    "- `sf-datacloud`: strengthen the end-to-end development lifecycle routing: architecture, object model, API category, environments, lifecycle, packages/data kits, cost, and optimization.",
    "- `sf-datacloud-connectapi`: split API guidance by integration, custom app development, Postman exploration, API end-of-life, and direct developer resources.",
    "- `sf-datacloud-metadata-agentic` and `sf-datacloud-connectapi`: add metadata component cheat-sheet awareness for Data 360 promotion and packaging.",
    "- `sf-deploy` adjacent guidance: Data 360 development uses sandbox/second-org/partner-org patterns plus data kits and 2GP, not a direct copy of standard Platform scratch-org assumptions.",
    "- `sf-datacloud-governance` and `sf-flex-estimator`: incorporate Cost and Usage plus Best Practices for Optimizing Usage as first-class validation gates.",
    "",
    "## Page Map",
    "",
    ...manifest.map((item) => `- ${item.title}: ${item.summary.lead || item.summary.topics.join("; ")}`),
    "",
    "## Frequent Headings",
    "",
    ...[...topicCounts.entries()]
      .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
      .slice(0, 30)
      .map(([heading, count]) => `- ${heading}: ${count}`),
    "",
  ].join("\n");
  await writeFile(path.join(outdir, "learning-map.md"), learningMap, "utf8");

  process.stdout.write(`Indexed ${manifest.length} developer guide pages into ${outdir}\n`);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
