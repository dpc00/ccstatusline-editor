import json
import os
from pathlib import Path
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

SETTINGS_PATH = Path.home() / ".config" / "ccstatusline" / "settings.json"

WIDGET_TYPES = [
    {"type": "model",                    "group": "AI"},
    {"type": "output-style",             "group": "AI"},
    {"type": "thinking-effort",          "group": "AI"},
    {"type": "skills",                   "group": "AI"},
    {"type": "version",                  "group": "AI"},
    {"type": "context-percentage",       "group": "Context"},
    {"type": "context-percentage-usable","group": "Context"},
    {"type": "context-length",           "group": "Context"},
    {"type": "context-window",           "group": "Context"},
    {"type": "context-bar",              "group": "Context"},
    {"type": "compaction-counter",       "group": "Context"},
    {"type": "session-cost",             "group": "Session"},
    {"type": "session-clock",            "group": "Session"},
    {"type": "session-name",             "group": "Session"},
    {"type": "session-usage",            "group": "Session"},
    {"type": "block-timer",              "group": "Session"},
    {"type": "reset-timer",              "group": "Session"},
    {"type": "tokens-input",             "group": "Tokens"},
    {"type": "tokens-output",            "group": "Tokens"},
    {"type": "tokens-cached",            "group": "Tokens"},
    {"type": "tokens-total",             "group": "Tokens"},
    {"type": "cache-hit-rate",           "group": "Tokens"},
    {"type": "cache-read",               "group": "Tokens"},
    {"type": "cache-write",              "group": "Tokens"},
    {"type": "input-speed",              "group": "Speed"},
    {"type": "output-speed",             "group": "Speed"},
    {"type": "total-speed",              "group": "Speed"},
    {"type": "weekly-usage",             "group": "Usage"},
    {"type": "weekly-sonnet-usage",      "group": "Usage"},
    {"type": "weekly-opus-usage",        "group": "Usage"},
    {"type": "weekly-reset-timer",       "group": "Usage"},
    {"type": "extra-usage-utilization",  "group": "Usage"},
    {"type": "extra-usage-remaining",    "group": "Usage"},
    {"type": "extra-usage-used",         "group": "Usage"},
    {"type": "git-branch",               "group": "Git"},
    {"type": "git-changes",              "group": "Git"},
    {"type": "git-status",               "group": "Git"},
    {"type": "git-clean-status",         "group": "Git"},
    {"type": "git-staged",               "group": "Git"},
    {"type": "git-unstaged",             "group": "Git"},
    {"type": "git-untracked",            "group": "Git"},
    {"type": "git-staged-files",         "group": "Git"},
    {"type": "git-unstaged-files",       "group": "Git"},
    {"type": "git-untracked-files",      "group": "Git"},
    {"type": "git-insertions",           "group": "Git"},
    {"type": "git-deletions",            "group": "Git"},
    {"type": "git-ahead-behind",         "group": "Git"},
    {"type": "git-conflicts",            "group": "Git"},
    {"type": "git-sha",                  "group": "Git"},
    {"type": "git-root-dir",             "group": "Git"},
    {"type": "git-review",               "group": "Git"},
    {"type": "git-worktree",             "group": "Git"},
    {"type": "git-origin-owner",         "group": "Git Origin"},
    {"type": "git-origin-repo",          "group": "Git Origin"},
    {"type": "git-origin-owner-repo",    "group": "Git Origin"},
    {"type": "git-upstream-owner",       "group": "Git Origin"},
    {"type": "git-upstream-repo",        "group": "Git Origin"},
    {"type": "git-upstream-owner-repo",  "group": "Git Origin"},
    {"type": "git-is-fork",              "group": "Git Origin"},
    {"type": "worktree-mode",            "group": "Worktree"},
    {"type": "worktree-name",            "group": "Worktree"},
    {"type": "worktree-branch",          "group": "Worktree"},
    {"type": "worktree-original-branch", "group": "Worktree"},
    {"type": "jj-bookmarks",             "group": "Jujutsu"},
    {"type": "jj-workspace",             "group": "Jujutsu"},
    {"type": "jj-root-dir",              "group": "Jujutsu"},
    {"type": "jj-changes",               "group": "Jujutsu"},
    {"type": "jj-insertions",            "group": "Jujutsu"},
    {"type": "jj-deletions",             "group": "Jujutsu"},
    {"type": "jj-description",           "group": "Jujutsu"},
    {"type": "jj-revision",              "group": "Jujutsu"},
    {"type": "current-working-dir",      "group": "System"},
    {"type": "free-memory",              "group": "System"},
    {"type": "terminal-width",           "group": "System"},
    {"type": "claude-session-id",        "group": "System"},
    {"type": "claude-account-email",     "group": "System"},
    {"type": "vim-mode",                 "group": "System"},
    {"type": "voice-status",             "group": "System"},
    {"type": "remote-control-status",    "group": "System"},
    {"type": "custom-text",              "group": "Custom"},
    {"type": "custom-symbol",            "group": "Custom"},
    {"type": "custom-command",           "group": "Custom"},
    {"type": "link",                     "group": "Custom"},
    {"type": "separator",                "group": "Layout"},
    {"type": "flex-separator",           "group": "Layout"},
]


