#!/usr/bin/env node
import { createHash } from "node:crypto";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";

const DEFAULT_CENTER = "https://developer.salesforce.com/developer-centers/data-cloud";
const DEFAULT_OUTDIR = "docs/data360/developer";
const ORIGIN = "https://developer.salesforce.com";
const DEFAULT_MCP_ROOT = path.join(
  process.env.HOME ?? ".",
  ".data360beast",
  "mcp-servers",
  "sf-docs-mcp",
);
const MCP_ROOT = process.env.SF_DOCS_MCP_ROOT ?? DEFAULT_MCP_ROOT;
const extractorUrl = pathToFileURL(path.join(MCP_ROOT, "dist/extractors/index.js")).href;
const browserUrl = pathToFileURL(path.join(MCP_ROOT, "dist/extractors/base.js")).href;
const { scrape } = await import(extractorUrl);
const { closeBrowser } = await import(browserUrl);

const GUIDE_SEEDS = [
  {
    family: "developer-guide",
    url: "https://developer.salesforce.com/docs/data/data-cloud-dev/guide/get-started.html",
    capture: "full",
  },
  {
    family: "code-extension",
    url: "https://developer.salesforce.com/docs/data/data-cloud-code-ext/guide/use-custom-code.html",
    capture: "full",
  },
  {
    family: "connect-rest-api",
    url: "https://developer.salesforce.com/docs/data/connectapi/overview",
    capture: "full",
  },
  {
    family: "connect-rest-api-guide",
    url: "https://developer.salesforce.com/docs/data/connectapi/guide",
    capture: "full",
  },
  {
    family: "connect-rest-api-reference",
    url: "https://developer.salesforce.com/docs/data/connectapi/references",
    capture: "full",
  },
  {
    family: "dmo-mapping",
    url: "https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-model-data.html",
    capture: "selected",
  },
  {
    family: "integration",
    url: "https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-data-cloud-integrations.html",
    capture: "full",
  },
  {
    family: "query-guide",
    url: "https://developer.salesforce.com/docs/data/data-cloud-query-guide/guide/query-guide-get-started.html",
    capture: "full",
  },
  {
    family: "sql-reference",
    url: "https://developer.salesforce.com/docs/data/data-cloud-query-guide/references/dc-sql-reference/data-cloud-sql-context.html",
    capture: "full",
  },
];

const IMPORTANT_DMO_LABELS = new Set([
  "Account Contact DMO",
  "Account DMO",
  "Calculated Insight DMO",
  "Contact Point Address DMO",
  "Contact Point Consent DMO",
  "Contact Point Email DMO",
  "Contact Point Phone DMO",
  "Email Engagement DMO",
  "Individual DMO",
  "Loyalty Program Member DMO",
  "Party DMO",
  "Party Identification DMO",
  "Product DMO",
  "Sales Order DMO",
  "Sales Order Product DMO",
  "Unified Individual DMO",
]);

const CANONICAL_PATH_ALIASES = new Map([
  [
    "/docs/data/data-cloud-dev/guide/get-started.html",
    "/docs/data/data-cloud-dev/guide/dc-get-started.html",
  ],
]);

function argValue(name, fallback) {
  const idx = process.argv.indexOf(name);
  if (idx === -1 || idx + 1 >= process.argv.length) return fallback;
  return process.argv[idx + 1];
}

function sha256(value) {
  return createHash("sha256").update(String(value), "utf8").digest("hex");
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
      .replace(/<[^>]+>/g, ""),
  )
    .replace(/[ \t]+\n/g, "\n")
    .replace(/\n{3,}/g, "\n\n")
    .replace(/[ \t]{2,}/g, " ")
    .trim();
}

function extractAttr(tag, attr) {
  const match = tag.match(new RegExp(`${attr}="([^"]*)"`));
  return match ? decodeHtml(match[1]) : "";
}

