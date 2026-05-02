/**
 * DevOps Guide PDF Generator for Muhammad Arham
 * Uses pdfkit — run with: node generate_devops_guide.js
 */

const PDFDocument = require("pdfkit");
const fs = require("fs");
const path = require("path");

// ─── Colors ────────────────────────────────────────────────────────────────
const C = {
  BG_DARK:      "#0D1117",
  BLUE:         "#2196F3",
  BLUE_DARK:    "#1565C0",
  BLUE_LIGHT:   "#E3F2FD",
  GREEN:        "#4CAF50",
  GREEN_DARK:   "#2E7D32",
  GREEN_LIGHT:  "#E8F5E9",
  ORANGE:       "#FF9800",
  ORANGE_LIGHT: "#FFF3E0",
  RED:          "#F44336",
  RED_LIGHT:    "#FFEBEE",
  PURPLE:       "#9C27B0",
  PURPLE_LIGHT: "#F3E5F5",
  CYAN:         "#00BCD4",
  YELLOW:       "#FFC107",
  GRAY:         "#607D8B",
  GRAY_LIGHT:   "#ECEFF1",
  GRAY_DARK:    "#37474F",
  WHITE:        "#FFFFFF",
  BLACK:        "#212121",
  COMMENT:      "#546E7A",
  CODE_BG:      "#1E2A38",
  CODE_TEXT:    "#E0E0E0",
  CODE_GOOD_BG: "#1B3A2D",
  CODE_GOOD:    "#C8E6C9",
  CODE_BAD_BG:  "#3B1F1F",
  CODE_BAD:     "#FFCDD2",
};

const PAGE_W = 595.28; // A4
const PAGE_H = 841.89;
const MARGIN = 40;
const CONTENT_W = PAGE_W - MARGIN * 2;

// ─── PDF Setup ─────────────────────────────────────────────────────────────
const outputPath = path.join(__dirname, "DevOps_Guide.pdf");
const doc = new PDFDocument({
  size: "A4",
  margin: MARGIN,
  info: {
    Title:    "DevOps Learning Guide — Muhammad Arham",
    Author:   "Muhammad Arham",
    Subject:  "Git, Docker, Node.js DevOps Guide",
    Keywords: "git docker nodejs devops",
  },
});

const stream = fs.createWriteStream(outputPath);
doc.pipe(stream);

let currentY = MARGIN;

// ─── Helpers ───────────────────────────────────────────────────────────────
function pageNum() {
  return doc.bufferedPageRange().count + 1 -
    (doc.bufferedPageRange ? 0 : 0);
}

function newPage() {
  doc.addPage();
  currentY = MARGIN;
  addPageFooter();
}

function addPageFooter() {
  const savedY = doc.y;
  doc
    .fontSize(8)
    .fillColor(C.GRAY)
    .text("Muhammad Arham — DevOps Learning Guide",
      MARGIN, PAGE_H - 25, { align: "left", width: CONTENT_W / 2 })
    .text(`Page ${doc.bufferedPageRange().count}`,
      PAGE_W / 2, PAGE_H - 25, { align: "right", width: CONTENT_W / 2 });
  doc.y = savedY;
}

function filledRect(x, y, w, h, fillColor, radius = 0) {
  doc.roundedRect(x, y, w, h, radius).fill(fillColor);
}

function strokedRect(x, y, w, h, strokeColor, lineWidth = 1) {
  doc.rect(x, y, w, h).strokeColor(strokeColor).lineWidth(lineWidth).stroke();
}

function centeredText(text, x, y, width, opts = {}) {
  doc
    .fontSize(opts.size || 10)
    .font(opts.bold ? "Helvetica-Bold" : opts.italic ? "Helvetica-Oblique" : "Helvetica")
    .fillColor(opts.color || C.BLACK)
    .text(text, x, y, { align: "center", width, ...opts });
}

function sectionHeader(title) {
  if (doc.y > PAGE_H - 120) newPage();
  const y = doc.y;
  filledRect(MARGIN, y, CONTENT_W, 34, C.BLUE_DARK, 4);
  doc
    .fontSize(16)
    .font("Helvetica-Bold")
    .fillColor(C.WHITE)
    .text(title, MARGIN + 12, y + 10, { width: CONTENT_W - 20 });
  doc.moveDown(0.5);
}

function miniHeader(title, color = C.BLUE_DARK) {
  if (doc.y > PAGE_H - 80) newPage();
  const y = doc.y;
  filledRect(MARGIN, y, CONTENT_W, 26, color, 4);
  doc
    .fontSize(11)
    .font("Helvetica-Bold")
    .fillColor(C.WHITE)
    .text(title, MARGIN + 10, y + 8, { width: CONTENT_W - 20 });
  doc.moveDown(0.4);
}

function bodyText(text, opts = {}) {
  ensureSpace(20);
  doc
    .fontSize(opts.size || 10)
    .font(opts.bold ? "Helvetica-Bold" : opts.italic ? "Helvetica-Oblique" : "Helvetica")
    .fillColor(opts.color || C.BLACK)
    .text(text, MARGIN + (opts.indent || 0), doc.y,
      { width: CONTENT_W - (opts.indent || 0), align: opts.align || "justify", ...opts });
}

function calloutBox(text, type = "tip") {
  const config = {
    tip:     { bg: C.BLUE_LIGHT,   fg: "#1A237E", prefix: "💡 " },
    warning: { bg: C.ORANGE_LIGHT, fg: "#BF360C", prefix: "⚠️  " },
    success: { bg: C.GREEN_LIGHT,  fg: "#1B5E20", prefix: "✅ " },
    error:   { bg: C.RED_LIGHT,    fg: "#B71C1C", prefix: "❌ " },
  };
  const { bg, fg, prefix } = config[type] || config.tip;
  ensureSpace(40);
  const y = doc.y;
  const lines = Math.ceil(text.length / 80);
  const boxH = Math.max(30, lines * 14 + 14);
  filledRect(MARGIN, y, CONTENT_W, boxH, bg, 4);
  doc
    .fontSize(9.5)
    .font("Helvetica")
    .fillColor(fg)
    .text(prefix + text, MARGIN + 10, y + 8,
      { width: CONTENT_W - 20, align: "left" });
  doc.y = y + boxH + 6;
}

function codeBlock(lines, type = "normal") {
  const bg = type === "good" ? C.CODE_GOOD_BG :
             type === "bad"  ? C.CODE_BAD_BG  : C.CODE_BG;
  const fg = type === "good" ? C.CODE_GOOD :
             type === "bad"  ? C.CODE_BAD   : C.CODE_TEXT;
  const totalLines = Array.isArray(lines) ? lines : [lines];
  ensureSpace(totalLines.length * 14 + 16);
  const y = doc.y;
  const boxH = totalLines.length * 13 + 12;
  filledRect(MARGIN, y, CONTENT_W, boxH, bg, 4);
  doc.fontSize(8.5).font("Courier").fillColor(fg);
  totalLines.forEach((line, i) => {
    const lineColor = line.startsWith("#") ? "#78909C" : fg;
    doc.fillColor(lineColor)
       .text(line || " ", MARGIN + 10, y + 6 + i * 13,
         { width: CONTENT_W - 20, lineBreak: false });
  });
  doc.y = y + boxH + 4;
}

function hline(color = C.BLUE_LIGHT) {
  ensureSpace(10);
  doc
    .moveTo(MARGIN, doc.y)
    .lineTo(MARGIN + CONTENT_W, doc.y)
    .strokeColor(color)
    .lineWidth(1)
    .stroke();
  doc.moveDown(0.3);
}

function ensureSpace(needed) {
  if (doc.y + needed > PAGE_H - 50) newPage();
}

