import argparse
import csv
import random
import re
import sys
from collections import Counter, defaultdict
from typing import Iterable, List, Optional, Tuple


DIGITS = "0123456789"


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ssc",
        description="SSC CLI: generate numbers, analyze CSV history, check bets",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # generate
    p_gen = subparsers.add_parser("generate", help="Generate random 5-digit SSC numbers")
    p_gen.add_argument("--count", type=int, default=1, help="How many numbers to generate")
    p_gen.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    p_gen.add_argument("--unique", action="store_true", help="Ensure generated numbers are unique")
    p_gen.add_argument(
        "--format",
        choices=["plain", "csv"],
        default="plain",
        help="Output format",
    )
    p_gen.set_defaults(func=handle_generate)

    # analyze
    p_an = subparsers.add_parser(
        "analyze", help="Analyze historical draws from a CSV file"
    )
    p_an.add_argument("csv_path", help="Path to CSV file containing historical draws")
    p_an.add_argument(
        "--col",
        help=(
            "Column name or 0-based index that contains draws. "
            "If omitted, auto-detect a column with 5-digit values."
        ),
        default=None,
    )
    p_an.add_argument(
        "--limit", type=int, default=None, help="Only analyze the first N rows"
    )
    p_an.set_defaults(func=handle_analyze)

    # check
    p_ck = subparsers.add_parser(
        "check", help="Check bets against a draw (supports wildcards ? x *)"
    )
    p_ck.add_argument("draw", help="Winning draw as 5-digit string, e.g., 01234")
    p_ck.add_argument(
        "--bet",
        action="append",
        default=[],
        help=(
            "Bet pattern (repeatable). 5 chars; digits or wildcards ? x *. "
            "Examples: 12345 (exact), 12x4?, *0?*?"
        ),
    )
    p_ck.add_argument(
        "--bets-file",
        help="Path to a text file with one bet per line",
        default=None,
    )
    p_ck.set_defaults(func=handle_check)

    return parser


def main(argv: Optional[List[str]] = None) -> None:
    parser = create_parser()
    args = parser.parse_args(argv)
    args.func(args)


# --------------------- generate ---------------------

def handle_generate(args: argparse.Namespace) -> None:
    count: int = args.count
    seed: Optional[int] = args.seed
    ensure_unique: bool = args.unique
    out_format: str = args.format

    rng = random.Random(seed)

    generated: List[str] = []
    seen = set()

    while len(generated) < count:
        number = "".join(rng.choice(DIGITS) for _ in range(5))
        if ensure_unique and number in seen:
            continue
        generated.append(number)
        seen.add(number)

    if out_format == "csv":
        writer = csv.writer(sys.stdout)
        for n in generated:
            writer.writerow([n])
    else:
        for n in generated:
            print(n)


# --------------------- analyze ---------------------

def normalize_draw(value: str) -> Optional[str]:
    if value is None:
        return None
    digits_only = re.sub(r"\D", "", value)
    if len(digits_only) == 5 and digits_only.isdigit():
        return digits_only
    return None


def detect_draw_column(header: Optional[List[str]], rows: Iterable[List[str]], probe_rows: int = 200) -> Optional[int]:
    candidates_counter: Counter[int] = Counter()
    row_count = 0
    for row in rows:
        row_count += 1
        for idx, cell in enumerate(row):
            if normalize_draw(cell) is not None:
                candidates_counter[idx] += 1
        if probe_rows is not None and row_count >= probe_rows:
            break
    if not candidates_counter:
        return None
    # choose column with most hits
    best_idx, _ = candidates_counter.most_common(1)[0]
    return best_idx


def resolve_column_index(col_arg: Optional[str], header: Optional[List[str]]) -> Optional[int]:
    if col_arg is None:
        return None
    # try integer index
    try:
        return int(col_arg)
    except (TypeError, ValueError):
        pass
    if header is None:
        return None
    # match by header name (case-insensitive, trimmed)
    normalized_to_index = {h.strip().lower(): i for i, h in enumerate(header)}
    return normalized_to_index.get(col_arg.strip().lower())


def iter_draws_from_csv(csv_path: str, col: Optional[str], limit: Optional[int]) -> Iterable[str]:
    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        sample = f.read(4096)
        f.seek(0)
        sniffer = csv.Sniffer()
        try:
            has_header = sniffer.has_header(sample)
        except csv.Error:
            has_header = False
        reader = csv.reader(f)
        header: Optional[List[str]] = next(reader) if has_header else None

        col_index = resolve_column_index(col, header)

        # If column is unknown, we need to detect it. Re-open a lightweight reader.
        if col_index is None:
            probe_rows: List[List[str]] = []
            # We already read one row if header exists; now probe up to 200
            for i, row in enumerate(reader):
                probe_rows.append(row)
                if limit is not None and i >= limit:
                    break
                if i >= 200:
                    break
            col_index = detect_draw_column(header, probe_rows)
            # Now iterate again from the beginning (after header)
            if has_header:
                f.seek(0)
                next(csv.reader(f))  # consume header again
                reader = csv.reader(f)
            else:
                f.seek(0)
                reader = csv.reader(f)
        else:
            # We already consumed header if present; reader continues
            pass

        yielded = 0
        for row in reader:
            if limit is not None and yielded >= limit:
                break
            cell = row[col_index] if (col_index is not None and col_index < len(row)) else None
            draw = normalize_draw(cell) if cell is not None else None
            if draw is None:
                # Try whole-row fallback: concatenate row to see if any 5-digit pattern exists
                joined = " ".join(row)
                draw = normalize_draw(joined)
            if draw is not None:
                yielded += 1
                yield draw