function extractSidebar(html) {
  const match = html.match(/sidebar-content="([^"]*)"/s);
  return match ? JSON.parse(decodeHtml(match[1])) : [];
}

function flattenSidebar(nodes, family, depth = 0, parent = null, rows = []) {
  for (const node of nodes) {
    const href = node?.link?.href || node?.name;
    if (href) {
      rows.push({
        label: node.label || href,
        url: new URL(href, ORIGIN).href,
        depth,
        parent,
        guideFamily: family,
      });
    }
    if (Array.isArray(node.children) && node.children.length) {
      flattenSidebar(node.children, family, depth + 1, node.label || parent, rows);
    }
  }
  return rows;
}

function normalizeDeveloperUrl(value) {
  try {
    const url = new URL(value, ORIGIN);
    if (url.hostname !== "developer.salesforce.com") return null;
    url.hash = "";
    url.search = "";
    url.pathname = url.pathname.replace(/\/+$/, "") || "/";
    url.pathname = CANONICAL_PATH_ALIASES.get(url.pathname) || url.pathname;
    return url.href;
  } catch {
    return null;
  }
}

function developerCenterDocLinks(html) {
  const links = new Set();
  for (const match of html.matchAll(/href=["']([^"']+)["']/gi)) {
    const normalized = normalizeDeveloperUrl(decodeHtml(match[1]));
    if (normalized?.includes("/docs/data/")) links.add(normalized);
  }
  return [...links].sort();
}

function dedupePages(pages) {
  const byUrl = new Map();
  for (const page of pages) {
    const normalized = normalizeDeveloperUrl(page.url);
    if (!normalized) continue;
    const existing = byUrl.get(normalized);
    const candidate = { ...page, url: normalized };
    if (!existing || candidate.depth < existing.depth) byUrl.set(normalized, candidate);
  }
  return [...byUrl.values()].sort(
    (a, b) => a.guideFamily.localeCompare(b.guideFamily) || a.depth - b.depth || a.url.localeCompare(b.url),
  );
}

function extractContentHtml(html) {
  const layoutStart = html.indexOf("<doc-content-layout");
  const h1Start = html.indexOf("<h1", layoutStart);
  const contentEnd = html.indexOf("</doc-content-layout>", h1Start);
  if (h1Start !== -1 && contentEnd !== -1) return html.slice(h1Start, contentEnd);

  const overview = html.match(/<dx-group-text\s+header="([^"]+)"\s+body="([^"]*)"[\s\S]*?<\/dx-section>/i);
  if (overview) {
    const features = [...html.matchAll(/"title"\s*:\s*"([^"]+)"[\s\S]*?"description"\s*:\s*"([^"]+)"/g)]
      .map((match) => `<h2>${match[1]}</h2><p>${match[2]}</p>`)
      .join("\n");
    return `<h1>${overview[1]}</h1><p>${overview[2]}</p>${features}`;
  }

  const reference = html.match(/reference-config='([^']+)'/s);
  if (reference) {
    const config = JSON.parse(decodeHtml(reference[1]));
    const item = config.refList?.[0];
    return `<h1>${item?.title || "Data 360 Connect API Reference"}</h1><p>Official API reference.</p>`;
  }
  throw new Error("Could not isolate Salesforce Developer content");
}