GROUPS = ["AI","Context","Session","Tokens","Speed","Usage","Git","Git Origin","Worktree","Jujutsu","System","Custom"]

def scheme(name, desc, ai, ctx, ses, tok, spd, use, git, gito, wt, jj, sys_, cus):
    return {"name": name, "desc": desc, "colors": {
        "AI": ai, "Context": ctx, "Session": ses, "Tokens": tok,
        "Speed": spd, "Usage": use, "Git": git, "Git Origin": gito,
        "Worktree": wt, "Jujutsu": jj, "System": sys_, "Custom": cus,
    }}

#                  name              desc                         AI        Ctx       Ses       Tok       Spd       Use       Git       GitO      WT        JJ        Sys       Cus
SCHEMES = [
    scheme("Ocean",          "Cool blues and cyans",              "cyan",   "blue",   "green",  "cyan",   "blue",   "yellow", "blue",   "blue",   "cyan",   "blue",   "white",  "white"),
    scheme("Deep Sea",       "All blues, deep and calm",          "blue",   "cyan",   "blue",   "cyan",   "blue",   "blue",   "cyan",   "blue",   "cyan",   "blue",   "cyan",   "white"),
    scheme("Sky",            "Cyan and white, open air",          "cyan",   "cyan",   "blue",   "white",  "cyan",   "blue",   "blue",   "blue",   "cyan",   "blue",   "white",  "cyan"),
    scheme("Ice",            "Pale and cold",                     "white",  "cyan",   "white",  "cyan",   "white",  "blue",   "cyan",   "blue",   "white",  "cyan",   "white",  "cyan"),
    scheme("Sapphire",       "Rich blue throughout",              "blue",   "blue",   "cyan",   "blue",   "blue",   "cyan",   "blue",   "blue",   "blue",   "blue",   "white",  "blue"),
    scheme("Forest",         "Greens and earth tones",            "green",  "green",  "cyan",   "yellow", "green",  "yellow", "green",  "green",  "green",  "green",  "white",  "yellow"),
    scheme("Matrix",         "Pure green on black",               "green",  "green",  "green",  "green",  "green",  "green",  "green",  "green",  "green",  "green",  "green",  "green"),
    scheme("Nature",         "Natural greens and yellows",        "green",  "yellow", "green",  "cyan",   "green",  "yellow", "green",  "green",  "green",  "green",  "white",  "white"),
    scheme("Spring",         "Fresh greens and cyan",             "green",  "cyan",   "green",  "yellow", "cyan",   "green",  "green",  "cyan",   "green",  "green",  "white",  "yellow"),
    scheme("Jade",           "Teal and green gem",                "cyan",   "green",  "green",  "cyan",   "green",  "yellow", "green",  "green",  "cyan",   "green",  "white",  "cyan"),
    scheme("Everforest",     "Muted greens, warm feel",           "green",  "green",  "yellow", "cyan",   "green",  "yellow", "green",  "green",  "green",  "green",  "white",  "yellow"),
    scheme("Fire",           "Red and yellow heat",               "red",    "yellow", "red",    "yellow", "red",    "yellow", "red",    "red",    "red",    "red",    "white",  "yellow"),
    scheme("Sunset",         "Red, magenta, golden",              "red",    "yellow", "magenta","yellow", "red",    "magenta","yellow", "red",    "magenta","red",    "white",  "yellow"),
    scheme("Autumn",         "Warm reds and yellows",             "yellow", "red",    "yellow", "red",    "yellow", "red",    "yellow", "red",    "yellow", "red",    "white",  "yellow"),
    scheme("Lava",           "Molten red and orange",             "red",    "yellow", "red",    "yellow", "red",    "yellow", "red",    "red",    "red",    "yellow", "white",  "red"),
    scheme("Ruby",           "Deep reds and magenta",             "red",    "magenta","red",    "red",    "magenta","red",    "red",    "magenta","red",    "red",    "white",  "red"),
    scheme("Desert",         "Sandy yellows and warm white",      "yellow", "yellow", "red",    "yellow", "white",  "yellow", "yellow", "yellow", "yellow", "yellow", "white",  "yellow"),
    scheme("Amber",          "All amber/yellow",                  "yellow", "yellow", "yellow", "yellow", "yellow", "yellow", "yellow", "yellow", "yellow", "yellow", "white",  "yellow"),
    scheme("Neon",           "Electric pop colours",              "magenta","cyan",   "green",  "yellow", "cyan",   "magenta","green",  "cyan",   "magenta","cyan",   "white",  "yellow"),
    scheme("Royal",          "Purple and blue regal",             "blue",   "magenta","blue",   "cyan",   "blue",   "magenta","blue",   "magenta","blue",   "blue",   "white",  "magenta"),
    scheme("Nebula",         "Deep space purples",                "magenta","blue",   "cyan",   "magenta","blue",   "cyan",   "magenta","blue",   "magenta","blue",   "white",  "cyan"),
    scheme("Synthwave",      "Retro purple and cyan",             "magenta","cyan",   "magenta","blue",   "cyan",   "magenta","cyan",   "magenta","cyan",   "magenta","white",  "cyan"),
    scheme("Rose",           "Pink and magenta blooms",           "magenta","red",    "magenta","red",    "magenta","red",    "magenta","red",    "magenta","magenta","white",  "magenta"),
    scheme("Grape",          "Solid magenta/purple",              "magenta","magenta","blue",   "magenta","magenta","magenta","magenta","magenta","magenta","magenta","white",  "magenta"),
    scheme("Dracula",        "Classic Dracula palette",           "magenta","cyan",   "green",  "cyan",   "green",  "yellow", "green",  "cyan",   "magenta","cyan",   "white",  "magenta"),
    scheme("Nord",           "Arctic blues and whites",           "blue",   "cyan",   "white",  "blue",   "cyan",   "blue",   "blue",   "cyan",   "blue",   "blue",   "white",  "blue"),
    scheme("Solarized",      "Balanced warm/cool tones",          "yellow", "cyan",   "green",  "yellow", "cyan",   "yellow", "green",  "cyan",   "yellow", "green",  "white",  "yellow"),
    scheme("Gruvbox",        "Warm retro earthy",                 "yellow", "green",  "yellow", "green",  "yellow", "red",    "green",  "yellow", "green",  "yellow", "white",  "yellow"),
    scheme("Monokai",        "Classic Monokai",                   "magenta","green",  "yellow", "cyan",   "green",  "red",    "green",  "cyan",   "magenta","green",  "white",  "yellow"),
    scheme("Tokyo Night",    "Dark city neons",                   "blue",   "magenta","cyan",   "blue",   "cyan",   "blue",   "magenta","blue",   "cyan",   "magenta","white",  "cyan"),
    scheme("Catppuccin",     "Soft pastel mocha",                 "magenta","blue",   "cyan",   "green",  "cyan",   "yellow", "green",  "blue",   "magenta","cyan",   "white",  "magenta"),
    scheme("One Dark",       "Atom One Dark",                     "blue",   "cyan",   "green",  "yellow", "cyan",   "red",    "green",  "blue",   "cyan",   "green",  "white",  "magenta"),
    scheme("Oceanic Next",   "Muted ocean blue-green",            "cyan",   "blue",   "cyan",   "blue",   "cyan",   "blue",   "green",  "cyan",   "blue",   "cyan",   "white",  "cyan"),
    scheme("Vibrant",        "Every group a different hue",       "cyan",   "yellow", "green",  "blue",   "magenta","red",    "green",  "blue",   "cyan",   "magenta","white",  "yellow"),
    scheme("Candy",          "Playful bright mix",                "magenta","cyan",   "yellow", "green",  "cyan",   "magenta","green",  "blue",   "cyan",   "magenta","white",  "yellow"),
    scheme("Cyberpunk",      "High-voltage cyan and magenta",     "cyan",   "magenta","yellow", "cyan",   "magenta","yellow", "cyan",   "magenta","cyan",   "magenta","white",  "yellow"),
    scheme("Aurora",         "Northern lights",                   "green",  "cyan",   "magenta","green",  "cyan",   "magenta","green",  "cyan",   "magenta","green",  "white",  "cyan"),
    scheme("Carnival",       "Circus brights",                    "red",    "yellow", "green",  "blue",   "magenta","cyan",   "green",  "blue",   "yellow", "red",    "white",  "magenta"),
    scheme("Monochrome",     "Pure white on dark",                "white",  "white",  "white",  "white",  "white",  "white",  "white",  "white",  "white",  "white",  "white",  "white"),
    scheme("Zen",            "Mostly quiet, tiny accents",        "cyan",   "white",  "white",  "white",  "white",  "white",  "white",  "white",  "white",  "white",  "white",  "white"),
    scheme("Minimal",        "Only AI and Git stand out",         "cyan",   "white",  "white",  "white",  "white",  "white",  "green",  "white",  "white",  "white",  "white",  "white"),
    scheme("Git Focus",      "Git highlighted, rest quiet",       "white",  "white",  "white",  "white",  "white",  "white",  "green",  "green",  "green",  "white",  "white",  "white"),
    scheme("Cost Alert",     "Session cost in red, rest quiet",   "white",  "yellow", "red",    "yellow", "white",  "red",    "white",  "white",  "white",  "white",  "white",  "white"),
    scheme("Dev Mode",       "Code-focused: AI, Git, Context",    "cyan",   "yellow", "white",  "white",  "white",  "white",  "green",  "white",  "green",  "green",  "white",  "white"),
    scheme("Danger",         "Everything red — something's wrong","red",    "red",    "red",    "red",    "red",    "red",    "red",    "red",    "red",    "red",    "red",    "red"),
    scheme("Warning",        "All yellow caution",                "yellow", "yellow", "yellow", "yellow", "yellow", "yellow", "yellow", "yellow", "yellow", "yellow", "yellow", "yellow"),
    scheme("Safe",           "All green, everything OK",          "green",  "green",  "green",  "green",  "green",  "green",  "green",  "green",  "green",  "green",  "green",  "green"),
    scheme("Winter",         "Cold blue-white season",            "white",  "cyan",   "blue",   "white",  "cyan",   "blue",   "white",  "blue",   "white",  "blue",   "white",  "cyan"),
    scheme("Summer",         "Warm sunny vibes",                  "yellow", "green",  "green",  "cyan",   "yellow", "green",  "green",  "green",  "yellow", "green",  "white",  "yellow"),
    scheme("Christmas",      "Red and green festive",             "red",    "green",  "red",    "green",  "red",    "green",  "green",  "red",    "green",  "red",    "white",  "yellow"),
    scheme("Halloween",      "Orange-yellow and red spooky",      "red",    "yellow", "red",    "yellow", "red",    "yellow", "yellow", "red",    "yellow", "red",    "white",  "yellow"),
    scheme("Cobalt",         "Strong cyan and yellow contrast",   "cyan",   "yellow", "green",  "cyan",   "white",  "yellow", "cyan",   "yellow", "cyan",   "cyan",   "white",  "yellow"),
    scheme("Hemisu",         "Blue and white with cyan hints",    "blue",   "cyan",   "white",  "cyan",   "blue",   "white",  "white",  "cyan",   "blue",   "white",  "white",  "cyan"),
    scheme("Flatland",       "Clean multi-hue flat design",       "blue",   "cyan",   "green",  "yellow", "cyan",   "blue",   "green",  "blue",   "cyan",   "green",  "white",  "yellow"),
    scheme("Paraiso",        "Tropical bright mix",               "magenta","cyan",   "green",  "yellow", "green",  "red",    "green",  "cyan",   "magenta","green",  "white",  "yellow"),
    scheme("Retro Terminal", "Old-school amber phosphor",         "yellow", "yellow", "yellow", "yellow", "yellow", "yellow", "yellow", "yellow", "yellow", "yellow", "yellow", "yellow"),
    scheme("Hacker",         "Green on black, old hacker",        "green",  "green",  "green",  "green",  "green",  "yellow", "green",  "green",  "green",  "green",  "white",  "green"),
    scheme("Blueprint",      "Engineer blue-on-white feel",       "blue",   "blue",   "blue",   "cyan",   "blue",   "blue",   "blue",   "blue",   "blue",   "blue",   "white",  "blue"),
]