def classify_pattern(draw: str) -> str:
    counts = Counter(draw)
    freq = sorted(counts.values(), reverse=True)
    if freq[0] == 5:
        return "five-kind"
    if freq[0] == 4:
        return "four-kind"
    if freq[0] == 3 and len(freq) == 2:
        return "full-house"  # 3+2
    if freq[0] == 3:
        return "triple"
    if freq[0] == 2 and freq.count(2) == 2:
        return "two-pairs"
    if freq[0] == 2:
        return "one-pair"
    return "all-distinct"


def handle_analyze(args: argparse.Namespace) -> None:
    csv_path: str = args.csv_path
    col: Optional[str] = args.col
    limit: Optional[int] = args.limit

    total_draws = 0
    pos_counts = [Counter() for _ in range(5)]
    overall_counts = Counter()
    sum_distribution = Counter()
    parity_distribution = Counter()  # even/odd by sum
    big_small_counts = Counter()  # big vs small by individual digits aggregated
    pattern_counts = Counter()

    for draw in iter_draws_from_csv(csv_path, col, limit):
        total_draws += 1
        # per-position counts
        for i, ch in enumerate(draw):
            pos_counts[i][ch] += 1
            overall_counts[ch] += 1
            big_small_counts["big" if int(ch) >= 5 else "small"] += 1
        digit_sum = sum(int(c) for c in draw)
        sum_distribution[digit_sum] += 1
        parity_distribution["even" if (digit_sum % 2 == 0) else "odd"] += 1
        pattern_counts[classify_pattern(draw)] += 1

    if total_draws == 0:
        print("No draws detected in the specified CSV.", file=sys.stderr)
        sys.exit(1)

    def pct(part: int, whole: int) -> str:
        return f"{(part / whole * 100):.2f}%"

    print(f"Total draws: {total_draws}")

    print("\nPosition-wise digit frequencies:")
    for i, cnt in enumerate(pos_counts):
        # show digits 0-9 on one line with counts and percents
        line = []
        for d in DIGITS:
            c = cnt[d]
            line.append(f"{d}:{c}({pct(c, total_draws)})")
        print(f"  Pos {i}: " + " ".join(line))

    print("\nOverall digit frequencies:")
    overall_total = total_draws * 5
    line = []
    for d in DIGITS:
        c = overall_counts[d]
        line.append(f"{d}:{c}({pct(c, overall_total)})")
    print("  " + " ".join(line))

    print("\nBig/Small distribution (per-digit):")
    for key in ["small", "big"]:
        c = big_small_counts[key]
        print(f"  {key}: {c} ({pct(c, overall_total)})")

    print("\nSum distribution (top 10 by frequency):")
    for s, c in sum_distribution.most_common(10):
        print(f"  sum={s}: {c} ({pct(c, total_draws)})")

    print("\nParity by sum:")
    for k in ["even", "odd"]:
        c = parity_distribution[k]
        print(f"  {k}: {c} ({pct(c, total_draws)})")

    print("\nPattern distribution:")
    for k, c in pattern_counts.most_common():
        print(f"  {k}: {c} ({pct(c, total_draws)})")


# --------------------- check ---------------------

def bet_to_regex(bet: str) -> Optional[re.Pattern]:
    bet = bet.strip()
    if not bet:
        return None
    # Normalize common wildcards to digit wildcard
    bet = bet.replace("x", "?")
    bet = bet.replace("*", "?")

    # If it's exactly 5 digits -> exact match
    if re.fullmatch(r"\d{5}", bet):
        return re.compile("^" + bet + "$")

    # If contains invalid characters other than digits and '?', reject
    if not re.fullmatch(r"[\d\?]{1,10}", bet):
        return None

    # Compress multiple '?' if present; but enforce final length = 5
    # If length is not 5, reject
    if len(bet) != 5:
        return None

    pattern = "^" + bet.replace("?", "[0-9]") + "$"
    try:
        return re.compile(pattern)
    except re.error:
        return None


def handle_check(args: argparse.Namespace) -> None:
    draw: str = args.draw
    if normalize_draw(draw) is None:
        print("Draw must be a 5-digit string.", file=sys.stderr)
        sys.exit(2)

    bets: List[str] = list(args.bet or [])
    if args.bets_file:
        with open(args.bets_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    bets.append(line)

    if not bets:
        print("No bets provided.", file=sys.stderr)
        sys.exit(2)

    winners: List[str] = []
    invalid: List[str] = []

    for b in bets:
        rx = bet_to_regex(b)
        if rx is None:
            invalid.append(b)
            continue
        if rx.fullmatch(draw):
            winners.append(b)

    print(f"Draw: {draw}")
    print(f"Total bets: {len(bets)}")
    print(f"Winners: {len(winners)}")
    for w in winners:
        print(f"  {w}")

    if invalid:
        print("\nInvalid bets (skipped):", file=sys.stderr)
        for ib in invalid:
            print(f"  {ib}", file=sys.stderr)