function h2(text) {
  ensureSpace(30);
  doc.moveDown(0.4);
  doc
    .fontSize(14)
    .font("Helvetica-Bold")
    .fillColor(C.BLUE_DARK)
    .text(text, MARGIN, doc.y);
  doc.moveDown(0.3);
}

function h3(text) {
  ensureSpace(20);
  doc
    .fontSize(11)
    .font("Helvetica-Bold")
    .fillColor(C.GRAY_DARK)
    .text(text, MARGIN, doc.y);
  doc.moveDown(0.2);
}

// ─── Table helper ──────────────────────────────────────────────────────────
function drawTable(headers, rows, colWidths, opts = {}) {
  const rowH    = opts.rowH    || 22;
  const headerH = opts.headerH || 24;
  const hdrBg   = opts.hdrBg   || C.BLUE_DARK;
  const altBg   = opts.altBg   || C.GRAY_LIGHT;
  const totalH  = headerH + rows.length * rowH + 4;

  ensureSpace(totalH);
  let x = MARGIN;
  let y = doc.y;

  // Header row
  filledRect(x, y, CONTENT_W, headerH, hdrBg, 3);
  colWidths.forEach((w, ci) => {
    doc
      .fontSize(9)
      .font("Helvetica-Bold")
      .fillColor(C.WHITE)
      .text(headers[ci], x + 5, y + 7,
        { width: w - 10, lineBreak: false });
    x += w;
  });

  // Data rows
  rows.forEach((row, ri) => {
    y += (ri === 0 ? headerH : rowH);
    const bg = ri % 2 === 0 ? C.WHITE : altBg;
    filledRect(MARGIN, y, CONTENT_W, rowH, bg);
    x = MARGIN;
    colWidths.forEach((w, ci) => {
      const cellOpts = opts.colFonts && opts.colFonts[ci] ? opts.colFonts[ci] : {};
      doc
        .fontSize(cellOpts.size || 8.5)
        .font(cellOpts.font || "Helvetica")
        .fillColor(cellOpts.color || C.BLACK)
        .text(String(row[ci] || ""), x + 5, y + 5,
          { width: w - 10, lineBreak: false });
      x += w;
    });
  });

  // Border
  doc.rect(MARGIN, doc.y, CONTENT_W, headerH + rows.length * rowH)
     .strokeColor("#CFD8DC").lineWidth(0.5).stroke();

  doc.y = y + rowH + 6;
}

// ─── Side-by-Side Code Comparison ─────────────────────────────────────────
function sideBySideCode(leftTitle, leftLines, rightTitle, rightLines) {
  const halfW = CONTENT_W / 2 - 3;
  const maxLines = Math.max(leftLines.length, rightLines.length);
  const blockH = maxLines * 13 + 28;
  ensureSpace(blockH + 10);
  const y = doc.y;

  // Left header
  filledRect(MARGIN, y, halfW, 20, C.RED_LIGHT, 3);
  doc.fontSize(9).font("Helvetica-Bold").fillColor("#B71C1C")
     .text(leftTitle, MARGIN + 5, y + 5, { width: halfW - 10, lineBreak: false });

  // Right header
  const rx = MARGIN + halfW + 6;
  filledRect(rx, y, halfW, 20, C.GREEN_LIGHT, 3);
  doc.fontSize(9).font("Helvetica-Bold").fillColor(C.GREEN_DARK)
     .text(rightTitle, rx + 5, y + 5, { width: halfW - 10, lineBreak: false });

  // Left code block
  filledRect(MARGIN, y + 20, halfW, blockH - 20, C.CODE_BAD_BG, 3);
  leftLines.forEach((line, i) => {
    doc.fontSize(8).font("Courier").fillColor(C.CODE_BAD)
       .text(line || " ", MARGIN + 6, y + 24 + i * 13,
         { width: halfW - 12, lineBreak: false });
  });

  // Right code block
  filledRect(rx, y + 20, halfW, blockH - 20, C.CODE_GOOD_BG, 3);
  rightLines.forEach((line, i) => {
    doc.fontSize(8).font("Courier").fillColor(C.CODE_GOOD)
       .text(line || " ", rx + 6, y + 24 + i * 13,
         { width: halfW - 12, lineBreak: false });
  });

  doc.y = y + blockH + 8;
}

// ─── Cover Page ────────────────────────────────────────────────────────────
function buildCover() {
  console.log("Building cover page...");

  // Dark background banner
  filledRect(MARGIN, MARGIN, CONTENT_W, 200, C.BG_DARK, 8);

  // Decorative circles
  doc.circle(MARGIN + 30, MARGIN + 30, 50).fill("#0D47A1");
  doc.circle(MARGIN + CONTENT_W - 20, MARGIN + 180, 60).fill("#1B5E20");
  doc.circle(MARGIN + CONTENT_W / 2, MARGIN + 100, 110).fill("#0D3666");

  // Title
  doc.fontSize(28).font("Helvetica-Bold").fillColor(C.WHITE)
     .text("DevOps Learning Guide", MARGIN, MARGIN + 70,
       { align: "center", width: CONTENT_W });

  doc.fontSize(13).font("Helvetica").fillColor("#90CAF9")
     .text("Muhammad Arham's Personal Handbook", MARGIN, MARGIN + 110,
       { align: "center", width: CONTENT_W });

  doc.fontSize(10).font("Helvetica").fillColor("#64B5F6")
     .text("Git  |  Docker  |  Node.js  |  GitHub Flow", MARGIN, MARGIN + 135,
       { align: "center", width: CONTENT_W });

  doc.fontSize(9).font("Helvetica-Oblique").fillColor("#B0BEC5")
     .text("From Zero to Deploying with Confidence", MARGIN, MARGIN + 158,
       { align: "center", width: CONTENT_W });

  doc.y = MARGIN + 215;

  // Workflow pills
  const pills = [
    { label: "GitHub",  color: C.GRAY_DARK },
    { label: "VS Code", color: C.BLUE_DARK },
    { label: "Docker",  color: C.GREEN_DARK },
    { label: "Ship! 🚀", color: C.ORANGE },
  ];
  const pillW = 100, pillH = 30, gap = 18;
  const totalPillW = pills.length * pillW + (pills.length - 1) * (gap + 10);
  let px = MARGIN + (CONTENT_W - totalPillW) / 2;
  const py = doc.y;

  pills.forEach((pill, i) => {
    filledRect(px, py, pillW, pillH, pill.color, 6);
    doc.fontSize(10).font("Helvetica-Bold").fillColor(C.WHITE)
       .text(pill.label, px, py + 9, { align: "center", width: pillW, lineBreak: false });
    if (i < pills.length - 1) {
      doc.fontSize(14).font("Helvetica-Bold").fillColor(C.YELLOW)
         .text("→", px + pillW + 4, py + 8, { lineBreak: false });
    }
    px += pillW + gap + 10;
  });

  doc.y = py + pillH + 14;

  doc.fontSize(9).font("Helvetica").fillColor(C.GRAY)
     .text("Based on your actual project: demo_nodejs_webpage  |  Node.js + Express + Docker  |  Generated 2026-04-26",
       MARGIN, doc.y, { align: "center", width: CONTENT_W });

  doc.moveDown(1.5);
}

