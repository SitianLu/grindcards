# Optional: cross-device sync

The built app stores progress in the browser. That is enough for one device. To keep a
phone and a laptop in step, the app can POST its progress to `/api/state` on the same
origin and merge whatever comes back; the menu's "Cross-device sync" section drives it.

This directory holds a reference endpoint for Netlify (`netlify/functions/state.mjs`,
uses Netlify Blobs, no configuration). Any host works as long as it answers
`POST /api/state` with `{k, doc}` → merged `doc` using the same merge rule:

- `cards` and `todoM`: per entry, newest timestamp `t` wins;
- `prefs` and `view`: whole block, newest `t` wins.

The rule lives in one place in the app (`mergeMap`, `applyPrefs`) and must stay identical
on the server, otherwise two devices fight.

## Deploy on Netlify

```
mydeck/
  build/                    ← output of `grindcards build`
  netlify/functions/state.mjs
  netlify.toml
```

```toml
# netlify.toml
[build]
  publish = "build"
```

`npm install @netlify/blobs`, push, done. Open `https://<site>/api/state` in a browser: it
returns `{"ok": true, ...}` when the function and the blob store are reachable. Then open
the app as `https://<site>/#k=<32 hex characters>` — any 32 hex characters you make up —
and use "Copy sync link" from the menu on the other devices.

The key is the record name. Whoever has the link has the progress; nothing else is stored.
