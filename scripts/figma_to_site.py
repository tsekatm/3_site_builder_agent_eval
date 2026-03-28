#!/usr/bin/env python3
"""Figma-to-Site: Single-call pipeline test.

Usage:
    python3 scripts/figma_to_site.py <figma_url> [--model sonnet|opus|haiku]

Example:
    python3 scripts/figma_to_site.py "https://www.figma.com/design/w8Qtdxpc6i6aOgcha3dllW/Experience-Madikwe?node-id=1-864"
    python3 scripts/figma_to_site.py "https://www.figma.com/design/w8Qtdxpc6i6aOgcha3dllW/Experience-Madikwe?node-id=1-864" --model opus
"""

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from eval_core.figma.extractor import FigmaDesignExtractor
from eval_core.figma.prompt_builder import DesignPromptBuilder


def get_figma_token() -> str:
    """Get Figma token from env or AWS Secrets Manager."""
    token = os.environ.get("FIGMA_ACCESS_TOKEN")
    if token:
        return token
    try:
        result = subprocess.run(
            ["aws", "secretsmanager", "get-secret-value",
             "--secret-id", "bbws/dev/figma-api-token",
             "--region", "eu-west-1", "--profile", "Tebogo-dev",
             "--query", "SecretString", "--output", "text"],
            capture_output=True, text=True, timeout=15,
        )
        if result.returncode == 0:
            return json.loads(result.stdout)["FIGMA_ACCESS_TOKEN"]
    except Exception:
        pass
    raise ValueError("Set FIGMA_ACCESS_TOKEN or configure AWS credentials")


def call_claude(prompt: str, system: str, model: str = "sonnet") -> dict:
    """Single Claude call via CLI. Returns {html, tokens, latency_s}."""
    full_prompt = f"{system}\n\n{prompt}"

    start = time.monotonic()
    result = subprocess.run(
        ["claude", "-p", "--model", model,
         "--output-format", "json", "--no-session-persistence"],
        input=full_prompt,
        capture_output=True, text=True, timeout=600,
    )
    elapsed = time.monotonic() - start

    if result.returncode != 0:
        print(f"ERROR: claude exit code {result.returncode}", file=sys.stderr)
        print(result.stderr[:500], file=sys.stderr)
        return {"html": "", "latency_s": elapsed, "error": result.stderr[:200]}

    try:
        data = json.loads(result.stdout)
        content = data.get("result", "")
    except json.JSONDecodeError:
        content = result.stdout

    return {"content": content, "latency_s": elapsed}


def parse_html(content: str) -> str:
    """Extract HTML from model response, stripping all markdown artifacts."""
    if "===HTML===" in content:
        html = content.split("===HTML===")[1]
        if "===END===" in html:
            html = html.split("===END===")[0]
        return _clean_html(html)
    if "```html" in content:
        html = content.split("```html")[1].split("```")[0]
        return _clean_html(html)
    if "<!DOCTYPE" in content:
        html = content[content.find("<!DOCTYPE"):]
        return _clean_html(html)
    if "<html" in content:
        html = content[content.find("<html"):]
        return _clean_html(html)
    return _clean_html(content)


def _clean_html(html: str) -> str:
    """Strip markdown backticks and artifacts from top and bottom."""
    html = html.strip()
    # Strip leading ```html or ```
    if html.startswith("```html"):
        html = html[7:]
    elif html.startswith("```"):
        html = html[3:]
    # Strip trailing ```
    if html.endswith("```"):
        html = html[:-3]
    return html.strip()