// ─── Table of Contents ─────────────────────────────────────────────────────
function buildTOC() {
  console.log("Building table of contents...");
  newPage();
  sectionHeader("Table of Contents");
  doc.moveDown(0.5);

  const entries = [
    ["1", "The Big Picture — Your Workflow",         "3"],
    ["2", "Git Fundamentals & Daily Commands",       "5"],
    ["3", "Branching Strategies",                    "9"],
    ["4", "Docker: Images vs Containers",            "12"],
    ["5", "Your Dockerfile — Line by Line",          "15"],
    ["6", "Common Errors & Fixes",                   "18"],
    ["7", "Cheat Sheets",                            "22"],
  ];

  entries.forEach(([num, title, pg]) => {
    const y = doc.y;
    filledRect(MARGIN, y, 26, 22, C.BLUE_DARK, 3);
    doc.fontSize(10).font("Helvetica-Bold").fillColor(C.WHITE)
       .text(num, MARGIN, y + 6, { align: "center", width: 26, lineBreak: false });
    filledRect(MARGIN + 26, y, CONTENT_W - 52, 22, C.GRAY_LIGHT, 0);
    doc.fontSize(10).font("Helvetica").fillColor(C.BLACK)
       .text(title, MARGIN + 32, y + 6, { width: CONTENT_W - 70, lineBreak: false });
    filledRect(MARGIN + CONTENT_W - 26, y, 26, 22, C.BLUE_LIGHT, 3);
    doc.fontSize(10).font("Helvetica-Bold").fillColor(C.BLUE_DARK)
       .text(pg, MARGIN + CONTENT_W - 26, y + 6,
         { align: "center", width: 26, lineBreak: false });
    doc.rect(MARGIN, y, CONTENT_W, 22).strokeColor("#CFD8DC").lineWidth(0.5).stroke();
    doc.y = y + 26;
  });
}

// ─── Section 1: Big Picture ────────────────────────────────────────────────
function buildBigPicture() {
  console.log("Building Section 1: Big Picture...");
  newPage();
  sectionHeader("Section 1 — The Big Picture: Your Workflow");

  bodyText(
    "Before diving into commands, understand WHY each tool exists and how they connect. " +
    "Here is your complete daily workflow as a DevOps learner:"
  );
  doc.moveDown(0.6);

  // Workflow diagram
  h2("Your Daily Workflow");
  const boxes = [
    { label: "Your\nBrain",   color: "#9C27B0", sub: "Idea" },
    { label: "VS Code",       color: C.BLUE_DARK, sub: "Write code" },
    { label: "Git",           color: C.GRAY_DARK, sub: "Track changes" },
    { label: "GitHub",        color: "#24292E",   sub: "Share / backup" },
    { label: "Docker",        color: C.GREEN_DARK, sub: "Run app" },
  ];
  const bw = 90, bh = 52, bgap = 12;
  const totalW = boxes.length * bw + (boxes.length - 1) * (bgap + 14);
  let bx = MARGIN + (CONTENT_W - totalW) / 2;
  const by = doc.y;

  ensureSpace(bh + 30);
  boxes.forEach((box, i) => {
    filledRect(bx, by, bw, bh, box.color, 6);
    const [line1, line2] = box.label.split("\n");
    doc.fontSize(10).font("Helvetica-Bold").fillColor(C.WHITE)
       .text(line1, bx, by + (line2 ? 8 : 14), { align: "center", width: bw, lineBreak: false });
    if (line2) {
      doc.fontSize(10).font("Helvetica-Bold").fillColor(C.WHITE)
         .text(line2, bx, by + 22, { align: "center", width: bw, lineBreak: false });
    }
    doc.fontSize(7.5).font("Helvetica").fillColor("#DDDDDD")
       .text(box.sub, bx, by + bh - 16, { align: "center", width: bw, lineBreak: false });
    if (i < boxes.length - 1) {
      doc.fontSize(16).font("Helvetica-Bold").fillColor(C.YELLOW)
         .text("→", bx + bw + 2, by + 17, { lineBreak: false });
    }
    bx += bw + bgap + 14;
  });

  // Feedback arc label
  doc.fontSize(8).font("Helvetica-Oblique").fillColor(C.CYAN)
     .text("↩ Feedback loop: iterate and improve", MARGIN, by + bh + 6,
       { align: "center", width: CONTENT_W });
  doc.y = by + bh + 22;

  // Step-by-step table
  h2("Step-by-Step: What You Do Each Day");
  drawTable(
    ["Step", "Tool", "What You Do", "Result"],
    [
      ["1", "VS Code",    "Open project, edit app.js or HTML files",       "New code written"],
      ["2", "Terminal",   "git add . && git commit -m 'message'",          "Change saved to history"],
      ["3", "Terminal",   "git push origin main",                          "Code backed up on GitHub"],
      ["4", "Terminal",   "docker build -t myapp .",                       "Docker image created"],
      ["5", "Terminal",   "docker run -p 3000:8081 myapp",                 "Container running"],
      ["6", "Browser",    "Visit http://localhost:3000",                   "You see your webpage!"],
    ],
    [28, 58, 285, 144],
    {
      hdrBg: C.BLUE_DARK,
      altBg: C.GRAY_LIGHT,
      colFonts: { 2: { font: "Courier", size: 8, color: "#1A237E" } },
    }
  );

  doc.moveDown(0.3);

  h2("Your Project File Structure");
  ensureSpace(160);
  const treeY = doc.y;
  filledRect(MARGIN, treeY, CONTENT_W, 150, C.BG_DARK, 6);
  const tree = [
    { indent: 0, text: "demo_nodejs_webpage/           ← Your project root",    color: C.YELLOW },
    { indent: 1, text: "├── app.js                     ← Main Express server",  color: C.CYAN },
    { indent: 1, text: "├── package.json               ← Dependencies & scripts", color: C.GREEN },
    { indent: 1, text: "├── Dockerfile                 ← Docker build recipe",  color: C.ORANGE },
    { indent: 1, text: "├── index.html                 ← Homepage",             color: C.WHITE },
    { indent: 1, text: "├── about.html                 ← About page",           color: C.WHITE },
    { indent: 1, text: "├── routes/                    ← Express route handlers", color: "#CE93D8" },
    { indent: 2, text: "│   └── tasks.js",                                       color: "#CE93D8" },
    { indent: 1, text: "└── data/                      ← Data layer",           color: "#CE93D8" },
    { indent: 2, text: "    └── task.js",                                        color: "#CE93D8" },
  ];
  tree.forEach((item, i) => {
    doc.fontSize(8.5).font("Courier").fillColor(item.color)
       .text(item.text, MARGIN + 12 + item.indent * 10, treeY + 8 + i * 14,
         { lineBreak: false });
  });
  doc.y = treeY + 155;

  doc.moveDown(0.3);
  calloutBox(
    "IMPORTANT — Port Mismatch in YOUR project: " +
    "app.js listens on port 8081, but your Dockerfile says EXPOSE 3000. " +
    "This means you must run: docker run -p 3000:8081 myapp  " +
    "(left=what browser uses, right=what app uses inside container). " +
    "This is covered in detail in the Common Errors section.",
    "warning"
  );
}

