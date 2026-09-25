#!/usr/bin/env node
import { writeFile, mkdir } from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";

const DEFAULT_SEED =
  "https://help.salesforce.com/s/articleView?id=data.c360_a_product_considerations.htm&language=en_US&type=5";
const FALLBACK_DISCOVERY_ARTICLE_IDS = [
  "data.c360_a_activations_publish_history.htm",
  "data.c360_a_bring_your_own_model.htm",
  "data.c360_a_considerations_and_guidelines.htm",
  "data.c360_a_considerations_for_related_attributes.htm",
  "data.c360_a_data_cloud_sandbox.htm",
  "data.c360_a_data_explorer.htm",
  "data.c360_a_data_governance.htm",
  "data.c360_a_dc_ai_finserv.htm",
  "data.c360_a_identity_resolution_match_type_compare.htm",
  "data.c360_a_limits_and_guidelines_dev_ed.htm",
  "data.c360_a_omni_audience.htm",
  "data.c360_a_profile_explorer.htm",
  "data.c360_a_query_data_in_dc.htm",
  "data.c360_a_query_secondary_indexes.htm",
  "data.c360_a_segment_types_statuses.htm",
  "analytics.c360_a_sl_get_started.htm",
  "data.c360_a_billing_considerations_for_data_ingestion.htm",
  "data.c360_a_billing_considerations_for_data_transforms.htm",
  "data.c360_a_billing_considerations_for_identity_resolution.htm",
  "data.c360_a_ai_foundation_models_configured_monitor.htm",
];
const RELATED_ARTICLE_IDS = [
  "sf.c360_a_search_index_ground_ai.htm",
  "ai.generative_ai_session_trace.htm",
  "mktg.persnl_agentforce_configure_get_context_action.htm",
  "sf.c360_a_glossary_guide.htm",
];
const REQUIRED_EVIDENCE_IDS = [
  "data.c360_a_data_spaces.htm",
  "data.c360_a_using_data_cloud_apis_with_data_spaces.htm",
  "data.c360_a_userpermissions.htm",
  "data.c360_a_hybridsearch_index_create.htm",
  "data.c360_a_ai_retriever_create.htm",
  "data.c360_a_limits_and_guidelines.htm",
  "data.c360_a_changelog_usage_and_access.htm",
  "data.c360_a_data_cloud_architecture_strategy.htm",
  "data.c360_a_data_gov_capabilities.htm",
  "data.c360_a_data_cloud_sandbox_create.htm",
  "data.c360_a_data_cloud_one_sandboxes.htm",
  "data.c360_a_companion_connections.htm",
];
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
const { HelpSfExtractor } = await import(pathToFileURL(path.join(MCP_ROOT, "dist/extractors/help-sf.js")).href);
const helpExtractor = new HelpSfExtractor();

function argValue(name, fallback) {
  const idx = process.argv.indexOf(name);
  if (idx === -1 || idx + 1 >= process.argv.length) return fallback;
  return process.argv[idx + 1];
}

function hasFlag(name) {
  return process.argv.includes(name);
}

function normalizeHelpUrl(url) {
  try {
    const parsed = new URL(url, "https://help.salesforce.com");
    if (parsed.hostname !== "help.salesforce.com") return null;
    const id = parsed.searchParams.get("id");
    if (!id || !(/^(?:data|analytics|sf)\.c360|^data\.cdp/.test(id) || RELATED_ARTICLE_IDS.includes(id))) return null;
    return `https://help.salesforce.com/s/articleView?id=${id}&language=en_US&type=5`;
  } catch {
    return null;
  }
}

function extractHelpLinks(markdown) {
  const links = new Set();
  const re = /\]\((https:\/\/help\.salesforce\.com\/(?:apex\/HTViewHelpDoc|s\/articleView)\?[^)]+)\)/g;
  let match;
  while ((match = re.exec(markdown))) {
    const normalized = normalizeHelpUrl(match[1]);
    if (normalized) links.add(normalized);
  }
  return [...links];
}

function articleId(url) {
  return new URL(url).searchParams.get("id") ?? "unknown";
}

function slug(url) {
  return articleId(url).replace(/[^a-zA-Z0-9_.-]+/g, "_").replace(/\.htm$/, "");
}

