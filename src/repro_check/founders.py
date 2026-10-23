"""The eight Diversity Outbred founder strains and their one-letter codes."""

from __future__ import annotations

FOUNDERS = {
    "A": "AJ",
    "B": "B6",
    "C": "129",
    "D": "NOD",
    "E": "NZO",
    "F": "CAST",
    "G": "PWK",
    "H": "WSB",
}
FOUNDER_CODES = tuple(FOUNDERS)

# Accepted spellings, upper-cased, mapped to the code.
_ALIASES = {code: code for code in FOUNDERS}
_ALIASES.update({name.upper(): code for code, name in FOUNDERS.items()})
_ALIASES.update({
    "A/J": "A", "C57BL/6J": "B", "B6J": "B", "129S1": "C", "129S1/SVIMJ": "C",
    "NOD/SHILTJ": "D", "NZO/HILTJ": "E", "CAST/EIJ": "F", "PWK/PHJ": "G", "WSB/EIJ": "H",
})


def normalise_founders(names: list[str], where: str = "") -> list[str]:
    """Map founder names or codes to one-letter codes, rejecting unknown ones."""
    out = []
    for n in names:
        code = _ALIASES.get(str(n).strip().upper())
        if code is None:
            raise ValueError(f"{where}: unknown founder {n!r}; use one of "
                             + ", ".join(f"{c} ({FOUNDERS[c]})" for c in FOUNDER_CODES))
        if code not in out:
            out.append(code)
    return out


def label(codes: list[str]) -> str:
    return ", ".join(FOUNDERS[c] for c in codes) if codes else "—"