// ─── Section 2: Git Commands ───────────────────────────────────────────────
function buildGit() {
  console.log("Building Section 2: Git Commands...");
  newPage();
  sectionHeader("Section 2 — Git Fundamentals & Daily Commands");

  bodyText(
    "Git is a version control system — it keeps a complete history of every change " +
    "you make, so you can always go back, compare, or share your work."
  );
  doc.moveDown(0.5);

  // 4-zone mental model
  h2("The Git Mental Model — 4 Zones");
  ensureSpace(90);
  const zones = [
    { label: "Working\nDirectory", sub: "Your files",  bg: C.RED_LIGHT,    fg: "#B71C1C" },
    { label: "Staging\nArea",      sub: "git add",     bg: C.ORANGE_LIGHT, fg: "#E65100" },
    { label: "Local\nRepo",        sub: "git commit",  bg: C.GREEN_LIGHT,  fg: C.GREEN_DARK },
    { label: "Remote\nGitHub",     sub: "git push",    bg: C.BLUE_LIGHT,   fg: C.BLUE_DARK },
  ];
  const zw = CONTENT_W / 4 - 6, zh = 70;
  let zx = MARGIN;
  const zy = doc.y;
  zones.forEach((zone, i) => {
    filledRect(zx, zy, zw, zh, zone.bg, 6);
    doc.rect(zx, zy, zw, zh).strokeColor(zone.fg).lineWidth(1.5).stroke();
    const [l1, l2] = zone.label.split("\n");
    doc.fontSize(10).font("Helvetica-Bold").fillColor(zone.fg)
       .text(l1, zx, zy + 10, { align: "center", width: zw, lineBreak: false });
    if (l2) {
      doc.fontSize(10).font("Helvetica-Bold").fillColor(zone.fg)
         .text(l2, zx, zy + 23, { align: "center", width: zw, lineBreak: false });
    }
    doc.fontSize(8).font("Courier").fillColor(zone.fg)
       .text(zone.sub, zx, zy + zh - 18, { align: "center", width: zw, lineBreak: false });
    if (i < zones.length - 1) {
      doc.fontSize(14).font("Helvetica-Bold").fillColor(C.GRAY)
         .text("→", zx + zw + 1, zy + 26, { lineBreak: false });
    }
    zx += zw + 8;
  });
  doc.y = zy + zh + 8;

  calloutBox(
    "Files live in your Working Directory. You stage selected changes, " +
    "commit them to local history, then push to share on GitHub.",
    "tip"
  );
  doc.moveDown(0.5);

  // Command table
  h2("Daily Git Commands Reference");
  drawTable(
    ["Command", "What It Does", "Example"],
    [
      ["git init",            "Create a new Git repo",                    "git init"],
      ["git status",          "See what's changed / staged",              "git status"],
      ["git add <file>",      "Stage a specific file",                    "git add app.js"],
      ["git add .",           "Stage ALL changed files",                  "git add ."],
      ["git commit -m",       "Save staged changes with message",         'git commit -m "add route"'],
      ["git log --oneline",   "See compact commit history",               "git log --oneline"],
      ["git diff",            "See unstaged changes",                     "git diff app.js"],
      ["git push origin main","Upload commits to GitHub",                 "git push origin main"],
      ["git pull origin main","Download latest from GitHub",              "git pull origin main"],
      ["git clone <url>",     "Download a repo from GitHub",              "git clone https://..."],
      ["git branch",          "List all branches",                        "git branch"],
      ["git checkout -b",     "Create & switch to new branch",            "git checkout -b feature/x"],
      ["git merge <branch>",  "Merge a branch into current",              "git merge feature/x"],
      ["git stash",           "Temporarily save uncommitted work",        "git stash"],
      ["git stash pop",       "Restore stashed work",                     "git stash pop"],
    ],
    [110, 175, 230],
    {
      hdrBg: C.BLUE_DARK,
      altBg: C.GRAY_LIGHT,
      colFonts: {
        0: { font: "Courier", size: 8.5, color: "#1A237E" },
        2: { font: "Courier", size: 8.5, color: "#1B5E20" },
      },
    }
  );

  doc.moveDown(0.5);
  h2("Good vs Bad Commit Messages");
  sideBySideCode(
    "BAD — avoid these",
    [
      'git commit -m "fix"',
      'git commit -m "changes"',
      'git commit -m "asdf"',
      'git commit -m "wip"',
      'git commit -m "stuff"',
    ],
    "GOOD — use these",
    [
      'git commit -m "fix port mismatch in Dockerfile"',
      'git commit -m "add /about route to app.js"',
      'git commit -m "update package.json description"',
      'git commit -m "work in progress: adding task routes"',
      'git commit -m "remove unused console.log in app.js"',
    ]
  );

  calloutBox(
    'Rule: A good commit message completes the sentence "If applied, this commit will..."',
    "tip"
  );
  doc.moveDown(0.4);

  h2("Real Workflow Using YOUR Project");
  codeBlock([
    "# You just edited app.js to add a new route",
    "",
    "git status                        # see: modified app.js",
    "git diff app.js                   # review your changes",
    "git add app.js                    # stage just that file",
    'git commit -m "add /contact route to Express app"',
    "git push origin main              # send to GitHub",
    "",
    "# Later, pull changes from another machine",
    "git pull origin main",
  ]);
}

