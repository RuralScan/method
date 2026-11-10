"""Render the verified Markdown guides as one offline, printable document."""

from pathlib import PurePosixPath
import re
from urllib.parse import urlsplit
from xml.etree import ElementTree as ET

from markdown_it import MarkdownIt


# These handbook pages accompany the original six practice guides.
HANDBOOK = "https://github.com/RuralScan/method/blob/c4b3b61e61453a4c7e9119baceb11ca6be26a9f0/handbook/"
FAMILY_DETAILS = re.compile(
    r"^<details>\s*<summary>([^<]+)</summary>\s*(.*?)^</details>\s*$",
    re.MULTILINE | re.DOTALL,
)
DOWNLOAD_LINK = "[Download the print edition](rural-scan-cookbook.html)"


def document_link(href, anchors):
    if href in anchors:
        return f"#{anchors[href]}"
    if re.fullmatch(r"\.\./handbook/[a-z0-9-]+\.md", href):
        return HANDBOOK + href.removeprefix("../handbook/")
    if urlsplit(href).scheme == "https":
        return href
    raise ValueError(f"Cookbook link has no standalone destination: {href}")


def label_table(table):
    for heading in table.findall("./thead/tr/th"):
        heading.set("scope", "col")
        match = re.match(r"^(T[0-7]E?)\b", heading.text or "")
        if match:
            table_id = match.group()
            label = ET.Element("span", {"data-ruralscan-table": table_id})
            label.text = table_id
            label.tail = heading.text[match.end() :]
            heading.text = None
            heading.insert(0, label)
    for row in table.findall("./tbody/tr"):
        label = row.find("td")
        if label is not None:
            label.tag = "th"
            label.set("scope", "row")


def chapter(parser, source, name, anchors):
    # The guides use one disclosure for lookup IDs. Its contents must always
    # print, even in browsers which suppress closed disclosure text.
    details = FAMILY_DETAILS.search(source)
    if "<details>" in source and not details:
        raise ValueError(f"Unrecognised family disclosure in {name}")
    if details:
        source = source[: details.start()] + source[details.end() :]
    if name == "README.md":
        source = "\n".join(
            line for line in source.splitlines() if line != DOWNLOAD_LINK
        )

    section = ET.fromstring("<section>" + parser.render(source) + "</section>")
    section.set("id", anchors[name])
    section.set("class", "overview" if name == "README.md" else "practice")
    heading = section.find("h1")
    if heading is None:
        raise ValueError(f"Cookbook guide has no title: {name}")
    for subheading in section.iter("h2"):
        subheading.tag = "h3"
    heading.tag = "h2"
    heading.set("class", "title")
    title_id = f"{anchors[name]}-title"
    heading.set("id", title_id)
    section.set("aria-labelledby", title_id)
    if details:
        # Keep lookup IDs beside the family definitions in the expanded edition.
        family = ET.Element("section", {"class": "family-ids"})
        family_table = section.find("table")
        if family_table is None:
            raise ValueError(f"Family disclosure has no family table in {name}")
        section.insert(list(section).index(family_table) + 1, family)
        ET.SubElement(family, "h3").text = details.group(1)
        family.extend(
            ET.fromstring("<div>" + parser.render(details.group(2)) + "</div>")
        )

    for link in section.iter("a"):
        link.set("href", document_link(link.attrib["href"], anchors))
    for paragraph in section.iter("p"):
        if paragraph.find("./a[@href='#overview']") is not None:
            paragraph.set("class", "back-link")
    if section.find(".//img") is not None:
        raise ValueError(f"Offline cookbook guide references an image: {name}")
    for table in section.iter("table"):
        label_table(table)
    return section


def render_edition(rendered: dict[str, str], table_css: str, edition_css: str) -> str:
    """Combine the same pages used by the Markdown publication; preserve their order."""
    names = ["README.md", *sorted(name for name in rendered if name != "README.md")]
    anchors = {name: PurePosixPath(name).stem for name in names}
    anchors["README.md"] = "overview"
    # XHTML output lets the standard library transform heading, table and link
    # elements without parsing HTML with regular expressions. Raw HTML stays escaped.
    parser = MarkdownIt("commonmark", {"html": False, "xhtmlOut": True}).enable("table")
    document = ET.Element("html", {"lang": "en"})
    head = ET.SubElement(document, "head")
    ET.SubElement(head, "meta", {"charset": "utf-8"})
    ET.SubElement(
        head,
        "meta",
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
    )
    title = "Rural Scan recipe cookbook"
    ET.SubElement(head, "title").text = title
    ET.SubElement(head, "style").text = (
        "\n" + table_css.strip() + "\n" + edition_css.strip() + "\n"
    )
    body = ET.SubElement(document, "body")
    header = ET.SubElement(body, "header", {"class": "edition-header"})
    ET.SubElement(header, "h1").text = title
    main = ET.SubElement(body, "main")
    for name in names:
        main.append(chapter(parser, rendered[name], name, anchors))
    return (
        "<!doctype html>\n"
        + ET.tostring(document, encoding="unicode", method="html")
        + "\n"
    )