def main():
    parser = argparse.ArgumentParser(description="Figma-to-Site single-call pipeline")
    parser.add_argument("figma_url", help="Figma design URL")
    parser.add_argument("--model", default="sonnet", choices=["sonnet", "opus", "haiku"],
                        help="Claude model (default: sonnet)")
    parser.add_argument("--no-screenshot", action="store_true",
                        help="Skip Figma screenshot in prompt")
    parser.add_argument("--serve", action="store_true", default=True,
                        help="Start HTTP server and open in browser")
    parser.add_argument("--port", type=int, default=8877,
                        help="HTTP server port (default: 8877)")
    args = parser.parse_args()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = Path(f"runs/figma_pipeline/{timestamp}")
    out_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: Extract from Figma
    print(f"\n{'='*60}")
    print(f"  FIGMA-TO-SITE PIPELINE")
    print(f"  Model: Claude {args.model.title()}")
    print(f"  Output: {out_dir}")
    print(f"{'='*60}\n")

    print("Step 1/5: Extracting design from Figma API...", flush=True)
    t0 = time.monotonic()
    token = get_figma_token()
    extractor = FigmaDesignExtractor(access_token=token)
    ctx = extractor.extract(args.figma_url)
    t_extract = time.monotonic() - t0

    print(f"  Design: {ctx.file_name} — {ctx.node_name}")
    print(f"  Dimensions: {int(ctx.dimensions.get('width', 0))}x{int(ctx.dimensions.get('height', 0))}")
    print(f"  Sections: {len(ctx.sections)}")
    for s in ctx.sections:
        print(f"    [{s.semantic_role}] {s.name[:40]} — {len(s.texts)}t, {len(s.images)}i")
    print(f"  Total images: {len(ctx.raw_images)} ({sum(1 for i in ctx.raw_images if i.get('temp_url'))} with URLs)")
    print(f"  Typography: {ctx.typography.heading_font} / {ctx.typography.body_font}")
    print(f"  Colours: primary={ctx.colours.primary}, bg={ctx.colours.background}")
    print(f"  Time: {t_extract:.1f}s\n", flush=True)

    # Step 2: Build prompt
    print("Step 2/5: Building generation prompt...", flush=True)
    builder = DesignPromptBuilder()
    include_ss = not args.no_screenshot
    prompt_data = builder.build(ctx, include_screenshot=False)  # text-only for CLI
    prompt = prompt_data["user_content"]
    system = prompt_data["system_prompt"]
    print(f"  Prompt: {len(prompt):,} chars")
    print(f"  System: {len(system):,} chars\n", flush=True)

    # Save prompt for debugging
    (out_dir / "prompt.txt").write_text(prompt)
    (out_dir / "system.txt").write_text(system)

    # Step 3: Call Claude (single call)
    print(f"Step 3/5: Calling Claude {args.model.title()} (single call)...", flush=True)
    result = call_claude(prompt, system, model=args.model)

    if result.get("error"):
        print(f"  ERROR: {result['error']}", file=sys.stderr)
        sys.exit(1)

    content = result["content"]
    latency = result["latency_s"]
    print(f"  Response: {len(content):,} chars")
    print(f"  Complete: {'</html>' in content}")
    print(f"  Time: {latency:.1f}s\n", flush=True)

    # Save raw response
    (out_dir / "raw_response.txt").write_text(content)

    # Step 4: Parse and save HTML
    print("Step 4/5: Parsing HTML output...", flush=True)
    html = parse_html(content)

    if not html or len(html) < 100:
        print("  ERROR: No valid HTML in response", file=sys.stderr)
        print(f"  First 500 chars: {content[:500]}", file=sys.stderr)
        sys.exit(1)

    (out_dir / "index.html").write_text(html)
    has_closing = "</html>" in html
    has_style = "</style>" in html
    has_body = "</body>" in html
    print(f"  HTML: {len(html):,} chars")
    print(f"  Valid: </html>={has_closing}, </style>={has_style}, </body>={has_body}\n", flush=True)

    # Step 5: Summary & serve
    total_time = t_extract + latency
    print(f"{'='*60}")
    print(f"  PIPELINE COMPLETE")
    print(f"{'='*60}")
    print(f"  Design:    {ctx.file_name}")
    print(f"  Model:     Claude {args.model.title()}")
    print(f"  Sections:  {len(ctx.sections)}")
    print(f"  Images:    {len(ctx.raw_images)}")
    print(f"  Extract:   {t_extract:.1f}s")
    print(f"  Generate:  {latency:.1f}s")
    print(f"  Total:     {total_time:.1f}s")
    print(f"  Output:    {out_dir / 'index.html'}")
    print(f"{'='*60}\n")

    if args.serve:
        # Kill any existing server on the port
        subprocess.run(f"lsof -ti:{args.port} | xargs kill -9 2>/dev/null",
                       shell=True, capture_output=True)
        time.sleep(0.5)

        # Start server
        subprocess.Popen(
            [sys.executable, "-m", "http.server", str(args.port),
             "--directory", str(out_dir)],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        time.sleep(1)

        url = f"http://localhost:{args.port}/index.html"
        print(f"  Preview: {url}")
        subprocess.run(["open", url], capture_output=True)


if __name__ == "__main__":
    main()