def w(type_, color=None):
    d = {"type": type_}
    if color: d["color"] = color
    return d

def fsep():
    return {"type": "flex-separator"}

def sep(char=None):
    d = {"type": "separator"}
    if char: d["metadata"] = {"character": char}
    return d

WIDGET_SCHEMES = [
    {
        "name": "Context Watch",
        "desc": "Laser focus on how full your context window is getting. Catch compaction before it surprises you.",
        "tags": ["context","compaction"],
        "lines": [
            [w("context-percentage","yellow"), fsep(), w("context-percentage-usable","yellow"), w("context-window","blue"), w("context-length","blue")],
            [w("context-bar","green"), fsep(), w("compaction-counter","red")],
        ]
    },
    {
        "name": "Cost Monitor",
        "desc": "Track session spend, weekly budget burn, and time until reset. Know before it hurts.",
        "tags": ["cost","budget","usage"],
        "lines": [
            [w("session-cost","red"), fsep(), w("block-timer","white"), w("reset-timer","yellow")],
            [w("weekly-usage","yellow"), w("weekly-sonnet-usage","yellow"), w("weekly-opus-usage","red"), fsep(), w("weekly-reset-timer","white")],
            [w("extra-usage-utilization","yellow"), fsep(), w("extra-usage-remaining","green"), w("extra-usage-used","red")],
        ]
    },
    {
        "name": "Project Orientation",
        "desc": "Answer 'where am I and what state is it in?' at a glance. Good for context-switching between repos.",
        "tags": ["git","project","orientation"],
        "lines": [
            [w("current-working-dir","white"), fsep(), w("git-root-dir","white"), w("git-branch","magenta")],
            [w("git-status","yellow"), w("git-clean-status","green"), fsep(), w("git-ahead-behind","cyan")],
        ]
    },
    {
        "name": "Git Full Picture",
        "desc": "Everything git at once — staged, unstaged, conflicts, insertions/deletions, remote status.",
        "tags": ["git","staged","conflicts"],
        "lines": [
            [w("git-branch","magenta"), w("git-status","yellow"), fsep(), w("git-ahead-behind","cyan"), w("git-review","blue")],
            [w("git-staged","green"), w("git-unstaged","yellow"), w("git-untracked","white"), fsep(), w("git-conflicts","red")],
            [w("git-insertions","green"), w("git-deletions","red"), fsep(), w("git-staged-files","green"), w("git-unstaged-files","yellow"), w("git-untracked-files","white")],
        ]
    },
    {
        "name": "Git Minimal",
        "desc": "Branch and dirty status only. Low noise for when you mostly trust your own git awareness.",
        "tags": ["git","minimal"],
        "lines": [
            [w("git-branch","magenta"), fsep(), w("git-changes","yellow"), w("git-clean-status","green")],
        ]
    },
    {
        "name": "Code Reviewer",
        "desc": "Focused on review workflow — PR status, ahead/behind, diff stats, and conflicts.",
        "tags": ["git","review","pr"],
        "lines": [
            [w("git-branch","magenta"), w("git-review","blue"), fsep(), w("git-ahead-behind","cyan"), w("git-conflicts","red")],
            [w("git-insertions","green"), w("git-deletions","red"), fsep(), w("git-staged-files","green"), w("git-unstaged-files","yellow")],
        ]
    },
    {
        "name": "Remote Origin",
        "desc": "Which remote repo are you working against? Fork status and upstream visibility.",
        "tags": ["git","remote","fork"],
        "lines": [
            [w("git-origin-owner-repo","blue"), fsep(), w("git-is-fork","yellow"), w("git-branch","magenta")],
            [w("git-upstream-owner-repo","magenta"), fsep(), w("git-ahead-behind","cyan"), w("git-review","blue")],
        ]
    },
    {
        "name": "Token Economy",
        "desc": "Watch every token: input, output, cached, and total. Cache hit rate shows if caching is paying off.",
        "tags": ["tokens","cache","cost"],
        "lines": [
            [w("tokens-input","white"), w("tokens-output","white"), fsep(), w("tokens-cached","cyan"), w("tokens-total","white")],
            [w("cache-hit-rate","green"), w("cache-read","green"), fsep(), w("cache-write","yellow")],
        ]
    },
    {
        "name": "Speed Check",
        "desc": "How fast is the model responding? Useful for noticing throttling or latency spikes.",
        "tags": ["speed","performance","tokens"],
        "lines": [
            [w("input-speed","white"), w("output-speed","cyan"), w("total-speed","white"), fsep(), w("cache-hit-rate","green")],
        ]
    },
    {
        "name": "Session Overview",
        "desc": "A balanced view of the current session — model, time, cost, and context in one sweep.",
        "tags": ["session","overview","model"],
        "lines": [
            [w("model","cyan"), w("session-name","white"), fsep(), w("session-clock","white"), w("block-timer","white")],
            [w("session-cost","green"), w("session-usage","yellow"), fsep(), w("context-percentage","yellow"), w("compaction-counter","red")],
        ]
    },
    {
        "name": "Model Intelligence",
        "desc": "What AI am I talking to and how is it configured? Model, output style, thinking effort.",
        "tags": ["model","ai","settings"],
        "lines": [
            [w("model","cyan"), w("output-style","blue"), fsep(), w("thinking-effort","magenta"), w("skills","blue")],
            [w("version","white"), fsep(), w("vim-mode","yellow"), w("voice-status","green")],
        ]
    },
    {
        "name": "Budget Dashboard",
        "desc": "Weekly spend across model tiers plus extra usage. Know your bill before the end of the month.",
        "tags": ["budget","weekly","usage"],
        "lines": [
            [w("weekly-usage","yellow"), fsep(), w("weekly-sonnet-usage","yellow"), w("weekly-opus-usage","red")],
            [w("extra-usage-utilization","yellow"), fsep(), w("extra-usage-remaining","green"), w("extra-usage-used","red")],
            [w("weekly-reset-timer","white"), fsep(), w("session-cost","green")],
        ]
    },
    {
        "name": "Writing / Docs",
        "desc": "Non-coding work. Just model, session time, cost, and context — no git noise.",
        "tags": ["writing","minimal","docs"],
        "lines": [
            [w("model","cyan"), w("session-clock","white"), fsep(), w("session-cost","green"), w("context-percentage","yellow")],
        ]
    },
    {
        "name": "Focus Mode",
        "desc": "Absolute minimum. Context fill and cost only. Everything else is distraction.",
        "tags": ["minimal","focus"],
        "lines": [
            [w("context-percentage","yellow"), fsep(), w("session-cost","green")],
        ]
    },
    {
        "name": "Minimal Classic",
        "desc": "Model, cost, git branch, changes. The timeless four.",
        "tags": ["minimal","classic"],
        "lines": [
            [w("model","cyan"), fsep(), w("session-cost","green"), w("git-branch","magenta"), w("git-changes","yellow")],
        ]
    },
    {
        "name": "Status Board",
        "desc": "A broader dashboard — model, git, context, tokens and cache at a glance.",
        "tags": ["overview","dashboard"],
        "lines": [
            [w("model","cyan"), w("git-branch","magenta"), fsep(), w("session-cost","green"), w("context-percentage","yellow")],
            [w("tokens-total","white"), w("cache-hit-rate","green"), fsep(), w("git-changes","yellow"), w("git-ahead-behind","cyan")],
        ]
    },
    {
        "name": "Workspace Navigator",
        "desc": "Where exactly are you? Working dir, git root, branch and worktree all visible.",
        "tags": ["workspace","worktree","navigation"],
        "lines": [
            [w("current-working-dir","white"), fsep(), w("git-root-dir","white"), w("git-branch","magenta")],
            [w("worktree-mode","cyan"), w("worktree-name","cyan"), fsep(), w("worktree-branch","cyan"), w("worktree-original-branch","blue")],
        ]
    },
    {
        "name": "Multi-Worktree",
        "desc": "Managing several worktrees simultaneously. Full worktree context with base branch reference.",
        "tags": ["worktree","git","parallel"],
        "lines": [
            [w("worktree-mode","cyan"), w("worktree-name","cyan"), w("worktree-branch","magenta"), fsep(), w("worktree-original-branch","blue"), w("git-ahead-behind","yellow")],
            [w("git-staged","green"), w("git-unstaged","yellow"), fsep(), w("git-conflicts","red")],
        ]
    },
    {
        "name": "Pair Programming",
        "desc": "Shared session context — who's driving? Session name, model, and current branch prominently shown.",
        "tags": ["pair","session","git"],
        "lines": [
            [w("session-name","cyan"), w("model","blue"), fsep(), w("git-branch","magenta"), w("git-status","yellow")],
            [w("context-percentage","yellow"), fsep(), w("session-cost","green"), w("block-timer","white")],
        ]
    },
    {
        "name": "Performance Audit",
        "desc": "Detailed performance analysis — token throughput, cache efficiency, cost per operation.",
        "tags": ["performance","tokens","cache","speed"],
        "lines": [
            [w("tokens-input","white"), w("tokens-output","white"), w("tokens-cached","cyan"), fsep(), w("tokens-total","white")],
            [w("cache-hit-rate","green"), w("cache-read","green"), w("cache-write","yellow"), fsep(), w("input-speed","white"), w("output-speed","cyan"), w("total-speed","white")],
            [w("session-cost","red"), fsep(), w("context-percentage","yellow"), w("compaction-counter","red")],
        ]
    },
    {
        "name": "Night Owl",
        "desc": "Late session check-in. Time, cost, context. Know when to stop.",
        "tags": ["session","time","cost"],
        "lines": [
            [w("session-clock","white"), w("block-timer","white"), fsep(), w("session-cost","red"), w("reset-timer","yellow")],
            [w("context-percentage","yellow"), fsep(), w("compaction-counter","red")],
        ]
    },
    {
        "name": "Ops / DevOps",
        "desc": "System and environment info alongside git state. Good for infrastructure or deployment work.",
        "tags": ["ops","system","git"],
        "lines": [
            [w("current-working-dir","white"), w("git-branch","magenta"), fsep(), w("git-clean-status","green"), w("git-ahead-behind","cyan")],
            [w("free-memory","cyan"), w("terminal-width","white"), fsep(), w("session-cost","green"), w("block-timer","white")],
        ]
    },
    {
        "name": "Open Source Contributor",
        "desc": "Fork, upstream, PR status and diff stats. The view a contributor needs.",
        "tags": ["git","oss","fork","pr"],
        "lines": [
            [w("git-origin-owner-repo","blue"), w("git-is-fork","yellow"), fsep(), w("git-branch","magenta"), w("git-review","blue")],
            [w("git-upstream-owner-repo","magenta"), fsep(), w("git-ahead-behind","cyan"), w("git-conflicts","red")],
            [w("git-insertions","green"), w("git-deletions","red"), fsep(), w("git-staged-files","green"), w("git-unstaged-files","yellow")],
        ]
    },
    {
        "name": "Jujutsu User",
        "desc": "For jj VCS users. Bookmarks, workspace, changes and revision info front and centre.",
        "tags": ["jj","jujutsu","vcs"],
        "lines": [
            [w("jj-bookmarks","magenta"), w("jj-workspace","cyan"), fsep(), w("jj-description","white"), w("jj-revision","white")],
            [w("jj-changes","yellow"), w("jj-insertions","green"), w("jj-deletions","red"), fsep(), w("jj-root-dir","white")],
        ]
    },
    {
        "name": "Weekly Reviewer",
        "desc": "End-of-week accounting. Usage across model tiers, time to reset, extra quota consumed.",
        "tags": ["weekly","budget","review"],
        "lines": [
            [w("weekly-usage","yellow"), fsep(), w("weekly-sonnet-usage","yellow"), w("weekly-opus-usage","red")],
            [w("extra-usage-utilization","yellow"), w("extra-usage-used","red"), fsep(), w("extra-usage-remaining","green"), w("weekly-reset-timer","white")],
        ]
    },
    {
        "name": "Long Session Survival",
        "desc": "Context creeping up, compaction looming, cost ticking. The endurance runner's view.",
        "tags": ["context","cost","compaction","session"],
        "lines": [
            [w("context-percentage","yellow"), w("context-length","blue"), fsep(), w("compaction-counter","red"), w("context-bar","green")],
            [w("session-cost","red"), w("session-clock","white"), fsep(), w("block-timer","white"), w("reset-timer","yellow")],
        ]
    },
    {
        "name": "Identity",
        "desc": "Who am I, where am I, what session is this? Account, session ID, working dir.",
        "tags": ["account","session","identity"],
        "lines": [
            [w("claude-account-email","white"), w("session-name","cyan"), fsep(), w("claude-session-id","white")],
            [w("current-working-dir","white"), fsep(), w("git-branch","magenta"), w("model","cyan")],
        ]
    },
    {
        "name": "Diff Watcher",
        "desc": "Watch changes accumulate as you work. Lines added and deleted, files modified.",
        "tags": ["git","diff","changes"],
        "lines": [
            [w("git-insertions","green"), w("git-deletions","red"), fsep(), w("git-staged-files","green"), w("git-unstaged-files","yellow"), w("git-untracked-files","white")],
            [w("git-branch","magenta"), fsep(), w("git-clean-status","green"), w("git-conflicts","red")],
        ]
    },
    {
        "name": "Cache Economist",
        "desc": "All about cache efficiency. Hit rate, reads, writes. Know if you're wasting money on repeated tokens.",
        "tags": ["cache","tokens","cost"],
        "lines": [
            [w("cache-hit-rate","green"), fsep(), w("cache-read","green"), w("cache-write","yellow")],
            [w("tokens-cached","cyan"), w("tokens-total","white"), fsep(), w("session-cost","red")],
        ]
    },
    {
        "name": "The Kitchen Sink",
        "desc": "Everything, grouped logically across lines. Maximum information density.",
        "tags": ["all","everything","full"],
        "lines": [
            [w("model","cyan"), w("output-style","cyan"), w("thinking-effort","blue"), fsep(), w("context-percentage","yellow"), w("context-length","blue"), w("compaction-counter","red")],
            [w("session-cost","green"), w("block-timer","white"), fsep(), w("weekly-usage","yellow"), w("reset-timer","yellow")],
            [w("tokens-input","white"), w("tokens-output","white"), w("tokens-cached","cyan"), fsep(), w("cache-hit-rate","green"), w("output-speed","cyan")],
            [w("git-branch","magenta"), w("git-status","yellow"), fsep(), w("git-ahead-behind","cyan"), w("git-conflicts","red")],
        ]
    },
]


@app.route("/")
def index():
    return render_template("index.html", widget_types=WIDGET_TYPES, color_schemes=SCHEMES, widget_schemes=WIDGET_SCHEMES, groups=GROUPS)


@app.route("/api/settings", methods=["GET"])
def get_settings():
    if not SETTINGS_PATH.exists():
        return jsonify({"error": f"Not found: {SETTINGS_PATH}"}), 404
    with open(SETTINGS_PATH) as f:
        return jsonify(json.load(f))


@app.route("/api/settings", methods=["POST"])
def save_settings():
    data = request.get_json()
    SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(SETTINGS_PATH, "w") as f:
        json.dump(data, f, indent=2)
    return jsonify({"ok": True, "path": str(SETTINGS_PATH)})


@app.route("/api/widgets")
def get_widgets():
    return jsonify(WIDGET_TYPES)


if __name__ == "__main__":
    print(f"Editing: {SETTINGS_PATH}")
    app.run(debug=True, port=5199)
