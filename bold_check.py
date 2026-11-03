"""Lore characteristics check (swccg-guild/work#72, STANDARD Rev 15/16).

  python3 bold_check.py test          # AC1: every KEYWORDS occurrence in every spec's lore is bold after bold_keywords()
  python3 bold_check.py report OUT.md # AC2/AC3: one row per card x characteristic, reference vs remaster

The reference is the card's transcription (`cards/vs*/NN.json` "lore"), which marks bold (*...*) where the slip or printed
card prints it bold. bold_keywords() then bolds every characteristic on the remaster (Bill 2026-10-13, 2026-11-03).
"""
import glob, json, re, sys
from collections import defaultdict
from build_vs import KEYWORDS, bold_keywords, template_for

KW = re.compile(rf"(?i)(?<![A-Za-z])(?:{KEYWORDS})(?![A-Za-z])")


def specs():
    for f in sorted(glob.glob("cards/vs*/[0-9][0-9]*.json")):
        if ".card." in f:
            continue
        c = json.load(open(f, encoding="utf-8"))
        if c.get("lore"):
            yield f.split("cards/")[1], c


def exception(text: str, m) -> str | None:
    before, after = text[:m.start()], text[m.end():]
    if re.search(r"(?i)\bformer\s+$", before):
        return "Former …"
    if re.search(r"(?i)\bthen-$", before):
        return "then-…"
    if re.match(r"[’']s\b", after):
        return "possessive"
    return None


def occurrences(lore: str):
    """(characteristic, bold on the reference, offset) for every KEYWORDS match in the transcription."""
    plain = lore.replace("*", "")
    spans, pos = [], 0     # bold spans of the transcription mapped onto the plain text
    for part in re.split(r"(\*[^*]+\*)", lore):
        t = part.strip("*") if part.startswith("*") else part
        if part.startswith("*"):
            spans.append((pos, pos + len(t)))
        pos += len(t)
    for m in KW.finditer(plain):
        yield m, any(a <= m.start() and m.end() <= b for a, b in spans), plain


def remaster_lore(c: dict) -> str:
    """The lore exactly as build_vs builds it: Rev 15 bolds characteristics on character cards only (and not where a spec
    sets "bold_lore": false)."""
    return bold_keywords(c["lore"]) if "character" in template_for(c) and c.get("bold_lore", True) else c["lore"]


def why_not(c: dict) -> str | None:
    if "character" not in template_for(c):
        return "not a character"
    if not c.get("bold_lore", True):
        return "bold_lore off"
    return None


def remaster_bold(c: dict):
    return [(m, b) for m, b, _ in occurrences(remaster_lore(c))]


def test():
    n = bad = 0
    lines = []
    for f, c in specs():
        for m, b, plain in occurrences(remaster_lore(c)):
            n += 1
            ex = exception(plain, m) or why_not(c)
            if not b and not ex:
                bad += 1
                lines.append(f"FAIL {f}: '{m.group(0)}' not bold: {plain[:90]}")
            elif not b:
                lines.append(f"ok   {f}: '{m.group(0)}' plain ({ex})")
    lines.append(f"{n} occurrences checked, {bad} not bold outside the exceptions")
    print("\n".join(lines))
    return bad == 0


def report(out):
    rows, seen = [], defaultdict(lambda: [0, 0])     # characteristic -> [bold on refs, plain on refs]
    for f, c in specs():
        rem = remaster_bold(c)
        for i, (m, ref_bold, plain) in enumerate(occurrences(c["lore"])):
            w = m.group(0).lower()
            ex = exception(plain, m) or why_not(c)
            rb = rem[i][1] if i < len(rem) else None
            seen[w][0 if ref_bold else 1] += 1
            rows.append([f, c["title"], m.group(0), "bold" if ref_bold else "plain", "bold" if rb else f"plain ({ex})" if ex else "plain",
                         "yes" if (rb != ref_bold) else "", plain[max(0, m.start() - 30): m.end() + 30].replace("|", "/")])
    # R4: the PC set its slips set by set, so a characteristic printed plain where another card of the SAME Virtual Set
    # prints it bold is flagged as a possible PC (or transcription) error; plain across a whole set is that set's style.
    bold_in_set = defaultdict(list)
    for r in rows:
        if r[3] == "bold":
            bold_in_set[(r[0].split("/")[0], r[2].lower())].append(r[0])
    for r in rows:
        other = bold_in_set.get((r[0].split("/")[0], r[2].lower()), [])
        r.append(f"possible PC error ({other[0]} prints it bold)" if r[3] == "plain" and other and not r[4].startswith("plain (") else "")
    bold_words = defaultdict(list)
    for f, c in specs():
        for t in re.findall(r"\*([^*]+)\*", c["lore"]):
            bold_words[t.strip(" .,;:").lower()].append(f)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("| Spec | Card | Characteristic | Reference | Remaster | Differs | Possible PC error | Context |\n|---|---|---|---|---|---|---|---|\n")
        for r in rows:
            fh.write(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} | {r[7]} | …{r[6]}… |\n")
        fh.write("\n## Every word set bold on a reference (AC3)\n\n| Word | References | In KEYWORDS |\n|---|---|---|\n")
        for w, fs in sorted(bold_words.items(), key=lambda kv: -len(kv[1])):
            fh.write(f"| {w} | {len(fs)} ({', '.join(fs[:4])}{' …' if len(fs) > 4 else ''}) | {'yes' if KW.fullmatch(w) else 'NO'} |\n")
    print(f"{len(rows)} rows, {sum(1 for r in rows if r[5])} differ, {sum(1 for r in rows if r[7])} possible PC errors -> {out}")


if __name__ == "__main__":
    if sys.argv[1] == "test":
        sys.exit(0 if test() else 1)
    report(sys.argv[2])
