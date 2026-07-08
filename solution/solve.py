import json
from collections import Counter

paths = Counter()
ips = set()
total = 0

with open("/app/access.log") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            prefix, request, _suffix = line.split('"', 2)
            ip = prefix.split()[0]
            _method, path, _version = request.split()
        except (IndexError, ValueError) as exc:
            raise ValueError(f"Malformed access log entry: {line}") from exc
        total += 1
        ips.add(ip)
        paths[path] += 1

top_path = ""
top_count = -1
for path, count in paths.items():
    if count > top_count:
        top_path = path
        top_count = count

with open("/app/report.json", "w") as out:
    json.dump(
        {
            "total_requests": total,
            "unique_ips": len(ips),
            "top_path": top_path,
        },
        out,
        sort_keys=True,
    )
print("wrote /app/report.json")
