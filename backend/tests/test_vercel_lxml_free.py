from pathlib import Path
import tomllib


def test_vercel_fastapi_runtime_avoids_lxml_build_dependency() -> None:
    config = tomllib.loads(Path("pyproject.toml").read_text())
    source = Path("src/cairn_api/main.py").read_text()

    assert all("lxml" not in dependency.lower() for dependency in config["project"]["dependencies"])
    assert 'BeautifulSoup(response.text, "html.parser")' in source
    assert 'BeautifulSoup(response.text, "lxml")' not in source
