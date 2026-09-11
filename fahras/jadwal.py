#!/usr/bin/env python3
"""Validates fahras/tarjamat.json against fahras/mukhattat.json and rewrites the
index tables in README.md and README.ar.md between the fahras markers.

    python3 fahras/jadwal.py            # validate, then rewrite both READMEs
    python3 fahras/jadwal.py --check    # validate only, exit 1 on any problem

Needs only the standard library; if the `jsonschema` package is installed the
schema is applied in full, otherwise the structural checks below still run.
"""
import json, re, sys, collections
from pathlib import Path

JIDHR = Path(__file__).resolve().parent.parent
FAHRAS = JIDHR / "fahras" / "tarjamat.json"
MUKHATTAT = JIDHR / "fahras" / "mukhattat.json"

EN = {
    "taghtiya": {"kamila": "full", "wajiha": "interface", "hiwar": "dialogue", "juziya": "partial", "ghayr_musarraha": "not stated"},
    "tareeqa": {"bashariya_kamila": "human", "aaliya_thum_bashariya": "machine, human-reviewed", "aaliya_faqat": "machine", "ghayr_musarraha": "not stated"},
    "tawzee": {"majjani": "free", "madfua": "paid", "vip": "subscription"},
    "hala": {"nashita": "released", "awwaliya": "initial", "qayd_altatwir": "in progress", "mahjura": "discontinued"},
    "arabiya": {"naam": "yes", "la": "no", "ghayr_maruf": "?"},
    "shakl": {"istibdal_malafat": "file replacement", "pak": "pak", "bepinex": "BepInEx", "xunity_autotranslator": "XUnity AutoTranslator", "modengine2": "ModEngine2", "owml": "OWML",
              "jotunn": "Jötunn", "munassib": "installer", "khatt": "font", "tashkil": "shaping/RTL", "istibdal_lugha": "language slot", "workshop": "Workshop", "dublaja": "dub",
              "tatbeeq_khass": "proprietary app", "ghayr_musarrah": "not stated"},
    "mudif": {"steam_workshop": "Steam Workshop", "nexusmods": "Nexus Mods", "thunderstore": "Thunderstore", "gamebanana": "GameBanana", "github": "GitHub", "itch": "itch.io",
              "outerwildsmods": "outerwildsmods.com", "mawqi_alfariq": "team site", "mudawwana": "blog"},
}
AR = {
    "taghtiya": {"kamila": "كاملة", "wajiha": "الواجهة", "hiwar": "الحوار", "juziya": "جزئية", "ghayr_musarraha": "غير مصرّح بها"},
    "tareeqa": {"bashariya_kamila": "بشرية", "aaliya_thum_bashariya": "آلية راجعها إنسان", "aaliya_faqat": "آلية", "ghayr_musarraha": "غير مصرّح بها"},
    "tawzee": {"majjani": "مجاني", "madfua": "مدفوع", "vip": "اشتراك"},
    "hala": {"nashita": "منشورة", "awwaliya": "أولية", "qayd_altatwir": "قيد العمل", "mahjura": "متوقفة"},
    "arabiya": {"naam": "نعم", "la": "لا", "ghayr_maruf": "؟"},
    "shakl": {"istibdal_malafat": "استبدال ملفات", "pak": "pak", "bepinex": "BepInEx", "xunity_autotranslator": "XUnity AutoTranslator", "modengine2": "ModEngine2", "owml": "OWML",
              "jotunn": "Jötunn", "munassib": "مثبّت", "khatt": "خط", "tashkil": "تشكيل/اتجاه", "istibdal_lugha": "خانة لغة أخرى", "workshop": "الورشة", "dublaja": "دبلجة",
              "tatbeeq_khass": "تطبيق خاص", "ghayr_musarrah": "غير مصرّح به"},
    "mudif": {"steam_workshop": "ورشة Steam", "nexusmods": "Nexus Mods", "thunderstore": "Thunderstore", "gamebanana": "GameBanana", "github": "GitHub", "itch": "itch.io",
              "outerwildsmods": "outerwildsmods.com", "mawqi_alfariq": "موقع الفريق", "mudawwana": "مدونة"},
}


def ihmal(s):
    return (s or "").replace("|", "\\|").replace("\n", " ")


def tahaqquq(doc, mukhattat):
    """Structural checks that hold with or without the jsonschema package."""
    akhta = []
    ids = [t["muarrif"] for t in doc["tarjamat"]]
    for i, n in collections.Counter(ids).items():
        if n > 1: akhta.append(f"duplicate muarrif {i}")
    firaq = {f["muarrif"] for f in doc["firaq"]}
    for t in doc["tarjamat"]:
        if t["fariq"] is not None and t["fariq"] not in firaq: akhta.append(f"{t['muarrif']}: unknown fariq {t['fariq']}")
        for r in [t["rabt"], t["tahaqquq"]["rabt"], *t["rawabit_ukhra"]]:
            if not re.match(r"^https://\S+$", r): akhta.append(f"{t['muarrif']}: not https: {r}")
        if t["rukhsa"]["naw"] == "spdx" and not t["rukhsa"]["muarrif"]: akhta.append(f"{t['muarrif']}: spdx licence without identifier")
    try:
        import jsonschema
        v = jsonschema.Draft202012Validator(mukhattat, format_checker=jsonschema.FormatChecker())
        for k in sorted(v.iter_errors(doc), key=lambda e: list(e.path)):
            akhta.append(f"schema: {'/'.join(str(p) for p in k.path)}: {k.message[:160]}")
    except ImportError:
        print("jsonschema not installed; schema not applied, structural checks only", file=sys.stderr)
    return akhta


