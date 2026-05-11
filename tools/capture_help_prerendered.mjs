#!/usr/bin/env node
import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const HELP_DIR = path.join(ROOT, "docs/data360/help");
const MCP_ROOT = "/Users/bertie/.codex/mcp-servers/sf-docs-mcp";
const requireFromMcp = createRequire(path.join(MCP_ROOT, "package.json"));
const TurndownService = requireFromMcp("turndown");
const { gfm } = requireFromMcp("turndown-plugin-gfm");

const GOOGLEBOT_UA = "Googlebot/2.1 (+http://www.google.com/bot.html)";
const PLACEHOLDER_RE = /Cannot populate due to large Document size/i;
const ARTICLE_ID_RE = /[?&]id=([^&]+)/;

function argValue(name, fallback) {
  const idx = process.argv.indexOf(name);
  if (idx === -1 || idx + 1 >= process.argv.length) return fallback;
  return process.argv[idx + 1];
}

function hasFlag(name) {
  return process.argv.includes(name);
}

function slug(articleId) {
  return articleId.replace(/[^A-Za-z0-9_.-]+/g, "_").replace(/\.htm$/, "");
}

function articleIdFromSource(source) {
  const match = String(source).match(ARTICLE_ID_RE);
  return match ? match[1] : null;
}

function helpUrl(articleId) {
  return `https://help.salesforce.com/s/articleView?id=${articleId}&language=en_US&type=5`;
}

