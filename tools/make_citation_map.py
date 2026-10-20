"""Generate citation_map.html for the homepage with the `citation-map` package.

Usage (run locally, from anywhere):
    pip install citation-map
    python tools/make_citation_map.py <GOOGLE_SCHOLAR_ID>

Outputs go to the repository root (the parent of tools/):
    citation_map.html   the interactive map embedded by index.html
    citation_info.csv   the parsed citing authors and affiliations
The download cache is kept in tools/cache/ (git-ignored).

Notes:
- Requires Google Chrome to be installed: Google Scholar may show CAPTCHA
  pop-ups that you need to solve by hand.
- Do not run this often. Google Scholar blocks IPs that send many requests;
  regenerating every few months is enough. Do not run it in GitHub Actions or
  other cloud machines (their IPs are usually blocked).
- If the map has wrong or missing affiliations, edit citation_info.csv and
  rerun with --from-csv to rebuild the map from the CSV without re-scraping.
- This file must not be named citation_map.py, or `import citation_map`
  would import this script instead of the package.
"""

import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Generate citation_map.html from a Google Scholar profile.")
    parser.add_argument("scholar_id", help="Google Scholar ID (the user=XXXX part of the profile URL)")
    parser.add_argument("--conservative", action="store_true",
                        help="Use conservative affiliation matching (fewer, more reliable pins)")
    parser.add_argument("--processes", type=int, default=4,
                        help="Number of parallel processes (default 4; use 1 if you get blocked)")
    parser.add_argument("--proxy", action="store_true",
                        help="Route requests through a free proxy (slower, may help when blocked)")
    parser.add_argument("--from-csv", action="store_true",
                        help="Rebuild the map from the existing (possibly edited) citation_info.csv")
    args = parser.parse_args()

    from citation_map import generate_citation_map

    tools_dir = Path(__file__).resolve().parent
    repo_root = tools_dir.parent

    generate_citation_map(
        args.scholar_id,
        output_path=str(repo_root / "citation_map.html"),
        csv_output_path=str(repo_root / "citation_info.csv"),
        parse_csv=args.from_csv,
        cache_folder=str(tools_dir / "cache"),
        affiliation_conservative=args.conservative,
        num_processes=args.processes,
        use_proxy=args.proxy,
        pin_colorful=True,
        print_citing_affiliations=True,
    )
    print(f"Done: {repo_root / 'citation_map.html'}")


if __name__ == "__main__":
    main()