def safaf(doc, L, ar):
    firaq = {f["muarrif"]: f for f in doc["firaq"]}
    groups = collections.OrderedDict()
    for t in doc["tarjamat"]:
        key = t["fariq"] or "_"
        groups.setdefault(key, []).append(t)
    order = sorted(groups, key=lambda k: (k == "_", -len(groups[k]), k))
    out = []
    head = ("| اللعبة | Steam | عربية رسمية | المؤلّف | المضيف | التغطية | الطريقة | الشكل التقني | الرخصة | التوزيع | الحالة | آخر تاريخ | فُحص |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|"
            if ar else "| Game | Steam | Official Arabic | Author | Host | Coverage | Method | Technical form | Licence | Distribution | Status | Latest date | Checked |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for key in order:
        rows = groups[key]
        if key == "_":
            title = "أفراد وفرق بلا صفحة فريق" if ar else "Individuals and teams without a team page"
        else:
            f = firaq[key]
            title = f"[{f['ism_arabi'] or f['ism']}]({f['rabt']})" if ar else f"[{f['ism']}]({f['rabt']})"
        out.append(f"<details>\n<summary><strong>{title}</strong> — {len(rows)}</summary>\n\n{head}")
        for t in rows:
            luba = f"[{ihmal(t['luba']['ism'])}]({t['rabt']})"
            steam = str(t["steam_appid"]) if t["steam_appid"] else "—"
            arab = L["arabiya"][(t["arabiya_rasmiya"] or {}).get("hala", "ghayr_maruf")]
            rukhsa = t["rukhsa"]["muarrif"] if t["rukhsa"]["naw"] == "spdx" else ("stated" if not ar else "مذكورة") if t["rukhsa"]["naw"] == "musarraha" else ("not stated" if not ar else "غير مذكورة")
            date = t["akhir_tahdith"] or t["waqt_alnashr"] or "—"
            out.append(f"| {luba} | {steam} | {arab} | {ihmal(t['muallif'])[:60]} | {L['mudif'][t['mudif']]} | {L['taghtiya'][t['taghtiya']]} | {L['tareeqa'][t['tareeqa']]} | "
                       f"{', '.join(L['shakl'][s] for s in t['shakl_tiqani'])} | {rukhsa} | {L['tawzee'][t['tawzee']]} | {L['hala'][t['hala']]} | {date} | {t['tahaqquq']['waqt']} |")
        out.append("\n</details>\n")
    return "\n".join(out)


def ihsa(doc, ar):
    t = doc["tarjamat"]; c = collections.Counter
    n = len(t); firaq = len(doc["firaq"])
    alab = len({(x["steam_appid"] or x["luba"]["ism"].lower()) for x in t})
    rasmi = sum(1 for x in t if (x["arabiya_rasmiya"] or {}).get("hala") == "naam")
    majjani = sum(1 for x in t if x["tawzee"] == "majjani")
    bashari = sum(1 for x in t if x["tareeqa"] == "bashariya_kamila")
    aali = sum(1 for x in t if x["tareeqa"] in ("aaliya_faqat", "aaliya_thum_bashariya"))
    rukhas = sum(1 for x in t if x["rukhsa"]["naw"] != "ghayr_musarraha")
    if ar:
        return (f"**{n}** تعريبًا لـ **{alab}** لعبة من **{firaq}** فريقًا وعددٍ من الأفراد. {majjani} منها مجاني، و{n - majjani} مدفوع أو باشتراك. "
                f"{bashari} تصرّح صفحته بترجمة بشرية أو تسمّي مترجميها، و{aali} تصرّح بترجمة آلية كليًا أو جزئيًا، والباقي لا يقول. "
                f"{rukhas} فقط تذكر رخصة أو شرط استعمال؛ الباقي لا يذكر شيئًا. {rasmi} منها للعبة صار لها عربية رسمية بعد ذلك بحسب Steam.")
    return (f"**{n}** translations of **{alab}** games from **{firaq}** teams plus individuals. {majjani} are free; {n - majjani} are sold or subscription-only. "
            f"{bashari} state a human translation or credit named translators, {aali} state machine translation in whole or in part, the rest do not say. "
            f"Only {rukhas} state any licence or terms of use. {rasmi} target a game that Steam now lists with official Arabic.")


def uktub(masar, doc, L, ar):
    nass = masar.read_text(encoding="utf-8")
    a, b = "<!-- fahras:start -->", "<!-- fahras:end -->"
    i, j = nass.index(a), nass.index(b)
    body = f"{a}\n{ihsa(doc, ar)}\n\n{safaf(doc, L, ar)}\n{b}"
    masar.write_text(nass[:i] + body + nass[j + len(b):], encoding="utf-8")


def main():
    doc = json.loads(FAHRAS.read_text(encoding="utf-8"))
    mukhattat = json.loads(MUKHATTAT.read_text(encoding="utf-8"))
    akhta = tahaqquq(doc, mukhattat)
    for k in akhta: print("FAIL", k)
    print(f"{len(doc['firaq'])} teams, {len(doc['tarjamat'])} translations, {len(akhta)} problem(s)")
    if akhta: sys.exit(1)
    if "--check" in sys.argv: return
    uktub(JIDHR / "README.md", doc, EN, False)
    uktub(JIDHR / "README.ar.md", doc, AR, True)
    print("README.md and README.ar.md tables rewritten")


if __name__ == "__main__":
    main()