// ─── Section 3: Branching ──────────────────────────────────────────────────
function buildBranching() {
  console.log("Building Section 3: Branching...");
  newPage();
  sectionHeader("Section 3 — Branching Strategies");

  bodyText(
    "A branch is an independent copy of your code where you can make changes " +
    "without affecting the main, working version. Think of it like a parallel universe for your code."
  );
  doc.moveDown(0.5);

  // Branch diagram
  h2("What a Branch Looks Like");
  ensureSpace(110);
  const dy = doc.y;
  const mainY = dy + 65;
  const featY = dy + 25;

  // main line
  doc.moveTo(MARGIN + 20, mainY).lineTo(MARGIN + CONTENT_W - 10, mainY)
     .strokeColor(C.BLUE_DARK).lineWidth(3).stroke();

  // commits on main
  const mainCommits = [
    { x: MARGIN + 20, label: "C1" },
    { x: MARGIN + 80, label: "C2" },
    { x: MARGIN + 160, label: "C3" },
    { x: MARGIN + 390, label: "C7" },
    { x: MARGIN + CONTENT_W - 10, label: "C8" },
  ];
  mainCommits.forEach(c => {
    doc.circle(c.x, mainY, 12).fill(C.BLUE_DARK);
    doc.circle(c.x, mainY, 12).strokeColor(C.WHITE).lineWidth(1).stroke();
    doc.fontSize(7).font("Helvetica-Bold").fillColor(C.WHITE)
       .text(c.label, c.x - 6, mainY - 4, { lineBreak: false });
  });

  // feature branch
  doc.moveTo(MARGIN + 160, mainY).lineTo(MARGIN + 200, featY)
     .strokeColor(C.GREEN).lineWidth(2).stroke();
  doc.moveTo(MARGIN + 200, featY).lineTo(MARGIN + 360, featY)
     .strokeColor(C.GREEN).lineWidth(3).stroke();
  doc.moveTo(MARGIN + 360, featY).lineTo(MARGIN + 390, mainY)
     .strokeColor(C.GREEN).lineWidth(2).stroke();

  const featCommits = [
    { x: MARGIN + 220, label: "C4" },
    { x: MARGIN + 280, label: "C5" },
    { x: MARGIN + 340, label: "C6" },
  ];
  featCommits.forEach(c => {
    doc.circle(c.x, featY, 12).fill(C.GREEN);
    doc.circle(c.x, featY, 12).strokeColor(C.WHITE).lineWidth(1).stroke();
    doc.fontSize(7).font("Helvetica-Bold").fillColor(C.WHITE)
       .text(c.label, c.x - 6, featY - 4, { lineBreak: false });
  });

  doc.fontSize(8).font("Helvetica-Bold").fillColor(C.BLUE_DARK)
     .text("main branch", MARGIN + 30, mainY + 15, { lineBreak: false });
  doc.fontSize(8).font("Helvetica-Bold").fillColor(C.GREEN_DARK)
     .text("feature/add-new-route branch", MARGIN + 200, featY - 18, { lineBreak: false });

  doc.y = dy + 100;

  calloutBox(
    "The main branch always stays working. You create a feature branch, " +
    "do your work there, then merge it back when done.",
    "tip"
  );
  doc.moveDown(0.5);

  // GitHub Flow steps
  h2("GitHub Flow (Recommended for Beginners)");
  const steps = [
    { num: "1", title: "Create branch",  cmd: "git checkout -b feature/new-route",   color: "#9C27B0" },
    { num: "2", title: "Make changes",   cmd: "Edit app.js, add your new feature",    color: C.BLUE_DARK },
    { num: "3", title: "Commit often",   cmd: 'git add . && git commit -m "add route"', color: C.CYAN },
    { num: "4", title: "Push branch",    cmd: "git push origin feature/new-route",   color: C.GREEN_DARK },
    { num: "5", title: "Open PR",        cmd: "On GitHub: compare & pull request",    color: C.ORANGE },
    { num: "6", title: "Merge & delete", cmd: "Merge PR, delete branch on GitHub",   color: C.RED },
  ];
  steps.forEach(step => {
    ensureSpace(28);
    const sy = doc.y;
    filledRect(MARGIN, sy, 26, 24, step.color, 3);
    doc.fontSize(11).font("Helvetica-Bold").fillColor(C.WHITE)
       .text(step.num, MARGIN, sy + 6, { align: "center", width: 26, lineBreak: false });
    filledRect(MARGIN + 26, sy, 100, 24, C.GRAY_LIGHT, 0);
    doc.fontSize(9).font("Helvetica-Bold").fillColor(C.GRAY_DARK)
       .text(step.title, MARGIN + 31, sy + 7, { width: 95, lineBreak: false });
    filledRect(MARGIN + 126, sy, CONTENT_W - 126, 24, C.WHITE, 0);
    doc.fontSize(8.5).font("Courier").fillColor("#1A237E")
       .text(step.cmd, MARGIN + 131, sy + 7, { width: CONTENT_W - 136, lineBreak: false });
    doc.rect(MARGIN, sy, CONTENT_W, 24).strokeColor("#CFD8DC").lineWidth(0.5).stroke();
    doc.y = sy + 28;
  });
  doc.moveDown(0.5);

  // GitHub Flow vs Git Flow
  h2("GitHub Flow vs Git Flow — Side-by-Side");
  ensureSpace(130);
  const gfy = doc.y;
  const halfW = CONTENT_W / 2 - 4;

  filledRect(MARGIN, gfy, halfW, 20, C.GREEN_LIGHT, 3);
  doc.fontSize(10).font("Helvetica-Bold").fillColor(C.GREEN_DARK)
     .text("GitHub Flow  (SIMPLE — use this)", MARGIN + 5, gfy + 5,
       { width: halfW - 10, lineBreak: false });

  filledRect(MARGIN + halfW + 8, gfy, halfW, 20, C.BLUE_LIGHT, 3);
  doc.fontSize(10).font("Helvetica-Bold").fillColor(C.BLUE_DARK)
     .text("Git Flow  (complex — learn later)", MARGIN + halfW + 13, gfy + 5,
       { width: halfW - 10, lineBreak: false });

  const compareItems = [
    ["2 key branches: main + feature/*",        "5 branch types: main, develop, feature, release, hotfix"],
    ["Deploy directly from main",               "Deploy from release branches only"],
    ["Great for: small teams, web apps",        "Great for: large teams, versioned software"],
    ["YOUR demo project: USE THIS ✅",           "Learn this when working in larger teams"],
  ];
  compareItems.forEach((row, ri) => {
    const ry = gfy + 20 + ri * 22;
    const bg = ri % 2 === 0 ? C.WHITE : C.GREEN_LIGHT;
    const bg2 = ri % 2 === 0 ? C.WHITE : C.BLUE_LIGHT;
    filledRect(MARGIN, ry, halfW, 22, bg, 0);
    filledRect(MARGIN + halfW + 8, ry, halfW, 22, bg2, 0);
    doc.fontSize(8.5).font("Helvetica").fillColor(C.BLACK)
       .text(row[0], MARGIN + 5, ry + 6, { width: halfW - 10, lineBreak: false });
    doc.fontSize(8.5).font("Helvetica").fillColor(C.BLACK)
       .text(row[1], MARGIN + halfW + 13, ry + 6, { width: halfW - 10, lineBreak: false });
  });
  doc.rect(MARGIN, gfy, halfW, 20 + compareItems.length * 22)
     .strokeColor("#CFD8DC").lineWidth(0.5).stroke();
  doc.rect(MARGIN + halfW + 8, gfy, halfW, 20 + compareItems.length * 22)
     .strokeColor("#CFD8DC").lineWidth(0.5).stroke();
  doc.y = gfy + 20 + compareItems.length * 22 + 10;

  h2("Branch Naming Conventions");
  drawTable(
    ["Branch Type", "Pattern", "Example for YOUR project"],
    [
      ["Feature",   "feature/<description>",  "feature/add-contact-page"],
      ["Bug fix",   "fix/<description>",       "fix/port-mismatch-dockerfile"],
      ["Hotfix",    "hotfix/<description>",    "hotfix/app-crash-on-startup"],
      ["Docs",      "docs/<description>",      "docs/add-readme"],
      ["Refactor",  "refactor/<description>",  "refactor/split-routes"],
    ],
    [80, 160, 275],
    {
      hdrBg: C.GRAY_DARK,
      colFonts: {
        1: { font: "Courier", size: 8.5, color: "#1A237E" },
        2: { font: "Courier", size: 8.5, color: C.GREEN_DARK },
      },
    }
  );
}

