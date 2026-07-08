Read the Apache-style access log at /app/access.log and write a JSON report to
/app/report.json.

For each non-empty log line, use the first token as the client IP. Use the path
inside the quoted request as the request path. For example, in
"GET /index.html HTTP/1.1", the path is /index.html.

Success criteria:

1. /app/report.json must be valid JSON with exactly these keys: total_requests,
   unique_ips, and top_path.
2. total_requests must equal the number of non-empty log entries.
3. unique_ips must equal the number of distinct client IPs.
4. top_path must be the most common request path. If there is a tie, choose the
   tied path that appears first in the log.
5. total_requests and unique_ips must be JSON integers, and top_path
   must be a JSON string.
