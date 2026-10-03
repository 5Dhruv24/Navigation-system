"""
nl_parser.py

A small rule-based natural-language parser for queries like:
    "how do I get to the library from gate 1"
    "route from boys hostel to the auditorium"
    "block a to block e"

WHY RULE-BASED, NOT A CALL TO AN EXTERNAL AI MODEL?
-----------------------------------------------------
This app runs entirely locally (Flask + a static frontend) with no
API keys configured. A lightweight keyword/alias matcher:
- needs no external service, no cost, no network dependency
- is fully transparent and easy to explain/defend in a viva
  ("here is exactly how it decides what you meant")
- is fast and deterministic — same input always gives same output

This is NOT a general-purpose NLP system. It specifically looks for
two location mentions (matched against LOCATION_ALIASES and the
official LOCATION_NAMES/codes) and tries to work out which one is
the start and which is the destination, using simple sentence
patterns a student is likely to actually type.

HOW IT WORKS:
1. Lowercase the query.
2. Try a few common sentence patterns first ("from X to Y",
   "to X from Y") using regex — these patterns tell us directly
   which mention is the start and which is the end.
3. If no pattern matches, fall back to: find every location mention
   in the text, in the order they appear, and assume the first
   mention is the start and the last is the destination.
4. Each matched phrase is resolved to a node code via
   LOCATION_ALIASES (checked first, since aliases are more specific
   phrases) and then LOCATION_NAMES/raw codes.
"""

import re
from campus_data import CAMPUS_GRAPH, LOCATION_ALIASES, LOCATION_NAMES

# Build one combined lookup of "phrase -> node code", longest
# phrases first, so e.g. "boys hostel" matches before just "boys".
_ALL_PHRASES = list(LOCATION_ALIASES.items())
for code in CAMPUS_GRAPH:
    _ALL_PHRASES.append((code.lower(), code))
    _ALL_PHRASES.append((LOCATION_NAMES.get(code, code).lower(), code))
_ALL_PHRASES.sort(key=lambda pair: -len(pair[0]))  # longest phrase first


def _find_locations_in_text(text):
    """Scan `text` left to right, returning a list of (position, code)
    for every location phrase found, longest matches preferred so
    we don't match "boys" inside an already-matched "boys hostel"."""
    found = []
    used_spans = []

    for phrase, code in _ALL_PHRASES:
        start = 0
        while True:
            idx = text.find(phrase, start)
            if idx == -1:
                break
            end = idx + len(phrase)
            overlaps = any(not (end <= s or idx >= e) for s, e in used_spans)
            if not overlaps:
                found.append((idx, code))
                used_spans.append((idx, end))
            start = end

    found.sort(key=lambda pair: pair[0])
    return found


def parse_query(query):
    """
    Returns (start_code, end_code) on success, or (None, None) if
    fewer than two distinct locations could be identified.
    """
    text = query.lower().strip()

    # --- Pattern 1: "... from X to Y ..." ---
    m = re.search(r"from\s+(.+?)\s+to\s+(.+)", text)
    if m:
        start_matches = _find_locations_in_text(m.group(1))
        end_matches = _find_locations_in_text(m.group(2))
        if start_matches and end_matches:
            return start_matches[-1][1], end_matches[0][1]

    # --- Pattern 2: "... to Y from X ..." ---
    m = re.search(r"to\s+(.+?)\s+from\s+(.+)", text)
    if m:
        end_matches = _find_locations_in_text(m.group(1))
        start_matches = _find_locations_in_text(m.group(2))
        if start_matches and end_matches:
            return start_matches[-1][1], end_matches[0][1]

    # --- Fallback: first mention = start, last mention = end ---
    all_matches = _find_locations_in_text(text)
    distinct_codes = []
    for _, code in all_matches:
        if code not in distinct_codes:
            distinct_codes.append(code)

    if len(distinct_codes) >= 2:
        return distinct_codes[0], distinct_codes[-1]

    return None, None