// ─── Section 4: Docker Concepts ────────────────────────────────────────────
function buildDockerConcepts() {
  console.log("Building Section 4: Docker Concepts...");
  newPage();
  sectionHeader("Section 4 — Docker: Images vs Containers");

  bodyText(
    'Docker solves the classic problem: "It works on my machine!" ' +
    "It packages your app with EVERYTHING it needs — Node.js, dependencies, config — " +
    "into a single unit that runs identically everywhere."
  );
  doc.moveDown(0.5);

  h2("The Analogy That Makes Docker Click");
  drawTable(
    ["Real World", "Docker Equivalent", "In Your Project"],
    [
      ["Cookie recipe",    "Dockerfile",         "Your Dockerfile file"],
      ["Cookie cutter",    "Image",              "node:alpine + your app code"],
      ["Actual cookie",    "Container",          "Running instance of your app"],
      ["Multiple cookies", "Multiple containers","Scale to handle more users"],
    ],
    [130, 130, 255],
    { hdrBg: C.ORANGE, altBg: C.ORANGE_LIGHT }
  );

  doc.moveDown(0.5);
  h2("Image vs Container — Visual Comparison");

  ensureSpace(170);
  const icY = doc.y;
  const halfW = CONTENT_W / 2 - 10;

  // IMAGE box
  filledRect(MARGIN, icY, halfW, 150, C.BLUE_LIGHT, 8);
  doc.rect(MARGIN, icY, halfW, 150).strokeColor(C.BLUE_DARK).lineWidth(2).stroke();
  doc.fontSize(13).font("Helvetica-Bold").fillColor(C.BLUE_DARK)
     .text("IMAGE", MARGIN, icY + 8, { align: "center", width: halfW });

  const imageLayers = [
    { label: "node:alpine (base OS)",    color: C.BLUE_DARK },
    { label: "npm install (deps)",       color: C.BLUE },
    { label: "app.js + HTML files",      color: "#1976D2" },
    { label: "package.json",             color: "#42A5F5" },
  ];
  imageLayers.forEach((layer, i) => {
    filledRect(MARGIN + 10, icY + 32 + i * 22, halfW - 20, 18, layer.color, 2);
    doc.fontSize(8).font("Courier").fillColor(C.WHITE)
       .text(layer.label, MARGIN + 14, icY + 36 + i * 22,
         { width: halfW - 28, lineBreak: false });
  });
  doc.fontSize(9).font("Helvetica-Bold").fillColor(C.BLUE_DARK)
     .text("READ-ONLY Blueprint", MARGIN, icY + 135,
       { align: "center", width: halfW });

  // Arrow
  doc.fontSize(20).font("Helvetica-Bold").fillColor(C.GRAY)
     .text("→", MARGIN + halfW + 2, icY + 65, { lineBreak: false });
  doc.fontSize(8).font("Courier").fillColor(C.GRAY)
     .text("docker run", MARGIN + halfW, icY + 88, { lineBreak: false });

  // CONTAINER box
  const cx = MARGIN + halfW + 30;
  filledRect(cx, icY, halfW, 150, C.GREEN_LIGHT, 8);
  doc.rect(cx, icY, halfW, 150).strokeColor(C.GREEN_DARK).lineWidth(2).stroke();
  doc.fontSize(13).font("Helvetica-Bold").fillColor(C.GREEN_DARK)
     .text("CONTAINER", cx, icY + 8, { align: "center", width: halfW });

  filledRect(cx + 10, icY + 30, halfW - 20, 80, C.BLUE_LIGHT, 4);
  doc.fontSize(8.5).font("Helvetica-Bold").fillColor(C.BLUE_DARK)
     .text("Image layers (read-only)", cx + 14, icY + 36,
       { width: halfW - 28, lineBreak: false });
  doc.fontSize(7.5).font("Courier").fillColor(C.BLUE)
     .text("node:alpine + your app code", cx + 14, icY + 50,
       { width: halfW - 28, lineBreak: false });

  filledRect(cx + 10, icY + 114, halfW - 20, 18, C.GREEN, 3);
  doc.fontSize(8).font("Courier").fillColor(C.WHITE)
     .text("Writable runtime layer", cx + 14, icY + 118,
       { width: halfW - 28, lineBreak: false });
  doc.fontSize(9).font("Helvetica-Bold").fillColor(C.GREEN_DARK)
     .text("LIVE — Port 8081 active", cx, icY + 135,
       { align: "center", width: halfW });

  doc.y = icY + 158;

  calloutBox(
    "Key difference: An IMAGE is static (a snapshot). " +
    "A CONTAINER is a live, running instance of that image. " +
    "You can run many containers from one image.",
    "tip"
  );
  doc.moveDown(0.5);

  h2("Essential Docker Commands");
  drawTable(
    ["Command", "What It Does", "Example"],
    [
      ["docker build -t <name> .",         "Build image from Dockerfile",          "docker build -t myapp ."],
      ["docker images",                     "List all images",                      "docker images"],
      ["docker run -p <host>:<cont> <img>", "Start container from image",           "docker run -p 3000:8081 myapp"],
      ["docker ps",                         "List running containers",              "docker ps"],
      ["docker ps -a",                      "List ALL containers",                  "docker ps -a"],
      ["docker stop <id>",                  "Stop a running container",             "docker stop abc123"],
      ["docker rm <id>",                    "Delete a stopped container",           "docker rm abc123"],
      ["docker rmi <name>",                 "Delete an image",                      "docker rmi myapp"],
      ["docker logs <id>",                  "View container output/logs",           "docker logs abc123"],
      ["docker exec -it <id> sh",           "Open shell inside container",          "docker exec -it abc123 sh"],
    ],
    [155, 175, 185],
    {
      hdrBg: C.GREEN_DARK,
      altBg: C.GREEN_LIGHT,
      colFonts: {
        0: { font: "Courier", size: 8, color: "#1B5E20" },
        2: { font: "Courier", size: 8, color: C.BLUE_DARK },
      },
    }
  );

  calloutBox(
    "Port mapping  (-p host:container):  LEFT number = browser port.  " +
    "RIGHT = app port inside container.  " +
    "For YOUR project: -p 3000:8081 → visit localhost:3000 → hits app on 8081.",
    "tip"
  );
}

// ─── Section 5: Dockerfile ─────────────────────────────────────────────────
function buildDockerfile() {
  console.log("Building Section 5: Dockerfile...");
  newPage();
  sectionHeader("Section 5 — Your Dockerfile, Line by Line");

  bodyText(
    "A Dockerfile is a recipe — a script Docker follows to build your image. " +
    "Here is YOUR actual Dockerfile from demo_nodejs_webpage/, explained line by line:"
  );
  doc.moveDown(0.5);

  const lines = [
    {
      code:  "FROM node:alpine",
      label: "BASE IMAGE",
      color: C.BLUE_DARK,
      desc:  "Start from an official Node.js image built on Alpine Linux (a tiny, secure Linux distro). " +
             "This gives you Node.js and npm pre-installed. Alpine keeps the image small (~120MB vs ~900MB for full Ubuntu).",
    },
    {
      code:  "WORKDIR /app",
      label: "WORKING DIR",
      color: C.GREEN_DARK,
      desc:  "Set /app as the working directory inside the container. All subsequent commands run from here. " +
             "If /app doesn't exist, Docker creates it automatically.",
    },
    {
      code:  "COPY package*.json ./",
      label: "COPY DEPS FIRST",
      color: C.ORANGE,
      desc:  "Copy only package.json BEFORE copying all code. Smart trick: Docker caches this layer. " +
             "If you only change app.js, npm install won't re-run — saving minutes of build time!",
    },
    {
      code:  "RUN npm install",
      label: "INSTALL DEPS",
      color: "#9C27B0",
      desc:  "Run npm install to download all dependencies (like Express). These get installed into " +
             "/app/node_modules inside the image.",
    },
    {
      code:  "COPY . .",
      label: "COPY ALL CODE",
      color: C.CYAN,
      desc:  "Copy everything from your local project folder into /app in the image. " +
             "This includes app.js, index.html, about.html, routes/, data/, etc.",
    },
    {
      code:  "EXPOSE 3000",
      label: "DOCUMENT PORT ⚠️",
      color: C.RED,
      desc:  "Tell Docker (and humans) that the container intends to use port 3000. " +
             "NOTE: Your app.js actually listens on 8081 — this is a mismatch! " +
             "EXPOSE is just documentation; you fix it at docker run with -p 3000:8081.",
    },
    {
      code:  'CMD ["npm", "start"]',
      label: "START CMD",
      color: "#795548",
      desc:  'The default command when the container starts. Runs "npm start" which executes "node app.js" ' +
             '(as defined in package.json). Use array form ["cmd","arg"] for better signal handling.',
    },
  ];

  lines.forEach(item => {
    ensureSpace(58);
    const ly = doc.y;
    filledRect(MARGIN, ly, 80, 26, item.color, 3);
    doc.fontSize(7).font("Helvetica-Bold").fillColor(C.WHITE)
       .text(item.label, MARGIN + 2, ly + 9, { align: "center", width: 76, lineBreak: false });
    filledRect(MARGIN + 80, ly, CONTENT_W - 80, 26, C.BG_DARK, 0);
    doc.fontSize(10).font("Courier").fillColor(C.CYAN)
       .text(item.code, MARGIN + 88, ly + 8,
         { width: CONTENT_W - 96, lineBreak: false });
    doc.y = ly + 28;
    doc.fontSize(9).font("Helvetica").fillColor(C.GRAY_DARK)
       .text("    ↑ " + item.desc, MARGIN + 4, doc.y,
         { width: CONTENT_W - 8, align: "left" });
    doc.moveDown(0.35);
  });

  doc.moveDown(0.4);
  h2("Current Dockerfile vs Improved Version");

  sideBySideCode(
    "Current (has issues)",
    [
      "# YOUR CURRENT Dockerfile",
      "",
      "FROM node:alpine",
      "WORKDIR /app",
      "COPY package*.json ./",
      "RUN npm install",
      "COPY . .",
      "EXPOSE 3000",
      'CMD ["npm", "start"]',
    ],
    "Improved version",
    [
      "# IMPROVED Dockerfile",
      "",
      "FROM node:18-alpine",
      "WORKDIR /app",
      "COPY package*.json ./",
      "RUN npm ci --only=production",
      "COPY . .",
      "EXPOSE 8081  # match app.js!",
      'CMD ["node", "app.js"]',
    ]
  );

  const improvements = [
    "node:18-alpine pins a specific Node version — builds stay reproducible.",
    "npm ci is faster and stricter, ideal for containers and CI pipelines.",
    "--only=production skips devDependencies — smaller final image.",
    "EXPOSE 8081 matches what app.js actually uses.",
    "node app.js directly is slightly more efficient than npm start in containers.",
  ];
  improvements.forEach(imp => {
    bodyText("• " + imp, { indent: 10 });
  });
}

