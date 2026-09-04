from pathlib import Path
import tomllib


def test_vercel_uses_the_cairn_fastapi_application() -> None:
    config = tomllib.loads(Path("pyproject.toml").read_text())

    assert config["tool"]["vercel"]["entrypoint"] == "src.cairn_api.main:app"
