# ReshapeX — Robot Deployment Tracker

A real-time operations dashboard for monitoring the deployment status of an industrial robot fleet across multiple manufacturing facilities. Built as a front-end showcase project, ReshapeX simulates the kind of live monitoring tool a robotics or industrial automation company would use to track hardware rollouts across client sites.

![Status](https://img.shields.io/badge/status-active-success)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black)
![Built with Claude Code](https://img.shields.io/badge/Built%20with-Claude%20Code-6366f1)

---

## Overview

ReshapeX tracks a fleet of 8 robots (welding units, precision drills, assembly systems, inspection units, and more) as they move through three deployment stages — **Pending → In Progress → Deployed** — across four manufacturing facilities and client accounts. The dashboard presents fleet-wide summary metrics, a live filterable table of every unit, and per-robot progress bars that update on their own, mimicking a real production monitoring feed.

The project is built entirely with vanilla HTML, CSS, and JavaScript — no frameworks, no build step, no dependencies. Open the file and it runs.

## What It Does

- Displays a live overview of the entire robot fleet: total units, deployed count, in-progress count, and pending count, with completion percentage.
- Renders a detailed fleet table with robot ID, type, assigned client, facility/bay location, current status, deployment timestamp, elapsed time, and a live progress bar.
- Lets users filter the fleet view by status (All / Deployed / In Progress / Pending) with a single click.
- Continuously simulates real deployment activity: in-progress robots advance toward completion, and pending robots automatically kick off deployment — all on a visible countdown timer, so the UI never looks static.
- Ships with its own lightweight test suite that validates the underlying deployment logic and data integrity, runnable directly in the browser console.

## Key Features

**🔴 Real-Time Updates**
A live clock, a "last synced" timestamp, and a visible countdown timer keep the dashboard feeling connected to a live system. Every metric card and table row re-renders automatically as fleet status changes.

**⚙️ Live API Simulation**
Since there's no backend, ReshapeX simulates one: a tick-based engine randomly advances in-progress robots by realistic increments, transitions robots from pending to in-progress, and flips completed units to "Deployed" — reproducing the unpredictability of a real deployment feed without needing a live API.

**✅ QA Test Suite**
A dedicated [test-runner.html](test-runner.html) page runs [tests.js](tests.js) against the deployment logic, covering:
- **Unit tests** — progress values are correctly capped at 100% and never overflow.
- **Integration tests** — every robot record has valid, complete data (status, progress range, required fields).
- **Regression tests** — fleet counters (deployed / in-progress / pending) stay consistent as robots change status.

Results print directly to the browser console with pass/fail styling, making it easy to verify the dashboard's core logic hasn't broken after a change.

**🎨 Polished, Dark-Themed UI**
A cohesive dark interface with gradient accents, animated status indicators, hover states, and color-coded badges — designed to look and feel like a production-grade internal tool.

## Technologies Used

| Technology | Purpose |
|---|---|
| **HTML5** | Semantic page structure and layout |
| **CSS3** | Custom dark theme, gradients, animations, and responsive grid/table layouts |
| **JavaScript (ES6+)** | Rendering logic, filtering, deployment simulation engine, and test suite |
| **Claude Code** | Used as an AI pair-programming assistant to design, build, and iterate on the dashboard |

No external libraries, frameworks, or build tools are required — everything runs directly in the browser.

## Project Structure

```
├── reshapex.html      # Main dashboard — polished UI, live simulation, filtering
├── dashboard.html      # Earlier dashboard iteration
├── data.js             # Robot fleet dataset consumed by the dashboard
├── robots.json         # Standalone JSON export of the fleet dataset
├── tests.js            # QA test suite (unit, integration, regression)
├── test-runner.html    # Browser page for executing the test suite
└── README.md
```

## Getting Started

No installation or dependencies needed.

1. Clone or download this repository.
2. Open [reshapex.html](reshapex.html) in any modern browser to view the live dashboard.
3. Open [test-runner.html](test-runner.html) and check the DevTools console to see the QA test suite run.

## Why It Was Built

This project was built to explore and demonstrate front-end skills around building a **realistic, data-driven operations dashboard** using only core web technologies — no frameworks or shortcuts. Industrial and robotics companies rely heavily on internal dashboards to track hardware rollouts across clients and facilities, and ReshapeX was designed as a portfolio piece that mirrors exactly that kind of tool: real-time status tracking, filterable data tables, simulated live data feeds, and a QA process to back it up.

It also served as a hands-on exercise in working with **Claude Code** as a development partner — using AI assistance to iterate quickly on UI polish, simulation logic, and test coverage while keeping the codebase clean, dependency-free, and easy to reason about.

## License

This project is available for personal and portfolio use.