// ─── Section 6: Common Errors ──────────────────────────────────────────────
function buildErrors() {
  console.log("Building Section 6: Common Errors...");
  newPage();
  sectionHeader("Section 6 — Common Errors & Fixes");

  bodyText(
    "Every developer hits these. Here are the most common errors in YOUR project " +
    "workflow, with exact fixes:"
  );
  doc.moveDown(0.4);

  const errors = [
    {
      id: "ERR-01", color: C.RED,
      title: "Port Mismatch — YOUR project has this right now!",
      error: [
        "docker run -p 3000:3000 myapp",
        "# App runs but browser shows 'This site can't be reached'",
      ],
      cause: "app.js listens on 8081, but you mapped -p 3000:3000 (container side wrong).",
      fix:   ["docker run -p 3000:8081 myapp",
              "# OR fix Dockerfile: change EXPOSE 3000 to EXPOSE 8081"],
      why:   "The RIGHT side of -p must match the port your app ACTUALLY uses inside the container.",
    },
    {
      id: "ERR-02", color: C.ORANGE,
      title: "Git Push Rejected",
      error: [
        "! [rejected]  main -> main (non-fast-forward)",
        "error: failed to push some refs",
      ],
      cause: "Someone else (or you on another machine) pushed commits you don't have locally.",
      fix:   ["git pull origin main --rebase", "git push origin main"],
      why:   "Pull first to merge their work, then push your combined history.",
    },
    {
      id: "ERR-03", color: C.ORANGE,
      title: "Cannot find module 'express'",
      error: [
        "Error: Cannot find module 'express'",
        "    at Function.Module._resolveFilename",
      ],
      cause: "Dependencies not installed. node_modules folder is missing.",
      fix:   ["npm install", "docker build -t myapp .    # rebuild image"],
      why:   "node_modules is in .gitignore (correctly). Always run npm install after cloning.",
    },
    {
      id: "ERR-04", color: C.RED,
      title: "Merge Conflict",
      error: [
        "CONFLICT (content): Merge conflict in app.js",
        "Automatic merge failed; fix conflicts and then commit",
      ],
      cause: "Two branches changed the same lines. Git doesn't know which to keep.",
      fix:   [
        "# Open app.js in VS Code, look for <<<<<<< markers",
        "# Keep the version you want, delete the markers",
        "git add app.js",
        'git commit -m "resolve merge conflict in app.js"',
      ],
      why:   "Conflicts are normal — Git is asking YOU to make the decision it can't.",
    },
    {
      id: "ERR-05", color: C.ORANGE,
      title: "Docker: address already in use",
      error: [
        "Error: bind: address already in use",
        "... port 3000 already allocated",
      ],
      cause: "Another container (or process) is already using port 3000 on your machine.",
      fix:   [
        "docker ps                    # find running containers",
        "docker stop <container_id>   # stop the conflicting one",
        "# OR use a different host port:",
        "docker run -p 3001:8081 myapp",
      ],
      why:   "Each port on your machine can only be used by one process at a time.",
    },
    {
      id: "ERR-06", color: C.GRAY,
      title: "Git: nothing to commit, working tree clean",
      error: ["nothing to commit, working tree clean"],
      cause: "Not actually an error — means you have no unsaved changes.",
      fix:   [
        "git status        # check what's happening",
        "git log --oneline # verify your last commit is there",
      ],
      why:   "This message means everything is saved. Check git log to confirm.",
    },
    {
      id: "ERR-07", color: C.RED,
      title: "Docker build: COPY failed — file not found",
      error: [
        "COPY failed: file not found in build context",
        "or excluded by .dockerignore",
      ],
      cause: "The file you're trying to COPY doesn't exist, or is in .dockerignore.",
      fix:   [
        "ls -la             # verify the file exists in your project",
        "cat .dockerignore  # check if the file is excluded",
        "docker build -t myapp .   # the dot = current folder!",
      ],
      why:   "Docker builds from the 'context' (folder). Always run docker build from project root.",
    },
  ];

  errors.forEach(err => {
    ensureSpace(100);
    filledRect(MARGIN, doc.y, CONTENT_W, 26, err.color, 4);
    doc.fontSize(10).font("Helvetica-Bold").fillColor(C.WHITE)
       .text(`${err.id}  ${err.title}`, MARGIN + 8, doc.y + 8,
         { width: CONTENT_W - 16, lineBreak: false });
    doc.moveDown(0.15);

    h3("Error message:");
    codeBlock(err.error, "bad");
    h3("Cause:");
    bodyText(err.cause);
    h3("Fix:");
    codeBlock(err.fix, "good");
    calloutBox("Why it works: " + err.why, "tip");
    doc.moveDown(0.3);
    hline(C.GRAY_LIGHT);
    doc.moveDown(0.2);
  });
}

