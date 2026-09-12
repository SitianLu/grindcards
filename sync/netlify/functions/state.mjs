/**
 * Optional cross-device progress sync for a GrindCards app — Netlify Functions flavour.
 *
 * Drop this file at netlify/functions/state.mjs next to your built deck, deploy, and the
 * app's "Cross-device sync" menu works: open the app with #k=<32 hex chars> on one device,
 * copy the sync link to the others.
 *
 * The key IS the record name (a capability URL): knowing the key means knowing where the
 * data lives. No env vars, no login page, zero configuration — the simplest auth a
 * single-person app can get away with, at the cost that a leaked key leaks the data
 * (which is only flashcard progress).
 *
 * The server merges; clients only ever push their own copy. Two devices online at once
 * cannot overwrite each other. The merge rule must stay identical to the one in the app.
 */
import { getStore } from '@netlify/blobs';

const KEY_RE = /^[a-f0-9]{32}$/;
const MAX_BODY = 64 * 1024;          // a few hundred cards is a few KB; more is abuse
const STORE = 'grindcards-progress';

const json = (body, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { 'content-type': 'application/json', 'cache-control': 'no-store' },
  });

/** Per-entry, newest timestamp wins. Whole-document last-write-wins would let a stale
 *  desktop tab swallow twenty cards reviewed on the phone. */
function mergeMap(a = {}, b = {}) {
  const out = { ...a };
  for (const [k, v] of Object.entries(b || {})) {
    if (!v || typeof v !== 'object') continue;
    const t = Number(v.t) || 0;
    if (!out[k] || t >= (Number(out[k].t) || 0)) out[k] = v;
  }
  return out;
}

/** Whole-block newest wins — for preferences (filters are interdependent; merging them
 *  field by field would produce a combination nobody set) and for the current card. */
function newer(a, b) {
  const ta = Number(a && a.t) || 0, tb = Number(b && b.t) || 0;
  return tb > ta ? b : (a || b || null);
}

export default async (req) => {
  if (req.method === 'OPTIONS') return new Response(null, { status: 204 });

  // GET = health check. Open /api/state in a browser to tell apart three failures that
  // look identical from the app ("sync failed"): function not deployed, dependency
  // missing, blob store unreachable.
  if (req.method === 'GET') {
    const out = { ok: true, fn: 'state', blobs: 'unknown', at: new Date().toISOString() };
    try {
      await getStore(STORE).get('__healthcheck__');   // read only
      out.blobs = 'ok';
    } catch (e) {
      out.ok = false;
      out.blobs = 'FAIL: ' + (e && e.message ? e.message : String(e));
    }
    return json(out, out.ok ? 200 : 500);
  }

  if (req.method !== 'POST') return json({ error: 'POST only' }, 405);

  const raw = await req.text();
  if (raw.length > MAX_BODY) return json({ error: 'payload too large' }, 413);

  let body;
  try { body = JSON.parse(raw); } catch { return json({ error: 'bad json' }, 400); }

  const key = String(body.k || '');
  if (!KEY_RE.test(key)) return json({ error: 'bad key' }, 400);

  const store = getStore(STORE);
  // strong: a write must be visible to the next device immediately
  const prev = (await store.get(key, { type: 'json', consistency: 'strong' })) || {};
  const doc = body.doc && typeof body.doc === 'object' ? body.doc : {};

  const merged = {
    v: 1,
    cards: mergeMap(prev.cards, doc.cards),
    todoM: mergeMap(prev.todoM, doc.todoM),
    prefs: newer(prev.prefs, doc.prefs),
    view: newer(prev.view, doc.view),
    at: Date.now(),
  };

  await store.setJSON(key, merged);
  return json(merged);
};

export const config = { path: '/api/state' };