function compactSummary(markdown) {
  const lines = markdown
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean)
    .filter((line) => !line.startsWith("!["))
    .filter((line) => !/^You are here:?$/i.test(line))
    .filter((line) => !/^\d+\.\s+\[/.test(line));
  const bullets = lines.filter((line) => line.startsWith("- ")).slice(0, 10);
  const headings = lines.filter((line) => line.startsWith("## ")).slice(0, 12);
  const lead = lines.find((line) => !line.startsWith("#") && !line.startsWith("- ")) ?? "";
  return {
    lead,
    headings: headings.map((line) => line.replace(/^##\s+/, "")),
    bullets: bullets.map((line) => line.replace(/^-\s+/, "")),
  };
}

function isAcceptableResult(result) {
  const title = String(result.title ?? "").trim();
  const markdown = String(result.markdown ?? "").trim();
  const oversizedPlaceholder = /Cannot populate due to large Document size/i.test(markdown);
  const rejectedBody =
    /We looked high and low but couldn't find that page|Sorry to interrupt|CSS Error/i;
  return (
    title &&
    !/^untitled$/i.test(title) &&
    (markdown.length >= 500 || oversizedPlaceholder) &&
    !rejectedBody.test(markdown)
  );
}

async function main() {
  const outdir = path.resolve(argValue("--outdir", "docs/data360/help"));
  const maxPages = Number(argValue("--max-pages", "0"));
  const maxDepth = Number(argValue("--depth", "2"));
  const seed = argValue("--seed", DEFAULT_SEED);
  const refresh = hasFlag("--refresh");
  const fallbackDiscoverySeeds = [...FALLBACK_DISCOVERY_ARTICLE_IDS, ...REQUIRED_EVIDENCE_IDS].map((id) => ({
    url: `https://help.salesforce.com/s/articleView?id=${id}&language=en_US&type=5`,
    depth: maxDepth,
    parent: "oversized-help-fallback",
  }));
  const queue = [
    { url: normalizeHelpUrl(seed) ?? seed, depth: 0, parent: null },
    ...RELATED_ARTICLE_IDS.map((id) => ({
      url: `https://help.salesforce.com/s/articleView?id=${id}&language=en_US&type=5`,
      depth: 0,
      parent: "reviewed-related-topic",
    })),
    ...fallbackDiscoverySeeds,
  ];
  const seen = new Set();
  const manifest = [];

  await mkdir(path.join(outdir, "raw"), { recursive: true });
  await mkdir(path.join(outdir, "summaries"), { recursive: true });

  while (queue.length && (maxPages <= 0 || manifest.length < maxPages)) {
    const current = queue.shift();
    if (!current || seen.has(current.url)) continue;
    seen.add(current.url);
    process.stderr.write(`Scraping depth ${current.depth}: ${current.url}\n`);
    const result = refresh ? await helpExtractor.extract(current.url) : await scrape(current.url);
    const id = articleId(result.url);
    const fileBase = slug(result.url);
    const rawPath = path.join(outdir, "raw", `${fileBase}.md`);
    const links = extractHelpLinks(result.markdown);
    const summary = compactSummary(result.markdown);
    if (!isAcceptableResult(result)) {
      process.stderr.write(
        `Rejected Help shell or suspicious capture: ${id} (${result.title}, ${result.markdown.length} chars)\n`,
      );
      if (current.depth < maxDepth) {
        for (const link of links) {
          if (!seen.has(link)) queue.push({ url: link, depth: current.depth + 1, parent: id });
        }
      }
      continue;
    }
    const frontmatter = [
      "---",
      `title: ${JSON.stringify(result.title)}`,
      `source: ${JSON.stringify(result.url)}`,
      `articleId: ${JSON.stringify(id)}`,
      `cached: ${result.cached}`,
      `extractedAt: ${JSON.stringify(result.extractedAt)}`,
      "---",
      "",
    ].join("\n");
    if (refresh || !result.cached) {
      await writeFile(rawPath, frontmatter + result.markdown + "\n", "utf8");
    } else {
      await writeFile(rawPath, frontmatter + result.markdown + "\n", "utf8");
    }
    await writeFile(path.join(outdir, "summaries", `${fileBase}.json`),
      JSON.stringify({ articleId: id, title: result.title, source: result.url, summary }, null, 2) + "\n", "utf8");
    manifest.push({
      title: result.title,
      source: result.url,
      articleId: id,
      depth: current.depth,
      parent: current.parent,
      rawPath,
      markdownChars: result.markdown.length,
      links: links.length,
      summary,
    });
    if (current.depth < maxDepth) {
      for (const link of links) {
        if (!seen.has(link)) queue.push({ url: link, depth: current.depth + 1, parent: id });
      }
    }
  }

  await writeFile(
    path.join(outdir, "manifest.json"),
    JSON.stringify(manifest, null, 2) + "\n",
    "utf8",
  );
  const index = [
    "# Data 360 Help Index",
    "",
    `Indexed articles: ${manifest.length}`,
    "",
    "This public index lists the official Salesforce Help pages analyzed for",
    "Data360 Beast. Raw extracted article bodies and generated local summaries are",
    "not published.",
    "",
    "Limit-source rule: use current Data 360 Limits and Guidelines first. When that",
    "page points to Data Services Billable Usage Types for Data 360, follow that",
    "source and treat the value as license, entitlement, usage, or contract",
    "sensitive. Use Customer Data Platform limits only for explicit legacy CDP scope",
    "or a clearly labeled comparison.",
    "",
    `Discovery seed: ${seed}`,
    `Discovery depth: ${maxDepth}`,
    "",
    "| Title | Article ID | Depth | Chars | Source |",
    "| --- | --- | --- | --- | --- |",
    ...manifest.map(
      (item) =>
        `| ${item.title.replaceAll("|", "\\|")} | ${item.articleId} | ${item.depth} | ${item.markdownChars} | ${item.source} |`,
    ),
    "",
  ].join("\n");
  await writeFile(path.join(outdir, "index.md"), index, "utf8");
  process.stdout.write(`Wrote ${manifest.length} help articles to ${outdir}\n`);
}

try {
  await main();
} finally {
  await closeBrowser();
}
