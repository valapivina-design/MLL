# Broker inbox

Drop new brokers here, then merge:

```bash
python3 tools/import_brokers.py --no-forensic --inbox
```

## Accepted files

- `*.json` — array of broker objects, or `{ "brokers": [ ... ] }`
- `*.jsonl` — one broker object per line
- `*.example` / `example.*` — ignored (see `example.batch.json.example`)

## Minimal broker object

```json
{
  "slug": "example-broker-review",
  "name": "Example Broker",
  "tier": "scam",
  "blurb": "a short description of what the platform claims to be.",
  "domain": "example.com",
  "aliases": ["Old Brand Name"],
  "officialDomain": "example.com",
  "clones": [{ "domain": "documented-lookalike.com", "name": "Only if we also index it or a story names it" }]
}
```

Forensic-shaped rows also work: `{ "n": "Name", "s": "slug-review", "t": "scam", "d": "blurb" }`.

Curated fields (`aliases`, `clones`, `timeline`, `fundFlow`, …) on existing slugs are preserved on merge.