function extractTitle(contentHtml, fallback) {
  const match = contentHtml.match(/<h1[^>]*>([\s\S]*?)<\/h1>/i);
  return match ? textFromHtml(match[1]).replace(/^#\s*/, "").trim() : fallback;
}

function extractHeadings(markdown) {
  return markdown
    .split(/\r?\n/)
    .filter((line) => /^#{1,6}\s+/.test(line))
    .map((line) => ({ level: line.match(/^#+/)?.[0].length || 2, text: line.replace(/^#{1,6}\s+/, "").trim() }))
    .filter((heading) => heading.text);
}

function compactSummary(markdown, title) {
  const lines = markdown.split(/\r?\n/).map((line) => line.trim()).filter(Boolean);
  const titleLine = title.toLowerCase();
  const lead = lines.find((line) => !line.startsWith("#") && !line.startsWith("- ") && !line.startsWith(">") && line.toLowerCase() !== titleLine) || "";
  return {
    lead: lead.slice(0, 500),
    topics: extractHeadings(markdown).filter((heading) => heading.level > 1).map((heading) => heading.text).slice(0, 16),
    bullets: lines.filter((line) => line.startsWith("- ")).map((line) => line.replace(/^-\s+/, "")).slice(0, 12),
  };
}

function deriveTopics(page, title, summary) {
  const text = [title, page.label, page.parent, summary.lead, ...summary.topics, ...summary.bullets].join(" ").toLowerCase();
  const rules = [
    ["authentication-and-permissions", /auth|oauth|permission|credential|access token|external client app/],
    ["connections-and-connectors", /connection|connector|source system/],
    ["data-streams-and-ingestion", /data stream|ingest|dlo|data lake object/],
    ["zero-copy-and-federation", /zero.?copy|federat|direct access|live query/],
    ["file-federation", /file federation|iceberg|unity catalog/],
    ["query-federation", /query federation|lakehouse federation/],
    ["acceleration-and-refresh", /accelerat|refresh|schedule/],
    ["data-shares-and-targets", /data share|data target|activation target/],
    ["dmo-modeling-and-mapping", /\bdmo\b|data model object|mapping|customer 360 data model/],
    ["identity-resolution", /identity resolution|unified individual|unified profile/],
    ["query-and-sql", /query|\bsql\b|\bsoql\b|jdbc|python connector/],
    ["code-extension", /code extension|custom script|custom function|data custom code/],
    ["unstructured-and-search", /unstructured|search index|chunk|retriever|vector/],
    ["packaging-and-deployment", /data kit|package|deploy|migration|sandbox|production/],
    ["limits-and-considerations", /limit|consideration|guideline|unsupported|preview/],
    ["troubleshooting-and-readiness", /troubleshoot|prerequisite|readiness|monitor|status|error/],
    ["segmentation-and-activation", /segment|audience|activation|data action/],
    ["web-and-mobile-sdk", /web sdk|mobile sdk|interactions sdk|website sitemap/],
    ["governance-and-security", /govern|security|policy|firewall|allowlist|private connect/],
  ];
  return rules.filter(([, pattern]) => pattern.test(text)).map(([topic]) => topic);
}

function isIndexGuidance(item) {
  if (item.guideFamily !== "integration") return true;
  if (item.depth <= 2) return true;
  return /file federation|query federation|zero.?copy|data share|private connect|accelerat|ingestion api|web sdk|unstructured|databricks|snowflake|amazon s3|marketing cloud|salesforce crm/i.test(
    `${item.title} ${item.navLabel}`,
  );
}

function isAcceptableCapture(title, markdown) {
  if (!title || /^untitled$/i.test(title)) return false;
  if (/Sorry to interrupt|CSS Error|We looked high and low/i.test(markdown)) return false;
  if (/^(?:404(?: error)?|page not found)$/i.test(title.trim())) return false;
  return markdown.trim().length >= 120;
}

function shouldCapture(page, familyConfig) {
  if (familyConfig.capture === "full") return true;
  return page.depth <= 1 || IMPORTANT_DMO_LABELS.has(page.label);
}

function slugFor(url) {
  const parsed = new URL(url);
  const name = path.basename(parsed.pathname).replace(/\.html?$/, "") || "overview";
  return `${name.replace(/[^a-zA-Z0-9_.-]+/g, "_")}-${sha256(parsed.pathname).slice(0, 10)}`;
}

function mdEscape(value) {
  return String(value).replace(/\|/g, "\\|").replace(/\n/g, " ");
}

async function fetchText(url) {
  const response = await fetch(url, {
    headers: { "user-agent": "Mozilla/5.0 AppleWebKit/537.36 Chrome/122 Safari/537.36" },
  });
  if (!response.ok) throw new Error(`HTTP ${response.status} for ${url}`);
  return response.text();
}

async function staticCapture(page, html = null) {
  const sourceHtml = html ?? await fetchText(page.url);
  const contentHtml = extractContentHtml(sourceHtml);
  const title = extractTitle(contentHtml, page.label);
  const markdown = textFromHtml(contentHtml);
  return { title, markdown, extractionMethod: "official-developer-static-html" };
}

async function sfDocsCapture(page) {
  const result = await scrape(page.url);
  let title = String(result.title || page.label).trim();
  let markdown = String(result.markdown || "").trim();
  let extractionMethod = result.cached ? "sf-docs-cache" : "sf-docs-extractor";
  if (!isAcceptableCapture(title, markdown)) {
    const fallback = await staticCapture(page);
    title = fallback.title;
    markdown = fallback.markdown;
    extractionMethod = `${extractionMethod}+${fallback.extractionMethod}`;
  }
  if (!isAcceptableCapture(title, markdown)) throw new Error(`suspicious capture (${markdown.length} chars)`);
  return { title, markdown, extractionMethod };
}

async function mapConcurrent(items, concurrency, worker) {
  const results = new Array(items.length);
  let next = 0;
  async function runWorker() {
    while (true) {
      const index = next++;
      if (index >= items.length) return;
      results[index] = await worker(items[index], index);
    }
  }
  await Promise.all(Array.from({ length: Math.min(concurrency, items.length) }, runWorker));
  return results;
}

async function discover(center) {
  const centerHtml = await fetchText(center);
  const centerLinks = developerCenterDocLinks(centerHtml);
  const discovered = [];
  const familyReports = [];
  for (const config of GUIDE_SEEDS) {
    const html = await fetchText(config.url);
    const sidebar = extractSidebar(html);
    const pages = sidebar.length
      ? flattenSidebar(sidebar, config.family)
      : [{ label: extractAttr(html.match(/<meta\s+name="description"[^>]*>/i)?.[0] || "", "content") || config.family, url: config.url, depth: 0, parent: null, guideFamily: config.family }];
    if (!pages.some((page) => normalizeDeveloperUrl(page.url) === normalizeDeveloperUrl(config.url))) {
      pages.unshift({ label: config.family, url: config.url, depth: 0, parent: null, guideFamily: config.family });
    }
    discovered.push(...pages.map((page) => ({ ...page, capturePolicy: config.capture })));
    familyReports.push({ family: config.family, seed: config.url, capturePolicy: config.capture, catalogPages: dedupePages(pages).length });
  }
  return { pages: dedupePages(discovered), centerLinks, familyReports };
}

async function main() {
  const center = argValue("--center", DEFAULT_CENTER);
  const outdir = path.resolve(argValue("--outdir", DEFAULT_OUTDIR));
  const concurrency = Math.max(1, Number(argValue("--concurrency", "6")));
  const { pages, centerLinks, familyReports } = await discover(center);
  const configByFamily = new Map(GUIDE_SEEDS.map((item) => [item.family, item]));
  const failures = [];

  await mkdir(path.join(outdir, "raw"), { recursive: true });
  await mkdir(path.join(outdir, "summaries"), { recursive: true });

  const manifest = await mapConcurrent(pages, concurrency, async (page, index) => {
    const familyConfig = configByFamily.get(page.guideFamily);
    const capture = shouldCapture(page, familyConfig);
    if (index === 0 || (index + 1) % 100 === 0 || index + 1 === pages.length) {
      process.stderr.write(`Indexing ${index + 1}/${pages.length} [${page.guideFamily}] ${capture ? "capture" : "catalog"}\n`);
    }
    if (!capture) {
      const summary = { lead: `${page.label} in the official ${page.guideFamily} reference catalog.`, topics: [page.parent, page.guideFamily].filter(Boolean), bullets: [] };
      summary.topics = [...new Set([...summary.topics, ...deriveTopics(page, page.label, summary)])];
      return {
        title: page.label,
        source: page.url,
        guidePath: new URL(page.url).pathname,
        guideFamily: page.guideFamily,
        navLabel: page.label,
        depth: page.depth,
        parent: page.parent,
        extractionStatus: "cataloged",
        extractionMethod: "official-sidebar-catalog",
        markdownChars: 0,
        contentHash: sha256([page.url, page.label, page.parent, page.guideFamily].join("\n")),
        headings: [],
        links: [],
        summary,
      };
    }
    try {
      const extracted = await sfDocsCapture(page);
      const summary = compactSummary(extracted.markdown, extracted.title);
      summary.topics = [...new Set([...deriveTopics(page, extracted.title, summary), ...summary.topics])].slice(0, 24);
      const fileBase = slugFor(page.url);
      const rawPath = path.join(outdir, "raw", `${fileBase}.md`);
      const summaryPath = path.join(outdir, "summaries", `${fileBase}.json`);
      const payload = {
        title: extracted.title,
        source: page.url,
        guidePath: new URL(page.url).pathname,
        guideFamily: page.guideFamily,
        navLabel: page.label,
        depth: page.depth,
        parent: page.parent,
        extractionStatus: "captured",
        extractionMethod: extracted.extractionMethod,
        rawPath: path.relative(process.cwd(), rawPath),
        markdownChars: extracted.markdown.length,
        contentHash: sha256(extracted.markdown),
        headings: extractHeadings(extracted.markdown),
        links: [],
        summary,
      };
      const frontmatter = [
        "---",
        `title: ${JSON.stringify(payload.title)}`,
        `source: ${JSON.stringify(payload.source)}`,
        `guideFamily: ${JSON.stringify(payload.guideFamily)}`,
        `extractionMethod: ${JSON.stringify(payload.extractionMethod)}`,
        `extractedAt: ${JSON.stringify(new Date().toISOString())}`,
        "---",
        "",
      ].join("\n");
      await writeFile(rawPath, frontmatter + extracted.markdown + "\n", "utf8");
      await writeFile(summaryPath, JSON.stringify(payload, null, 2) + "\n", "utf8");
      return payload;
    } catch (error) {
      failures.push({ source: page.url, guideFamily: page.guideFamily, error: String(error) });
      return null;
    }
  });

  const accepted = manifest.filter(Boolean);
  const captured = accepted.filter((item) => item.extractionStatus === "captured");
  const cataloged = accepted.filter((item) => item.extractionStatus === "cataloged");
  const requiredFamilies = new Set(GUIDE_SEEDS.map((item) => item.family));
  const capturedFamilies = new Set(captured.map((item) => item.guideFamily));
  const missingFamilies = [...requiredFamilies].filter((family) => !capturedFamilies.has(family));
  if (failures.length || missingFamilies.length) {
    await writeFile(path.join(outdir, "crawl-report.json"), JSON.stringify({ center, centerLinks, familyReports, totalPages: pages.length, capturedPages: captured.length, catalogedPages: cataloged.length, failures, missingFamilies }, null, 2) + "\n", "utf8");
    throw new Error(`Developer crawl incomplete: ${failures.length} failures; missing captured families: ${missingFamilies.join(", ") || "none"}`);
  }

  await writeFile(path.join(outdir, "manifest.json"), JSON.stringify(accepted, null, 2) + "\n", "utf8");
  await writeFile(path.join(outdir, "crawl-report.json"), JSON.stringify({ center, centerLinks, familyReports, totalPages: accepted.length, capturedPages: captured.length, catalogedPages: cataloged.length, failures: [], missingFamilies: [] }, null, 2) + "\n", "utf8");

  const familyCounts = new Map();
  for (const item of accepted) {
    const current = familyCounts.get(item.guideFamily) || { total: 0, captured: 0, cataloged: 0 };
    current.total += 1;
    current[item.extractionStatus] += 1;
    familyCounts.set(item.guideFamily, current);
  }
  const implementationPages = captured.filter(
    (item) => isIndexGuidance(item) && (item.guideFamily !== "dmo-mapping" || item.depth <= 1 || IMPORTANT_DMO_LABELS.has(item.navLabel)),
  );
  const indexMd = [
    "# Data 360 Developer Documentation Index",
    "",
    `Developer Center: ${center}`,
    `Indexed pages: ${accepted.length}`,
    `Content captures through sf-docs: ${captured.length}`,
    `Reference catalog entries: ${cataloged.length}`,
    "",
    "This public index covers the Data 360 guide families routed from the official",
    "Salesforce Developer Center. Raw extracted bodies and generated summaries are",
    "not published. The complete page catalog is represented in the public knowledge graph.",
    "",
    "## Guide Families",
    "",
    "| Guide Family | Indexed | Content Captured | Cataloged | Seed |",
    "| --- | ---: | ---: | ---: | --- |",
    ...GUIDE_SEEDS.map((seed) => {
      const counts = familyCounts.get(seed.family) || { total: 0, captured: 0, cataloged: 0 };
      return `| ${seed.family} | ${counts.total} | ${counts.captured} | ${counts.cataloged} | ${seed.url} |`;
    }),
    "",
    "## Implementation Guidance Pages",
    "",
    "| Title | Family | What It Covers | Key Topics | Source |",
    "| --- | --- | --- | --- | --- |",
    ...implementationPages.map((item) => `| ${[mdEscape(item.title), item.guideFamily, mdEscape(item.summary.lead), mdEscape(item.summary.topics.join(", ")), item.source].join(" | ")} |`),
    "",
  ].join("\n");
  await writeFile(path.join(outdir, "index.md"), indexMd, "utf8");

  const topicCounts = new Map();
  for (const item of captured) {
    for (const topic of item.summary.topics) {
      if (/^[a-z]+(?:-[a-z]+)+$/.test(topic)) topicCounts.set(topic, (topicCounts.get(topic) || 0) + 1);
    }
  }
  const fingerprints = [...familyCounts].map(([family, counts]) => ({ family, ...counts, hash: sha256(accepted.filter((item) => item.guideFamily === family).map((item) => item.contentHash).sort().join("\n")) }));
  const learningMap = [
    "# Data 360 Developer Documentation Learning Map",
    "",
    "This public-safe synthesis is derived from official Salesforce Developer pages",
    "discovered from the Data 360 Developer Center and extracted through sf-docs.",
    "",
    "## Crawl Scope",
    "",
    `- Developer Center: ${center}`,
    `- Pages indexed: ${accepted.length}`,
    `- Content captures: ${captured.length}`,
    `- Reference-only catalog entries: ${cataloged.length}`,
    "- Raw source bodies and generated summaries remain local and ignored.",
    "",
    "## Source Fingerprints",
    "",
    "| Guide Family | Indexed | Captured | Cataloged | SHA-256 |",
    "| --- | ---: | ---: | ---: | --- |",
    ...fingerprints.map((item) => `| ${item.family} | ${item.total} | ${item.captured} | ${item.cataloged} | \`${item.hash}\` |`),
    "",
    "## Frequent Implementation Topics",
    "",
    ...[...topicCounts.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0])).slice(0, 80).map(([topic, count]) => `- ${topic}: ${count}`),
    "",
  ].join("\n");
  await writeFile(path.join(outdir, "learning-map.md"), learningMap, "utf8");
  process.stdout.write(`Indexed ${accepted.length} Developer pages across ${familyCounts.size} guide families (${captured.length} captured, ${cataloged.length} cataloged).\n`);
}

try {
  await main();
} finally {
  await closeBrowser();
}
