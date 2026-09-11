from pathlib import Path
from sec_edgar_downloader import Downloader
import html2text
import tempfile
import time


def ticket_year(ticket, years):
    for i in range(years):
        year = int(time.localtime().tm_year) - (i+1)
        downloader(ticket, years, year)

def downloader(ticket, years, year):
    report_path = Path(__file__).parent / "company_report" / f"{ticket}"

    report_path.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(dir=report_path) as temp_dir:
        save_path = Path(temp_dir)
        dl = Downloader(
            "AnalisisFinanciero",
            "jesuszahidmorenocalderon@gmail.com",
            save_path,
        )

        dl.get("10-K", ticket, limit=years, download_details=True)

        filings_dir = save_path / "sec-edgar-filings" / ticket / "10-K"
        html_files = [
            f
            for f in filings_dir.rglob("*")
            if f.is_file()
            and f.suffix.lower() in {".htm", ".html"}
            and not f.name.startswith("R")
        ]

        if not html_files:
            print("No se encontraron archivos .htm. Revisa la carpeta descargada.")
            return
        downloaded_html = max(html_files, key=lambda f: f.stat().st_size)
        primary_html = report_path / f"{ticket}_{year}{downloaded_html.suffix}"
        downloaded_html.replace(primary_html)
        print(f"HTML encontrado: {primary_html.name}")

        with open(primary_html, "r", encoding="utf-8") as f:
            html_content = f.read()

        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        h.body_width = 0

        markdown_text = h.handle(html_content)

        md_path = report_path / f"{ticket}_{year}.md"
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(markdown_text)

        print(f"Markdown generado con exito en:\n{md_path}")


if __name__ == "__main__":
    ticket_year("AAPL", 8) # Probar AAPL AMNZ
