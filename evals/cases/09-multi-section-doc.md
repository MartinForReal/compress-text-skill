---
id: 09-multi-section-doc
mode: readable
aggressiveness: aggressive
should_trigger: true
---

## Prompt

Compress and restructure this doc. Generate candidate groupings and pick the leanest.

## Input

## Setup
To set the project up, install Node 20. You also need to install Node 20 before
running anything. Then copy `.env.example` to `.env`.

## Configuration
Set the `DATABASE_URL` variable in your `.env` file. You should set `DATABASE_URL`
to point at your Postgres instance. Also set `PORT`, which defaults to 8080.

## Running
Run `npm start` to start the app. The app starts on the `PORT` you configured.
Remember that you must have copied `.env.example` to `.env` first (see Setup).

## Troubleshooting
If the app will not start, check that `DATABASE_URL` is set correctly. Most start-up
failures are caused by a missing or wrong `DATABASE_URL`.

## Rubric

- [ ] Preserves all load-bearing facts: Node 20; copy `.env.example` → `.env`; set `DATABASE_URL` (Postgres); `PORT` defaults to 8080; `npm start`; troubleshooting = check `DATABASE_URL`
- [ ] Preserves verbatim identifiers: `DATABASE_URL`, `PORT`, `8080`, `npm start`, `.env`, `.env.example`, `Node 20`
- [ ] Removes the duplicated statements (install Node 20 twice; set `DATABASE_URL` twice; the `.env` copy restated under Running)
- [ ] Groups are MECE (each fact appears once; the cross-reference dup is consolidated)
- [ ] Reports a candidate comparison (≥2 candidates) and selects one with a reason
- [ ] Output is shorter than input and preserves a usable section structure/ordering
