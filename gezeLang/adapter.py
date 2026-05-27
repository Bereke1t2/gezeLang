# adapter.py — AdapterRegistry: discovers and loads language adapters
import json
from pathlib import Path

class GezeLangError(Exception):
    """Base error — all user-facing messages must be in Amharic."""
    pass

class GezeLangAdapterError(GezeLangError):
    pass

class Adapter:
    def __init__(self, lang: str, amharic_to_python: dict, python_to_amharic: dict):
        self.lang = lang
        self._a2p = amharic_to_python   # {"ስራ": "def", ...}
        self._p2a = python_to_amharic   # {"def": "ስራ", ...}

    @classmethod
    def load(cls, adapter_dir: Path) -> 'Adapter':
        """Load adapter from a directory containing keywords.json."""
        kw_path = adapter_dir / 'keywords.json'
        try:
            with open(kw_path, encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            raise GezeLangAdapterError(
                f"ስህተት[E004] keywords.json ፋይል ተሳስቷል — JSON ልክ አይደለም: {kw_path}"
            )
        # keywords.json has flat structure: {"amharic_word": "python_keyword", ...}
        a2p = {k: v for k, v in data.items() if not k.startswith('$')}
        p2a = {v: k for k, v in a2p.items()}
        return cls(lang=adapter_dir.name, amharic_to_python=a2p, python_to_amharic=p2a)

    def to_python_keyword(self, token: str) -> str | None:
        """O(1) lookup. Returns Python keyword or None if not a keyword."""
        return self._a2p.get(token)

    def to_amharic(self, python_kw: str) -> str:
        """Reverse lookup for error messages."""
        return self._p2a.get(python_kw, python_kw)


class AdapterRegistry:
    _adapters: dict[str, Adapter] = {}

    @classmethod
    def discover(cls, adapters_dir: str | Path):
        """Scan adapters/ subdirectories for keywords.json files."""
        d = Path(adapters_dir)
        if not d.exists():
            return
        for sub in d.iterdir():
            if sub.is_dir() and (sub / 'keywords.json').exists():
                cls._adapters[sub.name] = Adapter.load(sub)

    @classmethod
    def get(cls, lang: str) -> Adapter:
        if lang not in cls._adapters:
            available = ', '.join(cls._adapters.keys()) or 'ምንም የለም'
            raise GezeLangAdapterError(
                f"ስህተት[E003] ቋንቋ '{lang}' አልተገኘም። "
                f"የሚገኙ ቋንቋዎች: {available}"
            )
        return cls._adapters[lang]

    @classmethod
    def list_langs(cls) -> list[str]:
        return list(cls._adapters.keys())