// ─── Section 7: Cheat Sheets ───────────────────────────────────────────────
function buildCheatSheets() {
  console.log("Building Section 7: Cheat Sheets...");
  newPage();
  sectionHeader("Section 7 — Cheat Sheets");

  // Git Cheat Sheet
  miniHeader("GIT CHEAT SHEET", C.BLUE_DARK);
  doc.moveDown(0.3);
  drawTable(
    ["Category", "Command", "What It Does"],
    [
      ["SETUP",     'git config --global user.name "Muhammad Arham"',   "Set your name"],
      ["",          'git config --global user.email "your@email.com"',  "Set your email"],
      ["START",     "git init",                                          "New local repo"],
      ["",          "git clone <url>",                                   "Clone from GitHub"],
      ["SNAPSHOT",  "git status",                                        "See changes"],
      ["",          "git add <file>",                                    "Stage a file"],
      ["",          "git add .",                                         "Stage all"],
      ["",          'git commit -m "msg"',                               "Save snapshot"],
      ["HISTORY",   "git log --oneline",                                 "Compact history"],
      ["",          "git diff",                                          "Unstaged changes"],
      ["",          "git diff --staged",                                 "Staged changes"],
      ["BRANCHES",  "git branch",                                        "List branches"],
      ["",          "git checkout -b <name>",                            "New branch"],
      ["",          "git checkout main",                                 "Switch to main"],
      ["",          "git merge <branch>",                                "Merge branch"],
      ["REMOTE",    "git push origin main",                              "Push to GitHub"],
      ["",          "git pull origin main",                              "Pull from GitHub"],
      ["UNDO",      "git restore <file>",                                "Discard changes"],
      ["",          "git reset HEAD~1",                                  "Undo last commit"],
      ["",          "git stash",                                         "Stash changes"],
      ["",          "git stash pop",                                     "Restore stash"],
    ],
    [70, 220, 225],
    {
      hdrBg: C.BLUE_DARK,
      altBg: C.GRAY_LIGHT,
      rowH: 18,
      colFonts: {
        0: { font: "Helvetica-Bold", size: 8, color: C.BLUE_DARK },
        1: { font: "Courier", size: 8, color: "#1A237E" },
      },
    }
  );

  doc.moveDown(0.5);
  miniHeader("DOCKER CHEAT SHEET", C.GREEN_DARK);
  doc.moveDown(0.3);
  drawTable(
    ["Category", "Command", "What It Does"],
    [
      ["IMAGES",     "docker build -t myapp .",               "Build image"],
      ["",           "docker build -t myapp:v1.0 .",          "Build with version tag"],
      ["",           "docker images",                          "List images"],
      ["",           "docker rmi myapp",                       "Remove image"],
      ["CONTAINERS", "docker run -p 3000:8081 myapp",         "Run (your project)"],
      ["",           "docker run -d -p 3000:8081 myapp",      "Run in background"],
      ["",           "docker run --name web myapp",            "Run with name"],
      ["",           "docker ps",                              "Running containers"],
      ["",           "docker ps -a",                           "All containers"],
      ["",           "docker stop web",                        "Stop container"],
      ["",           "docker rm web",                          "Remove container"],
      ["INSPECT",    "docker logs web",                        "View logs"],
      ["",           "docker logs -f web",                     "Follow live logs"],
      ["",           "docker exec -it web sh",                 "Shell into container"],
      ["CLEANUP",    "docker system prune",                    "Remove all unused"],
    ],
    [70, 235, 210],
    {
      hdrBg: C.GREEN_DARK,
      altBg: C.GREEN_LIGHT,
      rowH: 18,
      colFonts: {
        0: { font: "Helvetica-Bold", size: 8, color: C.GREEN_DARK },
        1: { font: "Courier", size: 8, color: "#1B5E20" },
      },
    }
  );

  newPage();
  miniHeader("YOUR PROJECT — QUICK COMMAND REFERENCE", C.PURPLE);
  doc.moveDown(0.3);
  drawTable(
    ["Action", "Command"],
    [
      ["Build Docker image",               "docker build -t demo-nodejs ."],
      ["Run app (correct port mapping)",   "docker run -p 3000:8081 demo-nodejs"],
      ["Run in background (detached)",     "docker run -d -p 3000:8081 --name demo demo-nodejs"],
      ["View app in browser",              "http://localhost:3000"],
      ["See app logs",                     "docker logs demo"],
      ["Stop running app",                 "docker stop demo"],
      ["Rebuild after code change",        "docker stop demo && docker rm demo && docker build -t demo-nodejs . && docker run -d -p 3000:8081 --name demo demo-nodejs"],
      ["Push code to GitHub",              "git add . && git commit -m 'your message' && git push origin main"],
      ["Create a feature branch",          "git checkout -b feature/my-feature"],
      ["Merge feature branch to main",     "git checkout main && git merge feature/my-feature"],
    ],
    [160, 355],
    {
      hdrBg: C.PURPLE,
      altBg: C.PURPLE_LIGHT,
      rowH: 22,
      colFonts: {
        1: { font: "Courier", size: 7.5, color: "#1A237E" },
      },
    }
  );

  doc.moveDown(0.5);
  miniHeader("WHAT GOES IN .gitignore", C.GRAY_DARK);
  doc.moveDown(0.3);
  bodyText(
    "A .gitignore file tells Git which files to never track. " +
    "Here's what your Node.js project should ignore:"
  );
  doc.moveDown(0.2);
  codeBlock([
    "node_modules/          # 3rd-party packages (re-installed via npm install)",
    ".env                   # Secrets, API keys — NEVER commit these!",
    ".DS_Store              # Mac metadata files",
    "*.log                  # Log files",
    "dist/                  # Build output",
    "",
    "# NOT ignored (you DO want to commit these):",
    "# package.json         - dependency list",
    "# package-lock.json    - exact dependency versions",
    "# Dockerfile           - container recipe",
    "# app.js, *.html       - your actual code",
  ]);

  doc.moveDown(0.5);
  miniHeader("BEGINNER TIPS — THINGS TO REMEMBER", C.ORANGE);
  doc.moveDown(0.3);
  const tips = [
    ["Commit often, push daily",     "Small commits are easier to understand and revert than giant ones."],
    ["Read the full error message",   "Docker and Git errors are descriptive. Read the FULL error, not just the first line."],
    ["Google the exact error",        "Copy the error message into Google. Stack Overflow and GitHub Issues are gold."],
    ["Use git status constantly",     "Before and after every git command. It's your compass."],
    ["Tag your Docker images",        "Use -t myapp:v1.0 so you can roll back to previous versions."],
    ["Keep main always working",      "Never push broken code to main. Use branches for experiments."],
    ["Fix your port mismatch",        "Change EXPOSE 3000 to EXPOSE 8081 in your Dockerfile — it currently mismatches app.js."],
  ];
  drawTable(
    ["Tip", "Why"],
    tips,
    [165, 350],
    { hdrBg: C.ORANGE, altBg: C.ORANGE_LIGHT }
  );
}

// ─── Back Cover ────────────────────────────────────────────────────────────
function buildBackCover() {
  newPage();
  filledRect(MARGIN, MARGIN, CONTENT_W, 280, C.BG_DARK, 8);
  doc.circle(MARGIN + 40, MARGIN + 240, 55).fill("#0D47A1");
  doc.circle(MARGIN + CONTENT_W - 20, MARGIN + 40, 70).fill("#1B5E20");

  doc.fontSize(22).font("Helvetica-Bold").fillColor(C.WHITE)
     .text("Keep building. Keep shipping.", MARGIN, MARGIN + 90,
       { align: "center", width: CONTENT_W });

  doc.fontSize(11).font("Helvetica-Oblique").fillColor("#90CAF9")
     .text("Every expert was once a beginner who refused to give up.",
       MARGIN, MARGIN + 120, { align: "center", width: CONTENT_W });

  doc.fontSize(11).font("Helvetica-Bold").fillColor(C.YELLOW)
     .text("Your next 5 steps:", MARGIN + 60, MARGIN + 155);

  const nexts = [
    "1.  Fix the port mismatch:  EXPOSE 8081 in your Dockerfile",
    "2.  Add a .gitignore to your project",
    "3.  Create your first feature branch",
    "4.  Build and run your Docker container: docker run -p 3000:8081 demo-nodejs",
    "5.  Push your first Pull Request on GitHub",
  ];
  nexts.forEach((item, i) => {
    doc.fontSize(10).font("Helvetica").fillColor(C.WHITE)
       .text(item, MARGIN + 60, MARGIN + 175 + i * 18);
  });

  doc.fontSize(8).font("Helvetica").fillColor(C.COMMENT)
     .text(
       "Muhammad Arham's DevOps Guide  •  demo_nodejs_webpage  •  2026",
       MARGIN, MARGIN + 260, { align: "center", width: CONTENT_W }
     );
}

// ─── Build Everything ──────────────────────────────────────────────────────
buildCover();
addPageFooter();
buildTOC();
buildBigPicture();
buildGit();
buildBranching();
buildDockerConcepts();
buildDockerfile();
buildErrors();
buildCheatSheets();
buildBackCover();

doc.end();

stream.on("finish", () => {
  const size = (fs.statSync(outputPath).size / 1024).toFixed(1);
  console.log(`\n✓ PDF generated successfully!`);
  console.log(`  File: ${outputPath}`);
  console.log(`  Size: ${size} KB`);
});

stream.on("error", (err) => {
  console.error("PDF generation failed:", err);
  process.exit(1);
});
