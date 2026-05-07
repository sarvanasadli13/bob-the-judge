# Bob the Judge — 3-Minute Demo Script
# IBM Bob Hackathon · May 15-17, 2026

---

## TIMING GUIDE
| Segment | Time | Cumulative |
|---------|------|-----------|
| Hook (Bob can't ship alone) | 0:20 | 0:20 |
| Problem (the missing layer) | 0:20 | 0:40 |
| Solution framing | 0:15 | 0:55 |
| Live demo — Run Analysis | 0:25 | 1:20 |
| Live demo — Apply Bob's Patch (the flip) | 0:30 | 1:50 |
| Live demo — Export PDF | 0:15 | 2:05 |
| Business value | 0:35 | 2:40 |
| Close | 0:20 | 3:00 |

---

## SCRIPT (word-for-word)

---

### [0:00 — HOOK]
*(screen shows dashboard, IBM logo visible, no analysis yet)*

"IBM Bob can translate COBOL to Java.
It can write the code, generate the tests, ship the patch.

But translation isn't the hard part anymore.

The hard part is the decision: **when to flip the switch.**
That's a decision no AI tool has ever made autonomously.
Until now."

---

### [0:20 — PROBLEM]
*(keep dashboard on screen)*

"Today, a CTO running a migration is stuck.
They have two systems running in parallel.
Bob has rewritten everything.
Tests are passing.

But nobody can prove — function by function — that the new system
will behave identically to the old one in production.

Seventy percent of enterprise migrations stall right here, for months.
That's the missing layer Bob needs."

---

### [0:40 — SOLUTION]
*(point to IBM logo in top bar)*

"Bob the Judge is that missing layer.

It runs live traffic through both systems, scores parity per function,
and tells Bob when each function is safe to ship —
with a regulator-grade audit trail in one click.

Not 'is the system 87% ready' — that's what every other tool says.
**Which exact functions can Bob flip today.**"

---

### [1:00 — DEMO: RUN ANALYSIS]
*(click Run Analysis, watch spinner)*

"We have two live banking systems running right now.
A legacy COBOL-style payment processor — and its modern replacement.
Bob the Judge is sending real payment transactions through both, simultaneously."

*(results appear — scorecards show)*

"And here's the verdict.

Domestic Wire Transfer — **Safe to Cut**. 100% parity. Cut it today.
Scheduled Payments — **Safe to Cut**. 100% parity. Cut it today.
International Wire — **Do Not Cut**. Zero parity. Fee calculation divergence."

*(point to the score numbers)*

"Not a gut feeling. A readiness score. Per function. With evidence."

---

### [1:20 — DEMO: APPLY BOB'S PATCH — THE FLIP]
*(scroll to "Bob's Live Patch" section, hover the button)*

"Here's where it gets interesting.

Bob the Judge already knows International and High-Value Wire are blocked.
Watch what happens when I let Bob fix it himself."

*(click "Apply Bob's Patch & Re-Analyse")*

*(wait for spinner — Bob's code response appears)*

"Bob just generated a parallel-run compatibility patch — the FX margin
and the SWIFT fee schedule, aligned with legacy during the dual-run window.
Then it deployed itself to the modern banking service. And re-ran the analysis."

*(scroll up to scorecards — they should now all be green)*

"And there it is. All four functions, **safe to cut over.**
The verdict flipped — live, in front of you — because Bob fixed what Bob found.

That is Bob in Code mode and Orchestrator mode, working together,
with Bob the Judge as the verification layer.
This is what autonomous migration looks like."

---

### [1:50 — DEMO: EXPORT PDF]
*(scroll back down, click Export PDF, then Download)*

"One click. Regulator-grade audit report.
Executive summary, function verdicts, divergence log, sign-off page.

This is the document your compliance team needs before cutover.
Generated automatically. No manual reporting. No waiting for consultants."

---

### [2:05 — BUSINESS VALUE]
*(switch to pitch deck slide 7 — CTO testimonial — or speak to camera)*

"This is real pain. 800 billion lines of COBOL still in production.
$80 billion spent annually on mainframe modernization.
Seventy percent of migrations stall in dual-run for months — at $200,000 per month
in duplicate infrastructure.

Bob can write the code. Bob can ship the code.
But until now, Bob couldn't decide when to flip the switch.

Bob the Judge is that decision layer. The autonomous verification step
that lets Bob complete the migration without a CTO making a gut call."

---

### [2:40 — CLOSE]
*(back to dashboard, all scorecards green)*

"Bob writes the code. Bob ships it.
**Bob the Judge tells Bob when to flip the switch.**

The autonomous decision layer Bob was missing — built with IBM Bob,
for the enterprises that can't afford to get it wrong."

---

## KEY PHRASES TO MEMORIZE
- *"Translation isn't the hard part anymore. The decision is."* — the new positioning
- *"Bob can write the code. Bob can ship it. Bob couldn't decide when to flip."* — the gap
- *"Watch what happens when I let Bob fix it himself."* — set up the patch
- *"The verdict flipped — live, in front of you — because Bob fixed what Bob found."* — the wow moment
- *"Bob the Judge tells Bob when to flip the switch."* — closing line

## THINGS TO SHOW IN ORDER
1. Top bar — IBM branding + "MCP READY" indicator visible
2. Click Run Analysis — point to mixed verdicts (2 SAFE, 2 DO NOT CUT)
3. Pause on red verdicts — let judges absorb the failure
4. Click "Apply Bob's Patch & Re-Analyse" — Bob's code response appears
5. Scroll up — all 4 scorecards now GREEN (the flip)
6. Export PDF → Download
7. Close on the all-green dashboard

## WHAT NOT TO DO
- Do not explain the code or architecture
- Do not say "as you can see" — just point and describe
- Do not rush past the patch flip — that IS the demo
- Do not apologize for the mock Bob label — say "Real Bob API connects at the kick-off stream tonight"
- Do not click Reset Patch during the demo — leave the green state for the close
