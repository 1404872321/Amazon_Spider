from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from src.amazon_spider.io_utils import read_url_list, write_results
from src.amazon_spider.runner import run as run_crawler

app = typer.Typer(add_completion=False)
console = Console()


@app.command()
def crawl(
    input_file: Path = typer.Option(..., exists=True, readable=True, help="Path to input Excel/CSV file."),
    column: str = typer.Option("url", help="Column name in the input file that contains seller profile URLs."),
    sheet_name: Optional[str] = typer.Option(None, help="Sheet name if input is an Excel file."),
    output_file: Path = typer.Option(Path("output.xlsx"), help="Path to output file (.xlsx, .csv, or .json)."),
    max_workers: int = typer.Option(20, min=1, max=128, help="Maximum number of concurrent workers."),
    timeout: float = typer.Option(30.0, help="Per-request timeout in seconds."),
    max_retries: int = typer.Option(3, help="Max retries for HTTP requests."),
    backoff: float = typer.Option(0.5, help="Backoff factor for retries."),
    http_proxy: Optional[str] = typer.Option(None, help="HTTP proxy URL (e.g., http://user:pass@host:port)."),
    https_proxy: Optional[str] = typer.Option(None, help="HTTPS proxy URL (e.g., http://user:pass@host:port)."),
    socks_proxy: Optional[str] = typer.Option(None, help="SOCKS proxy URL (e.g., socks5h://host:port)."),
):
    """Crawl Amazon seller pages and export structured data."""
    try:
        urls = read_url_list(str(input_file), sheet_name=sheet_name, column=column)
    except Exception as exc:
        console.print(f"[red]Failed to read input: {exc}[/red]")
        raise typer.Exit(code=1)

    console.print(f"[bold]Loaded {len(urls)} URLs from[/bold] {input_file}")

    results = run_crawler(
        urls=urls,
        max_workers=max_workers,
        timeout=timeout,
        max_retries=max_retries,
        backoff_factor=backoff,
        http_proxy=http_proxy,
        https_proxy=https_proxy,
        socks_proxy=socks_proxy,
    )

    try:
        write_results(results, str(output_file))
    except Exception as exc:
        console.print(f"[red]Failed to write output: {exc}[/red]")
        raise typer.Exit(code=2)

    console.print(f"[green]Saved output to[/green] {output_file}")

    # Show a small preview table
    preview = results[: min(5, len(results))]
    table = Table(show_header=True, header_style="bold")
    for col in [
        "seller",
        "sellerName",
        "30daysRating",
        "90daysRating",
        "365daysRating",
        "lifetimeRating",
        "5starPercentage",
        "4starPercentage",
        "3starPercentage",
        "2starPercentage",
        "1starPercentage",
    ]:
        table.add_column(col)
    for r in preview:
        d = r.to_dict()
        table.add_row(
            d["seller"],
            d["sellerName"],
            d["30daysRating"],
            d["90daysRating"],
            d["365daysRating"],
            d["lifetimeRating"],
            d["5starPercentage"],
            d["4starPercentage"],
            d["3starPercentage"],
            d["2starPercentage"],
            d["1starPercentage"],
        )
    console.print(table)


if __name__ == "__main__":
    app()