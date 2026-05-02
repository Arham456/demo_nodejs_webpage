"""
DevOps Guide PDF Generator for Muhammad Arham
Generates a comprehensive, beginner-friendly DevOps guide based on his actual Node.js project.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.platypus.flowables import Flowable
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Arrow, Circle, Polygon
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Group
import os

# ─── Color Palette ────────────────────────────────────────────────────────────
C_BG_DARK     = colors.HexColor("#0D1117")   # GitHub-like dark
C_BLUE        = colors.HexColor("#2196F3")
C_BLUE_DARK   = colors.HexColor("#1565C0")
C_BLUE_LIGHT  = colors.HexColor("#E3F2FD")
C_GREEN       = colors.HexColor("#4CAF50")
C_GREEN_DARK  = colors.HexColor("#2E7D32")
C_GREEN_LIGHT = colors.HexColor("#E8F5E9")
C_ORANGE      = colors.HexColor("#FF9800")
C_ORANGE_LIGHT= colors.HexColor("#FFF3E0")
C_RED         = colors.HexColor("#F44336")
C_RED_LIGHT   = colors.HexColor("#FFEBEE")
C_PURPLE      = colors.HexColor("#9C27B0")
C_PURPLE_LIGHT= colors.HexColor("#F3E5F5")
C_CYAN        = colors.HexColor("#00BCD4")
C_CYAN_LIGHT  = colors.HexColor("#E0F7FA")
C_YELLOW      = colors.HexColor("#FFC107")
C_YELLOW_LIGHT= colors.HexColor("#FFFDE7")
C_GRAY        = colors.HexColor("#607D8B")
C_GRAY_LIGHT  = colors.HexColor("#ECEFF1")
C_GRAY_DARK   = colors.HexColor("#37474F")
C_WHITE       = colors.white
C_BLACK       = colors.HexColor("#212121")

PAGE_W, PAGE_H = A4

# ─── Styles ───────────────────────────────────────────────────────────────────
def build_styles():
    base = getSampleStyleSheet()
    styles = {}

    styles["title"] = ParagraphStyle(
        "title", parent=base["Title"],
        fontSize=28, textColor=C_WHITE, alignment=TA_CENTER,
        spaceAfter=6, fontName="Helvetica-Bold", leading=34
    )
    styles["subtitle"] = ParagraphStyle(
        "subtitle", parent=base["Normal"],
        fontSize=13, textColor=colors.HexColor("#90CAF9"),
        alignment=TA_CENTER, spaceAfter=4, fontName="Helvetica"
    )
    styles["h1"] = ParagraphStyle(
        "h1", parent=base["Heading1"],
        fontSize=20, textColor=C_WHITE, fontName="Helvetica-Bold",
        spaceBefore=6, spaceAfter=10, leading=26,
        backColor=C_BLUE_DARK, borderPad=8
    )
    styles["h2"] = ParagraphStyle(
        "h2", parent=base["Heading2"],
        fontSize=15, textColor=C_BLUE_DARK, fontName="Helvetica-Bold",
        spaceBefore=14, spaceAfter=6, leading=20,
        borderColor=C_BLUE, borderWidth=0, leftIndent=0
    )
    styles["h3"] = ParagraphStyle(
        "h3", parent=base["Heading3"],
        fontSize=12, textColor=C_GRAY_DARK, fontName="Helvetica-Bold",
        spaceBefore=10, spaceAfter=4, leading=16
    )
    styles["body"] = ParagraphStyle(
        "body", parent=base["Normal"],
        fontSize=10, textColor=C_BLACK, fontName="Helvetica",
        spaceBefore=2, spaceAfter=4, leading=15, alignment=TA_JUSTIFY
    )
    styles["body_center"] = ParagraphStyle(
        "body_center", parent=base["Normal"],
        fontSize=10, textColor=C_BLACK, fontName="Helvetica",
        spaceBefore=2, spaceAfter=4, leading=15, alignment=TA_CENTER
    )
    styles["code"] = ParagraphStyle(
        "code", parent=base["Code"],
        fontSize=9, fontName="Courier", textColor=colors.HexColor("#E0E0E0"),
        backColor=colors.HexColor("#1E2A38"), borderPad=8,
        spaceBefore=2, spaceAfter=2, leading=14, leftIndent=4
    )
    styles["code_good"] = ParagraphStyle(
        "code_good", parent=base["Code"],
        fontSize=9, fontName="Courier", textColor=colors.HexColor("#C8E6C9"),
        backColor=colors.HexColor("#1B3A2D"), borderPad=8,
        spaceBefore=2, spaceAfter=2, leading=14, leftIndent=4
    )
    styles["code_bad"] = ParagraphStyle(
        "code_bad", parent=base["Code"],
        fontSize=9, fontName="Courier", textColor=colors.HexColor("#FFCDD2"),
        backColor=colors.HexColor("#3B1F1F"), borderPad=8,
        spaceBefore=2, spaceAfter=2, leading=14, leftIndent=4
    )
    styles["tip"] = ParagraphStyle(
        "tip", parent=base["Normal"],
        fontSize=9.5, textColor=colors.HexColor("#1A237E"), fontName="Helvetica",
        backColor=C_BLUE_LIGHT, borderPad=8,
        leftIndent=10, rightIndent=10, spaceBefore=6, spaceAfter=6, leading=14
    )
    styles["warning"] = ParagraphStyle(
        "warning", parent=base["Normal"],
        fontSize=9.5, textColor=colors.HexColor("#BF360C"), fontName="Helvetica",
        backColor=C_ORANGE_LIGHT, borderPad=8,
        leftIndent=10, rightIndent=10, spaceBefore=6, spaceAfter=6, leading=14
    )
    styles["success"] = ParagraphStyle(
        "success", parent=base["Normal"],
        fontSize=9.5, textColor=colors.HexColor("#1B5E20"), fontName="Helvetica",
        backColor=C_GREEN_LIGHT, borderPad=8,
        leftIndent=10, rightIndent=10, spaceBefore=6, spaceAfter=6, leading=14
    )
    styles["error"] = ParagraphStyle(
        "error", parent=base["Normal"],
        fontSize=9.5, textColor=colors.HexColor("#B71C1C"), fontName="Helvetica",
        backColor=C_RED_LIGHT, borderPad=8,
        leftIndent=10, rightIndent=10, spaceBefore=6, spaceAfter=6, leading=14
    )
    styles["label"] = ParagraphStyle(
        "label", parent=base["Normal"],
        fontSize=8, textColor=C_GRAY, fontName="Helvetica",
        alignment=TA_CENTER, spaceBefore=0, spaceAfter=2
    )
    styles["toc_entry"] = ParagraphStyle(
        "toc_entry", parent=base["Normal"],
        fontSize=11, textColor=C_BLUE_DARK, fontName="Helvetica",
        spaceBefore=4, spaceAfter=4, leftIndent=20, leading=16
    )
    return styles

S = build_styles()

# ─── Helper Flowables ─────────────────────────────────────────────────────────
def hline(color=C_BLUE, thickness=1.5):
    return HRFlowable(width="100%", thickness=thickness, color=color, spaceAfter=6, spaceBefore=6)

def vspace(h=8):
    return Spacer(1, h)

def section_header(text, icon=""):
    d = Drawing(PAGE_W - 4*cm, 36)
    d.add(Rect(0, 0, PAGE_W - 4*cm, 36, fillColor=C_BLUE_DARK, strokeColor=None))
    d.add(String(14, 12, f"{icon}  {text}" if icon else text,
                 fontSize=16, fillColor=C_WHITE, fontName="Helvetica-Bold"))
    return d

def mini_header(text, color=C_BLUE_DARK):
    d = Drawing(PAGE_W - 4*cm, 26)
    d.add(Rect(0, 0, PAGE_W - 4*cm, 26, fillColor=color, strokeColor=None))
    d.add(String(10, 8, text, fontSize=12, fillColor=C_WHITE, fontName="Helvetica-Bold"))
    return d

def badge(text, bg=C_BLUE, fg=C_WHITE, width=120, height=22):
    d = Drawing(width, height)
    d.add(Rect(0, 0, width, height, fillColor=bg, strokeColor=None, rx=4, ry=4))
    d.add(String(width/2, 6, text, fontSize=9, fillColor=fg,
                 fontName="Helvetica-Bold", textAnchor="middle"))
    return d

# ─── Cover Page ───────────────────────────────────────────────────────────────
def cover_page(story):
    # Big dark background banner
    d = Drawing(PAGE_W - 4*cm, 220)
    d.add(Rect(0, 0, PAGE_W - 4*cm, 220, fillColor=C_BG_DARK, strokeColor=None))
    # Decorative circles
    d.add(Circle(30, 190, 50, fillColor=colors.HexColor("#1565C0"), strokeColor=None))
    d.add(Circle(PAGE_W - 4*cm - 20, 30, 70, fillColor=colors.HexColor("#1B5E20"), strokeColor=None))
    d.add(Circle((PAGE_W - 4*cm)//2, 110, 120,
                 fillColor=colors.HexColor("#0D47A1"), strokeColor=None))
    # Title
    d.add(String((PAGE_W - 4*cm)/2, 140, "DevOps Learning Guide",
                 fontSize=30, fillColor=C_WHITE, fontName="Helvetica-Bold", textAnchor="middle"))
    d.add(String((PAGE_W - 4*cm)/2, 110, "Muhammad Arham's Personal Handbook",
                 fontSize=14, fillColor=colors.HexColor("#90CAF9"),
                 fontName="Helvetica", textAnchor="middle"))
    d.add(String((PAGE_W - 4*cm)/2, 80, "Git  |  Docker  |  Node.js  |  GitHub Flow",
                 fontSize=11, fillColor=colors.HexColor("#64B5F6"),
                 fontName="Helvetica", textAnchor="middle"))
    d.add(String((PAGE_W - 4*cm)/2, 48, "From Zero to Deploying with Confidence",
                 fontSize=10, fillColor=colors.HexColor("#B0BEC5"),
                 fontName="Helvetica-Oblique", textAnchor="middle"))
    story.append(d)
    story.append(vspace(10))

    # Workflow pills row
    workflow = Drawing(PAGE_W - 4*cm, 50)
    items = [("GitHub", C_GRAY_DARK, 60), ("VS Code", C_BLUE_DARK, 220),
             ("Docker", C_GREEN_DARK, 380), ("Ship!", C_ORANGE, 510)]
    for label, col, x in items:
        workflow.add(Rect(x, 10, 100, 30, fillColor=col, strokeColor=None, rx=6, ry=6))
        workflow.add(String(x+50, 20, label, fontSize=11, fillColor=C_WHITE,
                            fontName="Helvetica-Bold", textAnchor="middle"))
    # Arrows between pills
    for ax in [168, 328, 488]:
        workflow.add(String(ax, 20, "→", fontSize=14, fillColor=C_GRAY,
                            fontName="Helvetica-Bold", textAnchor="middle"))
    story.append(workflow)
    story.append(vspace(16))
    story.append(Paragraph(
        "<b>Based on your actual project:</b> demo_nodejs_webpage &nbsp;|&nbsp; "
        "Node.js + Express + Docker &nbsp;|&nbsp; Generated 2026-04-26",
        S["body_center"]
    ))


# ─── Table of Contents ────────────────────────────────────────────────────────
def toc_page(story):
    story.append(PageBreak())
    story.append(section_header("Table of Contents", ""))
    story.append(vspace(12))
    toc = [
        ("1", "The Big Picture — Your Workflow", "3"),
        ("2", "Git Fundamentals & Daily Commands", "5"),
        ("3", "Branching Strategies", "9"),
        ("4", "Docker: Images vs Containers", "12"),
        ("5", "Your Dockerfile — Line by Line", "15"),
        ("6", "Common Errors & Fixes", "18"),
        ("7", "Cheat Sheets", "22"),
    ]
    for num, title, page in toc:
        data = [[
            Paragraph(f"<b>{num}</b>", S["body_center"]),
            Paragraph(title, S["body"]),
            Paragraph(page, S["body_center"]),
        ]]
        t = Table(data, colWidths=[1.2*cm, 12*cm, 1.5*cm])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (0,0), C_BLUE_DARK),
            ("TEXTCOLOR",  (0,0), (0,0), C_WHITE),
            ("BACKGROUND", (1,0), (1,0), C_GRAY_LIGHT),
            ("BACKGROUND", (2,0), (2,0), C_BLUE_LIGHT),
            ("ALIGN",      (0,0), (-1,-1), "CENTER"),
            ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
            ("ROWBACKGROUND", (0,0), (-1,-1), [C_GRAY_LIGHT, C_WHITE]),
            ("TOPPADDING",  (0,0), (-1,-1), 8),
            ("BOTTOMPADDING",(0,0), (-1,-1), 8),
            ("GRID",       (0,0), (-1,-1), 0.5, colors.HexColor("#CFD8DC")),
            ("ROUNDEDCORNERS", (0,0), (-1,-1), [4]),
        ]))
        story.append(t)
        story.append(vspace(4))


# ─── Section 1: Big Picture ───────────────────────────────────────────────────
def section_bigpicture(story):
    story.append(PageBreak())
    story.append(section_header("Section 1 — The Big Picture: Your Workflow", ""))
    story.append(vspace(8))

    story.append(Paragraph(
        "Before diving into commands, understand <b>WHY</b> each tool exists and how they connect. "
        "Here is your complete daily workflow as a DevOps learner:",
        S["body"]
    ))
    story.append(vspace(10))

    # Workflow diagram
    d = Drawing(PAGE_W - 4*cm, 160)
    boxes = [
        ("Your\nBrain", 20,  50, C_PURPLE,     "Idea / Feature\nrequest"),
        ("VS Code",     155, 50, C_BLUE_DARK,  "Write code\nEdit files"),
        ("Git",         290, 50, C_GRAY_DARK,  "Track changes\ngit add/commit"),
        ("GitHub",      425, 50, colors.HexColor("#24292E"), "Share code\nPull requests"),
        ("Docker",      540, 50, C_GREEN_DARK, "Package &\nRun app"),
    ]
    bw, bh = 100, 60
    for label, x, y, col, sub in boxes:
        d.add(Rect(x, y, bw, bh, fillColor=col, strokeColor=C_WHITE, strokeWidth=1, rx=6, ry=6))
        lines = label.split("\n")
        cy = y + bh - 12 - (len(lines)-1)*12
        for i, line in enumerate(lines):
            d.add(String(x+bw/2, cy+i*14, line, fontSize=10, fillColor=C_WHITE,
                         fontName="Helvetica-Bold", textAnchor="middle"))
        sub_lines = sub.split("\n")
        for i, line in enumerate(sub_lines):
            d.add(String(x+bw/2, y+4+i*10, line, fontSize=7.5,
                         fillColor=colors.HexColor("#EEEEEE"),
                         fontName="Helvetica", textAnchor="middle"))

    # Arrows
    arrow_positions = [(120, 80), (255, 80), (390, 80), (525+15, 80)]
    for ax, ay in arrow_positions:
        d.add(String(ax, ay-6, "→", fontSize=18, fillColor=C_YELLOW,
                     fontName="Helvetica-Bold", textAnchor="middle"))

    # Feedback arrow (bottom)
    d.add(Line(590, 50, 590, 20, strokeColor=C_CYAN, strokeWidth=2))
    d.add(Line(590, 20, 70,  20, strokeColor=C_CYAN, strokeWidth=2))
    d.add(Line(70,  20, 70,  50, strokeColor=C_CYAN, strokeWidth=2))
    d.add(String(330, 6, "Feedback loop: iterate and improve", fontSize=8,
                 fillColor=C_CYAN, fontName="Helvetica-Oblique", textAnchor="middle"))
    story.append(d)
    story.append(vspace(8))

    # Step-by-step table
    story.append(Paragraph("Step-by-Step: What You Do Each Day", S["h2"]))
    steps = [
        ["Step", "Tool", "What You Do", "Result"],
        ["1", "VS Code", "Open project, edit app.js or HTML files", "New code written"],
        ["2", "Terminal", "git add . && git commit -m 'message'", "Change saved to history"],
        ["3", "Terminal", "git push origin main", "Code backed up on GitHub"],
        ["4", "Terminal", "docker build -t myapp .", "Docker image created"],
        ["5", "Terminal", "docker run -p 3000:8081 myapp", "App running in container"],
        ["6", "Browser", "Visit http://localhost:3000", "You see your webpage!"],
    ]
    t = Table(steps, colWidths=[1.2*cm, 2.5*cm, 8*cm, 4*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0),  C_BLUE_DARK),
        ("TEXTCOLOR",     (0,0), (-1,0),  C_WHITE),
        ("FONTNAME",      (0,0), (-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,0),  9),
        ("FONTNAME",      (0,1), (-1,-1), "Courier"),
        ("FONTSIZE",      (0,1), (-1,-1), 8.5),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [C_WHITE, C_GRAY_LIGHT]),
        ("GRID",          (0,0), (-1,-1), 0.5, colors.HexColor("#CFD8DC")),
        ("ALIGN",         (0,0), (1,-1),  "CENTER"),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
    ]))
    story.append(t)
    story.append(vspace(10))

    story.append(Paragraph("Your Project Structure", S["h2"]))
    story.append(vspace(4))

    # File tree diagram
    d2 = Drawing(PAGE_W - 4*cm, 180)
    d2.add(Rect(0, 0, PAGE_W - 4*cm, 180, fillColor=C_BG_DARK, strokeColor=None, rx=6, ry=6))
    tree = [
        (10,  "demo_nodejs_webpage/           ← Your project root",    C_YELLOW),
        (30,  "├── app.js                     ← Main Express server",  C_CYAN),
        (30,  "├── package.json               ← Dependencies & scripts",C_GREEN),
        (30,  "├── Dockerfile                 ← Docker build recipe",  C_ORANGE),
        (30,  "├── index.html                 ← Homepage",             C_WHITE),
        (30,  "├── about.html                 ← About page",           C_WHITE),
        (30,  "├── routes/                    ← Express route handlers",C_PURPLE),
        (50,  "│   └── tasks.js",                                       colors.HexColor("#CE93D8")),
        (30,  "└── data/                      ← Data layer",           C_PURPLE),
        (50,  "    └── task.js",                                        colors.HexColor("#CE93D8")),
    ]
    y = 155
    for indent, text, col in tree:
        d2.add(String(indent, y, text, fontSize=8.5, fillColor=col,
                      fontName="Courier", textAnchor="start"))
        y -= 16
    story.append(d2)

    story.append(vspace(10))
    story.append(Paragraph(
        "⚠️  <b>Important note spotted in YOUR project:</b> "
        "Your <i>app.js</i> listens on port <b>8081</b>, but your <i>Dockerfile</i> says "
        "<b>EXPOSE 3000</b>. This means Docker documents port 3000 but your app actually "
        "uses 8081. When running the container you need: "
        "<b>docker run -p 3000:8081 myapp</b>. "
        "We cover this in the Common Errors section.",
        S["warning"]
    ))


# ─── Section 2: Git Commands ──────────────────────────────────────────────────
def section_git(story):
    story.append(PageBreak())
    story.append(section_header("Section 2 — Git Fundamentals & Daily Commands", ""))
    story.append(vspace(8))

    story.append(Paragraph(
        "Git is a <b>version control system</b> — it keeps a complete history of every "
        "change you make, so you can always go back, compare, or share your work.",
        S["body"]
    ))
    story.append(vspace(8))

    # Git mental model diagram
    story.append(Paragraph("The Git Mental Model — 4 Zones", S["h2"]))
    d = Drawing(PAGE_W - 4*cm, 100)
    zones = [
        ("Working\nDirectory", 10,  10, 115, 80, C_RED_LIGHT,    colors.HexColor("#B71C1C")),
        ("Staging\nArea",      140, 10, 115, 80, C_YELLOW_LIGHT, colors.HexColor("#E65100")),
        ("Local\nRepo",        270, 10, 115, 80, C_GREEN_LIGHT,  C_GREEN_DARK),
        ("Remote\n(GitHub)",   400, 10, 115, 80, C_BLUE_LIGHT,   C_BLUE_DARK),
    ]
    for label, x, y, w, h, bg, fg in zones:
        d.add(Rect(x, y, w, h, fillColor=bg, strokeColor=fg, strokeWidth=1.5, rx=4, ry=4))
        for i, line in enumerate(label.split("\n")):
            d.add(String(x+w/2, y+h-22-i*14, line, fontSize=10, fillColor=fg,
                         fontName="Helvetica-Bold", textAnchor="middle"))

    cmds = [("git add", 130, 55), ("git commit", 262, 55), ("git push", 393, 55)]
    for cmd, cx, cy in cmds:
        d.add(String(cx, cy, "→", fontSize=16, fillColor=C_GRAY,
                     fontName="Helvetica-Bold", textAnchor="middle"))
        d.add(String(cx, cy-14, cmd, fontSize=7, fillColor=C_GRAY,
                     fontName="Courier", textAnchor="middle"))
    story.append(d)
    story.append(vspace(4))
    story.append(Paragraph(
        "Files live in your <b>Working Directory</b>. You <b>stage</b> selected changes, "
        "<b>commit</b> them to local history, then <b>push</b> to share on GitHub.",
        S["tip"]
    ))
    story.append(vspace(10))

    # Command reference table
    story.append(Paragraph("Daily Git Commands Reference", S["h2"]))
    cmd_data = [
        ["Command", "What it does", "Example"],
        ["git init", "Create a new Git repo in current folder",
         "git init"],
        ["git status", "See what's changed / staged",
         "git status"],
        ["git add <file>", "Stage a specific file",
         "git add app.js"],
        ["git add .", "Stage ALL changed files",
         "git add ."],
        ["git commit -m", "Save staged changes with a message",
         'git commit -m "add about page"'],
        ["git log --oneline", "See compact commit history",
         "git log --oneline"],
        ["git diff", "See unstaged changes line by line",
         "git diff app.js"],
        ["git push origin main", "Upload commits to GitHub",
         "git push origin main"],
        ["git pull origin main", "Download latest from GitHub",
         "git pull origin main"],
        ["git clone <url>", "Download a repo from GitHub",
         "git clone https://github.com/user/repo.git"],
        ["git branch", "List all branches",
         "git branch"],
        ["git checkout -b", "Create & switch to new branch",
         "git checkout -b feature/login"],
        ["git merge <branch>", "Merge a branch into current",
         "git merge feature/login"],
        ["git stash", "Temporarily save uncommitted work",
         "git stash"],
        ["git stash pop", "Restore stashed work",
         "git stash pop"],
    ]
    t = Table(cmd_data, colWidths=[4*cm, 6.5*cm, 6*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0),  C_BLUE_DARK),
        ("TEXTCOLOR",     (0,0), (-1,0),  C_WHITE),
        ("FONTNAME",      (0,0), (-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,0),  9),
        ("FONTNAME",      (0,1), (0,-1),  "Courier"),
        ("FONTSIZE",      (0,1), (-1,-1), 8.5),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [C_WHITE, C_GRAY_LIGHT]),
        ("GRID",          (0,0), (-1,-1), 0.5, colors.HexColor("#CFD8DC")),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ("FONTNAME",      (2,1), (2,-1),  "Courier"),
        ("TEXTCOLOR",     (2,1), (2,-1),  colors.HexColor("#1A237E")),
    ]))
    story.append(t)
    story.append(vspace(10))

    # Good vs Bad commit messages
    story.append(Paragraph("Good vs Bad Commit Messages", S["h2"]))
    story.append(vspace(4))
    compare = [
        [Paragraph("<b>BAD (avoid these)</b>", S["body_center"]),
         Paragraph("<b>GOOD (use these)</b>",  S["body_center"])],
        [Paragraph('<font color="#B71C1C" name="Courier">git commit -m "fix"</font>', S["body"]),
         Paragraph('<font color="#2E7D32" name="Courier">git commit -m "fix port mismatch in Dockerfile"</font>', S["body"])],
        [Paragraph('<font color="#B71C1C" name="Courier">git commit -m "changes"</font>', S["body"]),
         Paragraph('<font color="#2E7D32" name="Courier">git commit -m "add /about route to app.js"</font>', S["body"])],
        [Paragraph('<font color="#B71C1C" name="Courier">git commit -m "asdf"</font>', S["body"]),
         Paragraph('<font color="#2E7D32" name="Courier">git commit -m "update package.json description"</font>', S["body"])],
        [Paragraph('<font color="#B71C1C" name="Courier">git commit -m "wip"</font>', S["body"]),
         Paragraph('<font color="#2E7D32" name="Courier">git commit -m "work in progress: adding task routes"</font>', S["body"])],
    ]
    t2 = Table(compare, colWidths=[8.5*cm, 8.5*cm])
    t2.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (0,0),  C_RED_LIGHT),
        ("BACKGROUND",    (1,0), (1,0),  C_GREEN_LIGHT),
        ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
        ("GRID",          (0,0), (-1,-1), 0.5, colors.HexColor("#CFD8DC")),
        ("ROWBACKGROUNDS",(0,1), (0,-1), [C_WHITE, C_RED_LIGHT]),
        ("ROWBACKGROUNDS",(1,1), (1,-1), [C_WHITE, C_GREEN_LIGHT]),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]))
    story.append(t2)
    story.append(vspace(6))
    story.append(Paragraph(
        "Rule: A good commit message completes the sentence "
        "<i>\"If applied, this commit will...\"</i>",
        S["tip"]
    ))

    # Real workflow with YOUR project
    story.append(vspace(10))
    story.append(Paragraph("Real Workflow Using YOUR Project", S["h2"]))
    story.append(vspace(4))
    workflow_code = [
        "# You just edited app.js to add a new route",
        "",
        "git status                        # see: modified app.js",
        "git diff app.js                   # review your changes",
        "git add app.js                    # stage just that file",
        'git commit -m "add /contact route to Express app"',
        "git push origin main              # send to GitHub",
        "",
        "# Later, pull changes from GitHub (e.g., edited on another machine)",
        "git pull origin main",
    ]
    for line in workflow_code:
        style = S["code"] if line and not line.startswith("#") else ParagraphStyle(
            "comment", parent=S["code"],
            textColor=colors.HexColor("#78909C")
        )
        story.append(Paragraph(line if line else "&nbsp;", style))
    story.append(vspace(4))


# ─── Section 3: Branching Strategies ─────────────────────────────────────────
def section_branching(story):
    story.append(PageBreak())
    story.append(section_header("Section 3 — Branching Strategies", ""))
    story.append(vspace(8))

    story.append(Paragraph(
        "A <b>branch</b> is an independent copy of your code where you can make changes "
        "without affecting the main, working version. Think of it like a parallel universe "
        "for your code.",
        S["body"]
    ))
    story.append(vspace(8))

    # Branch concept diagram
    story.append(Paragraph("What a Branch Looks Like", S["h2"]))
    d = Drawing(PAGE_W - 4*cm, 120)
    # main branch line
    d.add(Line(20, 80, PAGE_W - 4*cm - 20, 80, strokeColor=C_BLUE_DARK, strokeWidth=3))
    # commits on main
    main_commits = [(20, "C1"), (100, "C2"), (200, "C3"), (460, "C7"), (PAGE_W-4*cm-20, "C8")]
    for cx, label in main_commits:
        d.add(Circle(cx, 80, 12, fillColor=C_BLUE_DARK, strokeColor=C_WHITE, strokeWidth=1))
        d.add(String(cx, 75, label, fontSize=7, fillColor=C_WHITE,
                     fontName="Helvetica-Bold", textAnchor="middle"))
    # feature branch
    d.add(Line(200, 80, 240, 30, strokeColor=C_GREEN, strokeWidth=2))
    d.add(Line(240, 30, 420, 30, strokeColor=C_GREEN, strokeWidth=3))
    d.add(Line(420, 30, 460, 80, strokeColor=C_GREEN, strokeWidth=2))
    feat_commits = [(260, "C4"), (320, "C5"), (380, "C6")]
    for cx, label in feat_commits:
        d.add(Circle(cx, 30, 12, fillColor=C_GREEN, strokeColor=C_WHITE, strokeWidth=1))
        d.add(String(cx, 25, label, fontSize=7, fillColor=C_WHITE,
                     fontName="Helvetica-Bold", textAnchor="middle"))
    # Labels
    d.add(String(30, 95, "main branch", fontSize=9, fillColor=C_BLUE_DARK,
                 fontName="Helvetica-Bold"))
    d.add(String(290, 14, "feature/add-contact-form branch", fontSize=9,
                 fillColor=C_GREEN_DARK, fontName="Helvetica-Bold"))
    d.add(String(470, 85, "merge", fontSize=8, fillColor=C_GRAY,
                 fontName="Helvetica-Oblique"))
    story.append(d)
    story.append(vspace(6))
    story.append(Paragraph(
        "The <b>main</b> branch always stays working. You create a feature branch, "
        "do your work there, then <b>merge</b> it back when done.",
        S["tip"]
    ))
    story.append(vspace(12))

    # GitHub Flow
    story.append(Paragraph("GitHub Flow (Recommended for Beginners)", S["h2"]))
    story.append(vspace(4))
    story.append(Paragraph(
        "GitHub Flow is a simple, 6-step process. It's what you should use for your project:",
        S["body"]
    ))
    story.append(vspace(6))

    steps = [
        ("1", "Create branch", 'git checkout -b feature/new-route', C_PURPLE),
        ("2", "Make changes",  "Edit app.js, add your new feature",  C_BLUE_DARK),
        ("3", "Commit often",  'git add . && git commit -m "add route"', C_CYAN),
        ("4", "Push branch",   "git push origin feature/new-route",  C_GREEN_DARK),
        ("5", "Open PR",       "On GitHub: compare & pull request",   C_ORANGE),
        ("6", "Merge & delete","Merge PR, delete branch on GitHub",   C_RED),
    ]
    for num, title, cmd, col in steps:
        row_data = [[
            Paragraph(f"<b>{num}</b>", S["body_center"]),
            Paragraph(f"<b>{title}</b>", S["body"]),
            Paragraph(f'<font name="Courier" size="9">{cmd}</font>', S["body"]),
        ]]
        t = Table(row_data, colWidths=[1*cm, 4*cm, 11*cm])
        t.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (0,0), col),
            ("TEXTCOLOR",     (0,0), (0,0), C_WHITE),
            ("BACKGROUND",    (1,0), (1,0), C_GRAY_LIGHT),
            ("BACKGROUND",    (2,0), (2,0), C_WHITE),
            ("GRID",          (0,0), (-1,-1), 0.5, colors.HexColor("#CFD8DC")),
            ("ALIGN",         (0,0), (0,0),  "CENTER"),
            ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
            ("TOPPADDING",    (0,0), (-1,-1), 7),
            ("BOTTOMPADDING", (0,0), (-1,-1), 7),
            ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ]))
        story.append(t)
        story.append(vspace(3))

    story.append(vspace(10))

    # Git Flow vs GitHub Flow comparison
    story.append(Paragraph("GitHub Flow vs Git Flow — Side-by-Side", S["h2"]))
    story.append(vspace(4))
    compare = [
        [Paragraph("<b>GitHub Flow</b>  (simple)", S["body_center"]),
         Paragraph("<b>Git Flow</b>  (complex)", S["body_center"])],
        [Paragraph("2 key branches: main + feature/*", S["body"]),
         Paragraph("5 branch types: main, develop, feature, release, hotfix", S["body"])],
        [Paragraph("Deploy directly from main", S["body"]),
         Paragraph("Deploy from release branches only", S["body"])],
        [Paragraph("Great for: small teams, web apps, beginners", S["body"]),
         Paragraph("Great for: large teams, versioned software", S["body"])],
        [Paragraph("Your demo project: USE THIS", S["success"]),
         Paragraph("Learn this later when working in teams", S["tip"])],
    ]
    t2 = Table(compare, colWidths=[8.5*cm, 8.5*cm])
    t2.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (0,0), C_GREEN_LIGHT),
        ("BACKGROUND",    (1,0), (1,0), C_BLUE_LIGHT),
        ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
        ("GRID",          (0,0), (-1,-1), 0.5, colors.HexColor("#CFD8DC")),
        ("ROWBACKGROUNDS",(0,1), (0,-1), [C_WHITE, C_GREEN_LIGHT]),
        ("ROWBACKGROUNDS",(1,1), (1,-1), [C_WHITE, C_BLUE_LIGHT]),
        ("TOPPADDING",    (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]))
    story.append(t2)

    story.append(vspace(10))
    story.append(Paragraph("Branch Naming Conventions", S["h2"]))
    naming_data = [
        ["Branch Type", "Pattern", "Example for YOUR project"],
        ["Feature",    "feature/<description>",  "feature/add-contact-page"],
        ["Bug fix",    "fix/<description>",       "fix/port-mismatch-dockerfile"],
        ["Hotfix",     "hotfix/<description>",    "hotfix/app-crash-on-startup"],
        ["Docs",       "docs/<description>",      "docs/add-readme"],
        ["Refactor",   "refactor/<description>",  "refactor/split-routes"],
    ]
    t3 = Table(naming_data, colWidths=[3*cm, 5*cm, 8.5*cm])
    t3.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0),  C_GRAY_DARK),
        ("TEXTCOLOR",     (0,0), (-1,0),  C_WHITE),
        ("FONTNAME",      (0,0), (-1,0),  "Helvetica-Bold"),
        ("FONTNAME",      (0,1), (-1,-1), "Courier"),
        ("FONTSIZE",      (0,0), (-1,-1), 9),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [C_WHITE, C_GRAY_LIGHT]),
        ("GRID",          (0,0), (-1,-1), 0.5, colors.HexColor("#CFD8DC")),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]))
    story.append(t3)


# ─── Section 4: Docker Concepts ───────────────────────────────────────────────
def section_docker_concepts(story):
    story.append(PageBreak())
    story.append(section_header("Section 4 — Docker: Images vs Containers", ""))
    story.append(vspace(8))

    story.append(Paragraph(
        "Docker solves the classic problem: <i>\"It works on my machine!\"</i> "
        "It packages your app with EVERYTHING it needs — Node.js, dependencies, config — "
        "into a single unit that runs identically everywhere.",
        S["body"]
    ))
    story.append(vspace(10))

    # Analogy table
    story.append(Paragraph("The Analogy That Makes Docker Click", S["h2"]))
    analogy = [
        ["Real World",       "Docker Equivalent", "In Your Project"],
        ["Cookie recipe",    "Dockerfile",         "Your Dockerfile file"],
        ["Cookie cutter",    "Image",              "node:alpine + your app code"],
        ["Actual cookie",    "Container",          "Running instance of your app"],
        ["Multiple cookies", "Multiple containers","Scale to handle more users"],
    ]
    t = Table(analogy, colWidths=[4.5*cm, 4.5*cm, 7.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0),  C_ORANGE),
        ("TEXTCOLOR",     (0,0), (-1,0),  C_WHITE),
        ("FONTNAME",      (0,0), (-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1), 9),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [C_WHITE, C_ORANGE_LIGHT]),
        ("GRID",          (0,0), (-1,-1), 0.5, colors.HexColor("#FFE0B2")),
        ("TOPPADDING",    (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]))
    story.append(t)
    story.append(vspace(10))

    # Image vs Container diagram
    story.append(Paragraph("Image vs Container — Visual Comparison", S["h2"]))
    d = Drawing(PAGE_W - 4*cm, 160)
    # Image box
    d.add(Rect(20, 20, 210, 130, fillColor=C_BLUE_LIGHT,
               strokeColor=C_BLUE_DARK, strokeWidth=2, rx=8, ry=8))
    d.add(String(125, 136, "IMAGE", fontSize=14, fillColor=C_BLUE_DARK,
                 fontName="Helvetica-Bold", textAnchor="middle"))
    image_layers = [
        ("node:alpine", C_BLUE_DARK, 100),
        ("npm install", C_BLUE,      82),
        ("app.js + HTML", C_BLUE,    64),
        ("package.json", C_BLUE,     46),
    ]
    for label, col, y in image_layers:
        d.add(Rect(35, y, 180, 14, fillColor=col, strokeColor=None, rx=2, ry=2))
        d.add(String(125, y+3, label, fontSize=8, fillColor=C_WHITE,
                     fontName="Courier", textAnchor="middle"))
    d.add(String(125, 28, "READ-ONLY  |  Blueprint", fontSize=8.5,
                 fillColor=C_BLUE_DARK, fontName="Helvetica-Bold", textAnchor="middle"))

    # Arrow
    d.add(String(255, 85, "docker run", fontSize=9, fillColor=C_GRAY,
                 fontName="Courier", textAnchor="middle"))
    d.add(String(255, 72, "────────→", fontSize=12, fillColor=C_GRAY,
                 fontName="Courier", textAnchor="middle"))

    # Container box
    d.add(Rect(290, 20, 210, 130, fillColor=C_GREEN_LIGHT,
               strokeColor=C_GREEN_DARK, strokeWidth=2, rx=8, ry=8))
    d.add(String(395, 136, "CONTAINER", fontSize=14, fillColor=C_GREEN_DARK,
                 fontName="Helvetica-Bold", textAnchor="middle"))
    d.add(Rect(305, 44, 180, 70, fillColor=C_BLUE_LIGHT,
               strokeColor=C_BLUE, strokeWidth=1, rx=3, ry=3))
    d.add(String(395, 106, "Image layers (read-only)", fontSize=8,
                 fillColor=C_BLUE_DARK, fontName="Helvetica", textAnchor="middle"))
    d.add(Rect(305, 46, 180, 66, fillColor=None, strokeColor=None))
    d.add(String(395, 76, "node:alpine + your app", fontSize=7.5,
                 fillColor=C_BLUE_DARK, fontName="Courier", textAnchor="middle"))
    d.add(Rect(305, 28, 180, 14, fillColor=C_GREEN,
               strokeColor=None, rx=2, ry=2))
    d.add(String(395, 32, "Writable layer (runtime state)", fontSize=7.5,
                 fillColor=C_WHITE, fontName="Courier", textAnchor="middle"))
    d.add(String(395, 120, "LIVE  |  Port 8081 exposed", fontSize=8.5,
                 fillColor=C_GREEN_DARK, fontName="Helvetica-Bold", textAnchor="middle"))
    story.append(d)

    story.append(vspace(8))

    # Key Docker commands
    story.append(Paragraph("Essential Docker Commands", S["h2"]))
    docker_cmds = [
        ["Command", "What It Does", "Example"],
        ["docker build -t <name> .",       "Build image from Dockerfile in current folder",
         "docker build -t myapp ."],
        ["docker images",                   "List all images on your machine",
         "docker images"],
        ["docker run -p <host>:<cont> <img>","Start a container from an image",
         "docker run -p 3000:8081 myapp"],
        ["docker ps",                        "List running containers",
         "docker ps"],
        ["docker ps -a",                     "List ALL containers (incl. stopped)",
         "docker ps -a"],
        ["docker stop <id>",                 "Stop a running container",
         "docker stop abc123"],
        ["docker rm <id>",                   "Delete a stopped container",
         "docker rm abc123"],
        ["docker rmi <name>",                "Delete an image",
         "docker rmi myapp"],
        ["docker logs <id>",                 "View container output/logs",
         "docker logs abc123"],
        ["docker exec -it <id> sh",          "Open shell inside container",
         "docker exec -it abc123 sh"],
    ]
    t2 = Table(docker_cmds, colWidths=[5.5*cm, 6*cm, 5*cm])
    t2.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0),  C_GREEN_DARK),
        ("TEXTCOLOR",     (0,0), (-1,0),  C_WHITE),
        ("FONTNAME",      (0,0), (-1,0),  "Helvetica-Bold"),
        ("FONTNAME",      (0,1), (0,-1),  "Courier"),
        ("FONTNAME",      (2,1), (2,-1),  "Courier"),
        ("FONTSIZE",      (0,0), (-1,-1), 8.5),
        ("TEXTCOLOR",     (0,1), (0,-1),  colors.HexColor("#1B5E20")),
        ("TEXTCOLOR",     (2,1), (2,-1),  C_BLUE_DARK),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [C_WHITE, C_GREEN_LIGHT]),
        ("GRID",          (0,0), (-1,-1), 0.5, colors.HexColor("#CFD8DC")),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
    ]))
    story.append(t2)

    story.append(vspace(8))
    story.append(Paragraph(
        "<b>Port mapping</b>  (-p host:container): The LEFT number is what you type "
        "in your browser. The RIGHT is what your app listens on inside the container. "
        "For YOUR project: <b>-p 3000:8081</b> means visit localhost:3000 → hits app on 8081.",
        S["tip"]
    ))


# ─── Section 5: Your Dockerfile Explained ─────────────────────────────────────
def section_dockerfile(story):
    story.append(PageBreak())
    story.append(section_header("Section 5 — Your Dockerfile, Line by Line", ""))
    story.append(vspace(8))

    story.append(Paragraph(
        "A Dockerfile is a recipe — a script Docker follows to build your image. "
        "Here is YOUR actual Dockerfile from <b>demo_nodejs_webpage/</b>, "
        "explained line by line:",
        S["body"]
    ))
    story.append(vspace(10))

    # Dockerfile with annotations
    lines = [
        ("FROM node:alpine",
         "BASE IMAGE",
         C_BLUE_DARK,
         "Start from an official Node.js image built on Alpine Linux (a tiny, secure Linux distro). "
         "This gives you Node.js and npm pre-installed. Alpine keeps the image small (~120MB vs ~900MB for full Ubuntu)."),

        ("WORKDIR /app",
         "WORKING DIR",
         C_GREEN_DARK,
         "Set /app as the working directory inside the container. All subsequent commands run "
         "from here. If /app doesn't exist, Docker creates it automatically."),

        ("COPY package*.json ./",
         "COPY DEPS FIRST",
         C_ORANGE,
         "Copy only package.json (and package-lock.json if present) BEFORE copying all code. "
         "Smart trick: Docker caches this layer. If you only change app.js, npm install "
         "won't re-run — saving minutes of build time!"),

        ("RUN npm install",
         "INSTALL DEPS",
         C_PURPLE,
         "Run npm install to download all dependencies (like Express) listed in package.json. "
         "These get installed into /app/node_modules inside the image."),

        ("COPY . .",
         "COPY ALL CODE",
         C_CYAN,
         "Copy everything from your local project folder into /app in the image. "
         "This includes app.js, index.html, about.html, routes/, data/, etc."),

        ("EXPOSE 3000",
         "DOCUMENT PORT",
         C_RED,
         "Tell Docker (and humans) that the container intends to use port 3000. "
         "NOTE: Your app.js actually listens on 8081 — this is a mismatch! "
         "EXPOSE is just documentation; you fix it at docker run with -p."),

        ('CMD ["npm", "start"]',
         "START COMMAND",
         colors.HexColor("#795548"),
         'The default command to run when the container starts. Runs "npm start" which '
         'executes "node app.js" (as defined in package.json scripts.start). '
         'Use array form ["cmd","arg"] instead of string "cmd arg" for better signal handling.'),
    ]

    for code_line, label, col, explanation in lines:
        # Code line
        d = Drawing(PAGE_W - 4*cm, 28)
        d.add(Rect(0, 0, 2.5*cm, 28, fillColor=col, strokeColor=None))
        d.add(String(1.25*cm, 10, label, fontSize=7, fillColor=C_WHITE,
                     fontName="Helvetica-Bold", textAnchor="middle"))
        d.add(Rect(2.5*cm, 0, PAGE_W - 4*cm - 2.5*cm, 28,
                   fillColor=C_BG_DARK, strokeColor=None))
        d.add(String(2.5*cm + 8, 10, code_line, fontSize=10, fillColor=C_CYAN,
                     fontName="Courier", textAnchor="start"))
        story.append(d)
        story.append(Paragraph(f"    ↑ {explanation}", S["body"]))
        story.append(vspace(6))

    story.append(vspace(8))

    # Full Dockerfile side by side — current vs improved
    story.append(Paragraph("Current Dockerfile vs Improved Version", S["h2"]))
    story.append(vspace(4))

    current = [
        "# YOUR CURRENT Dockerfile",
        "",
        "FROM node:alpine",
        "WORKDIR /app",
        "COPY package*.json ./",
        "RUN npm install",
        "COPY . .",
        "EXPOSE 3000",
        'CMD ["npm", "start"]',
    ]
    improved = [
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
    col1 = [Paragraph(l if l else "&nbsp;", S["code_bad"]) for l in current]
    col2 = [Paragraph(l if l else "&nbsp;", S["code_good"]) for l in improved]
    data = [[Paragraph("<b>Current (has issues)</b>", S["body_center"]),
             Paragraph("<b>Improved version</b>",     S["body_center"])]]
    for a, b in zip(col1, col2):
        data.append([a, b])
    t = Table(data, colWidths=[8.5*cm, 8.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (0,0), C_RED_LIGHT),
        ("BACKGROUND", (1,0), (1,0), C_GREEN_LIGHT),
        ("GRID",       (0,0), (-1,-1), 0.5, colors.HexColor("#CFD8DC")),
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING",(0,0),(-1,-1), 4),
        ("LEFTPADDING",(0,0), (-1,-1), 6),
        ("VALIGN",     (0,0), (-1,-1), "TOP"),
    ]))
    story.append(t)
    story.append(vspace(6))

    improvements = [
        ("<b>node:18-alpine</b> instead of <b>node:alpine</b>: Pin a specific version "
         "so your builds are reproducible. 'alpine' always pulls the latest, which may break."),
        ("<b>npm ci</b> instead of <b>npm install</b>: Faster, stricter, uses package-lock.json. "
         "Ideal for containers and CI pipelines."),
        ("<b>--only=production</b>: Don't install devDependencies in your container. Smaller image."),
        ("<b>EXPOSE 8081</b>: Match what app.js actually uses (port 8081)."),
        ("<b>node app.js</b> directly: Slightly more efficient than 'npm start' in containers."),
    ]
    for imp in improvements:
        story.append(Paragraph(f"• {imp}", S["body"]))
    story.append(vspace(4))


# ─── Section 6: Common Errors ─────────────────────────────────────────────────
def section_errors(story):
    story.append(PageBreak())
    story.append(section_header("Section 6 — Common Errors & Fixes", ""))
    story.append(vspace(8))

    story.append(Paragraph(
        "Every developer hits these. Here are the most common errors you will encounter "
        "in YOUR project workflow, with exact fixes:",
        S["body"]
    ))
    story.append(vspace(10))

    errors = [
        {
            "id": "ERR-01",
            "color": C_RED,
            "title": "Port Mismatch — YOUR project has this right now!",
            "error": "docker run -p 3000:3000 myapp\n# App works but browser shows \"This site can't be reached\"",
            "cause": "app.js listens on 8081, but you mapped -p 3000:3000 (container side wrong).",
            "fix": "docker run -p 3000:8081 myapp\n# OR fix Dockerfile: change EXPOSE 3000 to EXPOSE 8081",
            "why": "The RIGHT side of -p must match the port your app ACTUALLY uses inside the container.",
        },
        {
            "id": "ERR-02",
            "color": C_ORANGE,
            "title": "Git Push Rejected",
            "error": '! [rejected]  main -> main (non-fast-forward)\nerror: failed to push some refs',
            "cause": "Someone else (or you on another machine) pushed commits you don't have locally.",
            "fix": "git pull origin main --rebase\ngit push origin main",
            "why": "Pull first to merge their work, then push your combined history.",
        },
        {
            "id": "ERR-03",
            "color": C_ORANGE,
            "title": "npm not found / Cannot find module 'express'",
            "error": "Error: Cannot find module 'express'\n    at Function.Module._resolveFilename",
            "cause": "Dependencies not installed. node_modules folder is missing.",
            "fix": "npm install\n# Then rebuild Docker image:\ndocker build -t myapp .",
            "why": "node_modules is in .gitignore (correctly). Always run npm install after cloning.",
        },
        {
            "id": "ERR-04",
            "color": C_RED,
            "title": "Merge Conflict",
            "error": "CONFLICT (content): Merge conflict in app.js\nAutomatic merge failed",
            "cause": "Two branches changed the same lines. Git doesn't know which to keep.",
            "fix": "# Open app.js in VS Code, look for <<<<<<< markers\n# Keep the version you want, delete the markers\ngit add app.js\ngit commit -m \"resolve merge conflict in app.js\"",
            "why": "Conflicts are normal — Git is asking you to make the decision it can't.",
        },
        {
            "id": "ERR-05",
            "color": C_ORANGE,
            "title": "Docker: address already in use",
            "error": "Error: bind: address already in use\n... port 3000 already allocated",
            "cause": "Another container (or process) is already using port 3000 on your machine.",
            "fix": "docker ps                  # find running containers\ndocker stop <container_id>  # stop the conflicting one\n# OR use a different host port:\ndocker run -p 3001:8081 myapp",
            "why": "Each port on your machine can only be used by one process at a time.",
        },
        {
            "id": "ERR-06",
            "color": C_GRAY,
            "title": "Git: nothing to commit, working tree clean",
            "error": "nothing to commit, working tree clean",
            "cause": "Not actually an error — just means you have no unsaved changes.",
            "fix": "git status        # check what's happening\ngit log --oneline # verify your last commit is there",
            "why": "This message means everything is saved. Check git log to confirm.",
        },
        {
            "id": "ERR-07",
            "color": C_RED,
            "title": "Docker build fails: COPY failed — file not found",
            "error": "COPY failed: file not found in build context\nor excluded by .dockerignore",
            "cause": "The file you're trying to COPY doesn't exist, or is listed in .dockerignore.",
            "fix": "ls -la             # verify the file exists in your project folder\ncat .dockerignore  # check if the file is excluded\n# Build from the correct directory:\ndocker build -t myapp .   # the dot = current folder!",
            "why": "Docker builds from the 'context' (folder). Always run docker build from project root.",
        },
    ]

    for err in errors:
        # Error header
        d = Drawing(PAGE_W - 4*cm, 28)
        d.add(Rect(0, 0, PAGE_W - 4*cm, 28, fillColor=err["color"], strokeColor=None, rx=4, ry=4))
        d.add(String(10, 10, f"{err['id']}  {err['title']}", fontSize=10,
                     fillColor=C_WHITE, fontName="Helvetica-Bold"))
        story.append(d)

        story.append(Paragraph("<b>Error message:</b>", S["h3"]))
        for line in err["error"].split("\n"):
            story.append(Paragraph(line, S["code_bad"]))

        story.append(Paragraph("<b>Cause:</b>", S["h3"]))
        story.append(Paragraph(err["cause"], S["body"]))

        story.append(Paragraph("<b>Fix:</b>", S["h3"]))
        for line in err["fix"].split("\n"):
            story.append(Paragraph(line, S["code_good"]))

        story.append(Paragraph(f"<b>Why it works:</b> {err['why']}", S["tip"]))
        story.append(vspace(8))
        story.append(hline(color=C_GRAY_LIGHT))
        story.append(vspace(4))


# ─── Section 7: Cheat Sheets ──────────────────────────────────────────────────
def section_cheatsheets(story):
    story.append(PageBreak())
    story.append(section_header("Section 7 — Cheat Sheets", ""))
    story.append(vspace(8))

    # Git Cheat Sheet
    story.append(mini_header("GIT CHEAT SHEET", C_BLUE_DARK))
    story.append(vspace(4))
    git_sheet = [
        ["SETUP",        "git config --global user.name \"Muhammad Arham\"",     "Set your name"],
        ["",             "git config --global user.email \"your@email.com\"",    "Set your email"],
        ["START",        "git init",                                               "New local repo"],
        ["",             "git clone <url>",                                        "Clone from GitHub"],
        ["SNAPSHOT",     "git status",                                             "See changes"],
        ["",             "git add <file>",                                         "Stage a file"],
        ["",             "git add .",                                              "Stage all changes"],
        ["",             "git commit -m \"msg\"",                                  "Save snapshot"],
        ["HISTORY",      "git log --oneline",                                      "Compact history"],
        ["",             "git diff",                                               "Unstaged changes"],
        ["",             "git diff --staged",                                      "Staged changes"],
        ["BRANCHES",     "git branch",                                             "List branches"],
        ["",             "git checkout -b <name>",                                 "New branch"],
        ["",             "git checkout main",                                      "Switch to main"],
        ["",             "git merge <branch>",                                     "Merge branch"],
        ["",             "git branch -d <name>",                                   "Delete branch"],
        ["REMOTE",       "git remote -v",                                          "List remotes"],
        ["",             "git push origin main",                                   "Push to GitHub"],
        ["",             "git pull origin main",                                   "Pull from GitHub"],
        ["UNDO",         "git restore <file>",                                     "Discard changes"],
        ["",             "git reset HEAD~1",                                       "Undo last commit"],
        ["",             "git stash",                                              "Stash changes"],
        ["",             "git stash pop",                                          "Restore stash"],
    ]
    header = [["Category", "Command", "What It Does"]]
    git_data = header + git_sheet
    t = Table(git_data, colWidths=[2.8*cm, 7.5*cm, 6.2*cm])
    cat_style = []
    prev = None
    for i, row in enumerate(git_data[1:], 1):
        if row[0]:
            prev = row[0]
            cat_style.append(("BACKGROUND", (0,i),(0,i), C_BLUE_LIGHT))
            cat_style.append(("FONTNAME",   (0,i),(0,i), "Helvetica-Bold"))
            cat_style.append(("TEXTCOLOR",  (0,i),(0,i), C_BLUE_DARK))
        else:
            cat_style.append(("BACKGROUND", (0,i),(0,i), C_WHITE))
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0),  C_BLUE_DARK),
        ("TEXTCOLOR",     (0,0), (-1,0),  C_WHITE),
        ("FONTNAME",      (0,0), (-1,0),  "Helvetica-Bold"),
        ("FONTNAME",      (1,1), (1,-1),  "Courier"),
        ("FONTSIZE",      (0,0), (-1,-1), 8.5),
        ("GRID",          (0,0), (-1,-1), 0.5, colors.HexColor("#CFD8DC")),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [C_WHITE, C_GRAY_LIGHT]),
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ] + cat_style))
    story.append(t)
    story.append(vspace(12))

    # Docker Cheat Sheet
    story.append(mini_header("DOCKER CHEAT SHEET", C_GREEN_DARK))
    story.append(vspace(4))
    docker_sheet = [
        ["IMAGES",      "docker build -t myapp .",               "Build image"],
        ["",            "docker build -t myapp:v1.0 .",          "Build with tag"],
        ["",            "docker images",                          "List images"],
        ["",            "docker rmi myapp",                       "Remove image"],
        ["",            "docker pull node:alpine",                "Download image"],
        ["CONTAINERS",  "docker run -p 3000:8081 myapp",         "Run (your project)"],
        ["",            "docker run -d -p 3000:8081 myapp",      "Run in background"],
        ["",            "docker run --name web -p 3000:8081 myapp","Run with name"],
        ["",            "docker ps",                              "Running containers"],
        ["",            "docker ps -a",                           "All containers"],
        ["",            "docker stop web",                        "Stop container"],
        ["",            "docker start web",                       "Start stopped container"],
        ["",            "docker rm web",                          "Remove container"],
        ["INSPECT",     "docker logs web",                        "View output logs"],
        ["",            "docker logs -f web",                     "Follow live logs"],
        ["",            "docker exec -it web sh",                 "Shell into container"],
        ["",            "docker inspect web",                     "Full container details"],
        ["CLEANUP",     "docker system prune",                    "Remove all unused"],
        ["",            "docker volume prune",                    "Remove unused volumes"],
    ]
    d_header = [["Category", "Command", "What It Does"]]
    docker_data = d_header + docker_sheet
    t2 = Table(docker_data, colWidths=[2.8*cm, 7.5*cm, 6.2*cm])
    cat_style2 = []
    for i, row in enumerate(docker_data[1:], 1):
        if row[0]:
            cat_style2.append(("BACKGROUND", (0,i),(0,i), C_GREEN_LIGHT))
            cat_style2.append(("FONTNAME",   (0,i),(0,i), "Helvetica-Bold"))
            cat_style2.append(("TEXTCOLOR",  (0,i),(0,i), C_GREEN_DARK))
        else:
            cat_style2.append(("BACKGROUND", (0,i),(0,i), C_WHITE))
    t2.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0),  C_GREEN_DARK),
        ("TEXTCOLOR",     (0,0), (-1,0),  C_WHITE),
        ("FONTNAME",      (0,0), (-1,0),  "Helvetica-Bold"),
        ("FONTNAME",      (1,1), (1,-1),  "Courier"),
        ("FONTSIZE",      (0,0), (-1,-1), 8.5),
        ("GRID",          (0,0), (-1,-1), 0.5, colors.HexColor("#CFD8DC")),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [C_WHITE, C_GREEN_LIGHT]),
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ] + cat_style2))
    story.append(t2)
    story.append(vspace(12))

    # Quick reference: Your project commands
    story.append(mini_header("YOUR PROJECT — QUICK COMMAND REFERENCE", C_PURPLE))
    story.append(vspace(4))
    project_cmds = [
        ["Action", "Command"],
        ["Build Docker image",
         "docker build -t demo-nodejs ."],
        ["Run the app (with correct port mapping)",
         "docker run -p 3000:8081 demo-nodejs"],
        ["Run in background (detached mode)",
         "docker run -d -p 3000:8081 --name demo demo-nodejs"],
        ["View app in browser",
         "http://localhost:3000"],
        ["See app logs",
         "docker logs demo"],
        ["Stop running app",
         "docker stop demo"],
        ["Rebuild after code change",
         "docker stop demo && docker rm demo && docker build -t demo-nodejs . && docker run -d -p 3000:8081 --name demo demo-nodejs"],
        ["Push code to GitHub",
         "git add . && git commit -m 'your message' && git push origin main"],
        ["Create a feature branch",
         "git checkout -b feature/my-feature"],
        ["Merge feature branch to main",
         "git checkout main && git merge feature/my-feature"],
    ]
    t3 = Table(project_cmds, colWidths=[5.5*cm, 11*cm])
    t3.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0),  C_PURPLE),
        ("TEXTCOLOR",     (0,0), (-1,0),  C_WHITE),
        ("FONTNAME",      (0,0), (-1,0),  "Helvetica-Bold"),
        ("FONTNAME",      (1,1), (1,-1),  "Courier"),
        ("FONTSIZE",      (0,0), (-1,-1), 8.5),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [C_WHITE, C_PURPLE_LIGHT]),
        ("GRID",          (0,0), (-1,-1), 0.5, colors.HexColor("#CFD8DC")),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("WORDWRAP",      (1,1), (1,-1),  "WORD"),
    ]))
    story.append(t3)
    story.append(vspace(12))

    # .gitignore cheat sheet
    story.append(mini_header("WHAT GOES IN .gitignore (FOR YOUR PROJECT)", C_GRAY_DARK))
    story.append(vspace(4))
    story.append(Paragraph(
        "A <b>.gitignore</b> file tells Git which files to never track. "
        "Here's what your Node.js project should ignore:",
        S["body"]
    ))
    story.append(vspace(4))
    gitignore_content = [
        "node_modules/          # 3rd-party packages (re-installed via npm install)",
        ".env                   # Secrets, API keys — NEVER commit these!",
        ".DS_Store              # Mac metadata files",
        "*.log                  # Log files",
        "dist/                  # Build output",
        "coverage/              # Test coverage reports",
        ".dockerignore          # Docker's own ignore file",
        "",
        "# NOT ignored (you DO want to commit these):",
        "# package.json         - dependency list",
        "# package-lock.json    - exact dependency versions",
        "# Dockerfile           - container recipe",
        "# app.js, *.html       - your actual code",
    ]
    for line in gitignore_content:
        style = S["code"] if not line.startswith("#") and line else ParagraphStyle(
            "gitignore_comment", parent=S["code"],
            textColor=colors.HexColor("#546E7A")
        )
        story.append(Paragraph(line if line else "&nbsp;", style))
    story.append(vspace(12))

    # Final tips box
    story.append(mini_header("BEGINNER TIPS — THINGS TO REMEMBER", C_ORANGE))
    story.append(vspace(4))
    tips = [
        ("Commit often, push daily", "Small commits are easier to understand and revert than giant ones."),
        ("Read the error message",   "Docker and Git errors are descriptive. Read the FULL error, not just the first line."),
        ("Google is your friend",    "Copy the exact error message into Google. Stack Overflow and GitHub Issues are gold."),
        ("Don't fear the terminal",  "Every command you run, you learn. The more you type, the more natural it becomes."),
        ("Use 'git status' constantly","Before and after every git command. It's your compass."),
        ("Tag your Docker images",   "Use -t myapp:v1.0 so you can roll back to previous versions."),
        ("Keep main always working", "Never push broken code to main. Use branches for experiments."),
    ]
    tips_data = [["Tip", "Why"]] + [[f"• {t}", d] for t, d in tips]
    t4 = Table(tips_data, colWidths=[5.5*cm, 11*cm])
    t4.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0),  C_ORANGE),
        ("TEXTCOLOR",     (0,0), (-1,0),  C_WHITE),
        ("FONTNAME",      (0,0), (-1,0),  "Helvetica-Bold"),
        ("FONTNAME",      (0,1), (0,-1),  "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1), 9),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [C_WHITE, C_ORANGE_LIGHT]),
        ("GRID",          (0,0), (-1,-1), 0.5, colors.HexColor("#FFE0B2")),
        ("TOPPADDING",    (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]))
    story.append(t4)


# ─── Back Cover ───────────────────────────────────────────────────────────────
def back_cover(story):
    story.append(PageBreak())
    d = Drawing(PAGE_W - 4*cm, 300)
    d.add(Rect(0, 0, PAGE_W - 4*cm, 300, fillColor=C_BG_DARK, strokeColor=None))
    d.add(Circle(50, 260, 60, fillColor=colors.HexColor("#0D47A1"), strokeColor=None))
    d.add(Circle(PAGE_W-4*cm-30, 40, 80, fillColor=colors.HexColor("#1B5E20"), strokeColor=None))

    d.add(String((PAGE_W-4*cm)/2, 240, "Keep building. Keep shipping.",
                 fontSize=22, fillColor=C_WHITE, fontName="Helvetica-Bold",
                 textAnchor="middle"))
    d.add(String((PAGE_W-4*cm)/2, 210,
                 "Every expert was once a beginner who refused to give up.",
                 fontSize=12, fillColor=colors.HexColor("#90CAF9"),
                 fontName="Helvetica-Oblique", textAnchor="middle"))

    items = [
        "Your next steps:",
        "1. Fix the port mismatch in your Dockerfile (EXPOSE 8081)",
        "2. Add a .gitignore to your project",
        "3. Create your first feature branch",
        "4. Build and run your Docker container",
        "5. Push your first PR on GitHub",
    ]
    y = 170
    for item in items:
        color = C_YELLOW if item.startswith("Your") else C_WHITE
        size = 11 if item.startswith("Your") else 10
        d.add(String(60, y, item, fontSize=size, fillColor=color,
                     fontName="Helvetica-Bold" if item.startswith("Your") else "Helvetica",
                     textAnchor="start"))
        y -= 20

    d.add(String((PAGE_W-4*cm)/2, 30,
                 "Muhammad Arham's DevOps Guide  •  demo_nodejs_webpage  •  2026",
                 fontSize=9, fillColor=colors.HexColor("#546E7A"),
                 fontName="Helvetica", textAnchor="middle"))
    story.append(d)


# ─── Page number callback ─────────────────────────────────────────────────────
def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(C_GRAY)
    page_num = canvas.getPageNumber()
    canvas.drawRightString(PAGE_W - 2*cm, 1.2*cm, f"Page {page_num}")
    canvas.drawString(2*cm, 1.2*cm, "Muhammad Arham — DevOps Learning Guide")
    canvas.restoreState()


# ─── Main Builder ─────────────────────────────────────────────────────────────
def build_pdf():
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "DevOps_Guide.pdf")

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,
        title="DevOps Learning Guide — Muhammad Arham",
        author="Muhammad Arham",
        subject="Git, Docker, Node.js DevOps Guide",
    )

    story = []

    print("Building cover page...")
    cover_page(story)

    print("Building table of contents...")
    toc_page(story)

    print("Building Section 1: Big Picture...")
    section_bigpicture(story)

    print("Building Section 2: Git Commands...")
    section_git(story)

    print("Building Section 3: Branching...")
    section_branching(story)

    print("Building Section 4: Docker Concepts...")
    section_docker_concepts(story)

    print("Building Section 5: Dockerfile...")
    section_dockerfile(story)

    print("Building Section 6: Common Errors...")
    section_errors(story)

    print("Building Section 7: Cheat Sheets...")
    section_cheatsheets(story)

    print("Building back cover...")
    back_cover(story)

    print(f"Generating PDF at: {output_path}")
    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)

    size_kb = os.path.getsize(output_path) / 1024
    print(f"\n✓ PDF generated successfully!")
    print(f"  File: {output_path}")
    print(f"  Size: {size_kb:.1f} KB")
    return output_path


if __name__ == "__main__":
    build_pdf()