function htmlDecode(value) {
  return String(value)
    .replace(/&quot;/g, '"')
    .replace(/&#x27;/g, "'")
    .replace(/&#39;/g, "'")
    .replace(/&#x26;/g, "&")
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&nbsp;/g, " ");
}

function extractTitle(html, articleId) {
  const match = html.match(/<title>([\s\S]*?)<\/title>/i);
  return match ? htmlDecode(match[1]).trim() : articleId;
}

function extractArticleHtml(html) {
  const marker = '<div class="slds-text-longform" id="content"';
  const start = html.indexOf(marker);
  if (start === -1) {
    throw new Error("Could not find Salesforce Help content container");
  }
  const endMarkers = [
    "<c-hc-article-feedback",
    '<div class="ul-container"',
    '<h2 id="ot-pc-title"',
  ];
  const end = endMarkers
    .map((markerText) => html.indexOf(markerText, start))
    .filter((idx) => idx > start)
    .sort((a, b) => a - b)[0];
  const sliced = html.slice(start, end === undefined ? html.length : end);
  return sliced
    .replace(/<div class="slds-max-small-hide[\s\S]*?<\/ol>\s*<\/div>/i, "")
    .replace(/<button[\s\S]*?<\/button>/gi, "");
}

function createTurndown() {
  const td = new TurndownService({
    headingStyle: "atx",
    codeBlockStyle: "fenced",
    bulletListMarker: "-",
  });
  td.use(gfm);
  td.addRule("sfHelpLinks", {
    filter: (node) => node.nodeName === "A",
    replacement: (content, node) => {
      const href = node.getAttribute("href");
      if (!href) return content;
      const normalized = new URL(href, "https://help.salesforce.com").href;
      return `[${content.trim() || normalized}](${normalized})`;
    },
  });
  td.addRule("compactImages", {
    filter: "img",
    replacement: (_content, node) => {
      const alt = node.getAttribute("alt") || "";
      return alt ? `Image: ${alt}` : "";
    },
  });
  return td;
}

function compactSummary(markdown) {
  const lines = markdown
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean)
    .filter((line) => !line.startsWith("Image:"));
  const lead =
    lines.find(
      (line) =>
        !line.startsWith("#") &&
        !line.startsWith("- ") &&
        !line.startsWith("|") &&
        !line.startsWith("[")
    ) || "";
  const headings = lines
    .filter((line) => line.startsWith("## "))
    .map((line) => line.replace(/^##\s+/, ""))
    .slice(0, 50);
  const bullets = lines
    .filter((line) => line.startsWith("- "))
    .map((line) => line.replace(/^-\s+/, ""))
    .slice(0, 30);
  return { lead, headings, bullets };
}

function extractLinks(markdown) {
  const links = new Set();
  for (const match of markdown.matchAll(/\]\((https:\/\/help\.salesforce\.com\/[^)]+)\)/g)) {
    links.add(match[1]);
  }
  return [...links].sort();
}

async function readJsonIfExists(filePath, fallback) {
  try {
    return JSON.parse(await readFile(filePath, "utf8"));
  } catch {
    return fallback;
  }
}

async function writeManifestEntry(payload) {
  const manifestPath = path.join(HELP_DIR, "cache-manifest.json");
  const manifest = await readJsonIfExists(manifestPath, []);
  const idx = manifest.findIndex((item) => item.articleId === payload.articleId);
  if (idx === -1) {
    manifest.push(payload);
  } else {
    manifest[idx] = payload;
  }
  manifest.sort((a, b) => String(a.title).localeCompare(String(b.title)));
  await writeFile(manifestPath, JSON.stringify(manifest, null, 2) + "\n", "utf8");

  const indexLines = [
    "# Data 360 Help Cache Export",
    "",
    `Exported articles: ${manifest.length}`,
    "",
    "| Title | Article ID | Chars | Source |",
    "| --- | --- | --- | --- |",
    ...manifest.map((item) =>
      `| ${String(item.title).replaceAll("|", "\\|")} | ${item.articleId} | ${item.markdownChars} | ${item.source} |`
    ),
    "",
  ];
  await writeFile(path.join(HELP_DIR, "cache-index.md"), indexLines.join("\n"), "utf8");
}

async function articleIdsFromPlaceholders() {
  const manifestPath = path.join(HELP_DIR, "cache-manifest.json");
  const manifest = await readJsonIfExists(manifestPath, []);
  const ids = [];
  for (const item of manifest) {
    const articleId = item.articleId || articleIdFromSource(item.source);
    if (!articleId) continue;
    const rawPath = path.join(ROOT, item.rawPath || `docs/data360/help/raw/${slug(articleId)}.md`);
    try {
      const raw = await readFile(rawPath, "utf8");
      if (PLACEHOLDER_RE.test(raw)) ids.push(articleId);
    } catch {
      ids.push(articleId);
    }
  }
  return [...new Set(ids)];
}

async function captureArticle(articleId) {
  const source = helpUrl(articleId);
  const response = await fetch(source, {
    headers: {
      "user-agent": GOOGLEBOT_UA,
      accept: "text/html,application/xhtml+xml",
    },
  });
  if (!response.ok) {
    throw new Error(`HTTP ${response.status} for ${source}`);
  }
  const html = await response.text();
  const title = extractTitle(html, articleId);
  const articleHtml = extractArticleHtml(html);
  const markdown = createTurndown().turndown(articleHtml).trim();
  if (markdown.length < 1000 || PLACEHOLDER_RE.test(markdown)) {
    throw new Error(`Prerendered capture did not produce full article for ${articleId}`);
  }

  const name = slug(articleId);
  const rawPath = path.join(HELP_DIR, "raw", `${name}.md`);
  const summaryPath = path.join(HELP_DIR, "summaries", `${name}.json`);
  const extractedAt = new Date().toISOString();
  const frontmatter = [
    "---",
    `title: ${JSON.stringify(title)}`,
    `source: ${JSON.stringify(source)}`,
    `articleId: ${JSON.stringify(articleId)}`,
    'pageType: "help-article"',
    'extractionMethod: "official-help-prerendered-html"',
    `extractedAt: ${JSON.stringify(extractedAt)}`,
    "---",
    "",
  ].join("\n");
  await writeFile(rawPath, frontmatter + markdown + "\n", "utf8");

  const summaryPayload = {
    title,
    source,
    articleId,
    rawPath: path.relative(ROOT, rawPath),
    markdownChars: markdown.length,
    links: extractLinks(markdown),
    extractionMethod: "official-help-prerendered-html",
    summary: compactSummary(markdown),
  };
  await writeFile(summaryPath, JSON.stringify(summaryPayload, null, 2) + "\n", "utf8");
  await writeManifestEntry(summaryPayload);
  return summaryPayload;
}

async function main() {
  const fromPlaceholders = hasFlag("--placeholders");
  const argIds = argValue("--article-ids", "")
    .split(",")
    .map((id) => id.trim())
    .filter(Boolean);
  const ids = fromPlaceholders ? await articleIdsFromPlaceholders() : argIds;
  if (!ids.length) {
    console.log("No oversized Help placeholders found.");
    return;
  }

  await mkdir(path.join(HELP_DIR, "raw"), { recursive: true });
  await mkdir(path.join(HELP_DIR, "summaries"), { recursive: true });

  const captures = [];
  for (const articleId of ids) {
    process.stderr.write(`Capturing prerendered Help article: ${articleId}\n`);
    captures.push(await captureArticle(articleId));
  }
  await writeFile(
    path.join(HELP_DIR, "fallback-captures.json"),
    JSON.stringify({ capturedAt: new Date().toISOString(), captures }, null, 2) + "\n",
    "utf8"
  );
  console.log(`Captured ${captures.length} oversized Help articles via official prerendered HTML.`);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
