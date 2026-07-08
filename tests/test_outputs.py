import json
from collections import Counter
from pathlib import Path

LOG_PATH = Path("/app/access.log")
REPORT_PATH = Path("/app/report.json")
EXPECTED_KEYS = {"total_requests", "unique_ips", "top_path"}


def load_report():
    assert REPORT_PATH.exists(), "/app/report.json was not created"
    return json.loads(REPORT_PATH.read_text())


def parse_access_log():
    total_requests = 0
    client_ips = set()
    path_counts = Counter()

    with LOG_PATH.open() as log_file:
        for raw_line in log_file:
            line = raw_line.strip()
            if not line:
                continue

            prefix, request, _suffix = line.split('"', 2)
            ip_address = prefix.split()[0]
            _method, path, _protocol = request.split()

            total_requests += 1
            client_ips.add(ip_address)
            path_counts[path] += 1

    return total_requests, client_ips, path_counts


def expected_top_path(path_counts):
    top_path = ""
    top_count = -1

    for path, count in path_counts.items():
        if count > top_count:
            top_path = path
            top_count = count

    return top_path


def test_criterion_1_report_is_valid_json_with_exact_top_level_keys():
    """Success criterion 1: /app/report.json is valid JSON with exactly total_requests, unique_ips, and top_path."""
    report = load_report()

    assert isinstance(report, dict)
    assert set(report.keys()) == EXPECTED_KEYS


def test_criterion_2_total_requests_counts_non_empty_log_entries():
    """Success criterion 2: total_requests is the total number of non-empty log entries."""
    report = load_report()
    total_requests, _client_ips, _path_counts = parse_access_log()

    assert report["total_requests"] == total_requests


def test_criterion_3_unique_ips_counts_distinct_client_ip_addresses():
    """Success criterion 3: unique_ips is the number of distinct client IP addresses in the log."""
    report = load_report()
    _total_requests, client_ips, _path_counts = parse_access_log()

    assert report["unique_ips"] == len(client_ips)


def test_criterion_4_top_path_is_most_frequent_path_with_first_seen_tie_break():
    """Success criterion 4: top_path is the most frequent request path, with ties broken by first appearance."""
    report = load_report()
    _total_requests, _client_ips, path_counts = parse_access_log()

    assert report["top_path"] == expected_top_path(path_counts)


def test_criterion_5_report_values_have_required_json_types():
    """Success criterion 5: total_requests and unique_ips are JSON integers, and top_path is a JSON string."""
    report = load_report()

    assert isinstance(report["total_requests"], int)
    assert not isinstance(report["total_requests"], bool)
    assert isinstance(report["unique_ips"], int)
    assert not isinstance(report["unique_ips"], bool)
    assert isinstance(report["top_path"], str)
