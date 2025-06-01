import re

class FFIndustryParser:
    def __init__(self, text: str):
        self.text = text
        self.sic_dict = self._parse_ff_industry(text)

    @staticmethod
    def _parse_ff_industry(text: str) -> dict:
        result = {}
        current_section_id = None
        current_section_full_description = ""

        for raw_line in text.splitlines():
            line = raw_line.rstrip()

            if not line.strip():
                continue

            match_section = re.match(r'^\s*(\d+)\s+([A-Za-z&]+)\s+(.+)$', line)
            if match_section:
                sec_id, name, description_text = match_section.groups()
                current_section_id = sec_id
                current_section_full_description = description_text.strip()
                result[sec_id] = {
                    "name": name.strip(),
                    "description": current_section_full_description,
                    "ranges": []
                }
                continue

            if current_section_id:
                match_new_range = re.match(r'^\s*(\d{4})-(\d{4})\s*$', line)
                if match_new_range:
                    start, end = match_new_range.groups()
                    result[current_section_id]["ranges"].append({
                        "sic_start": int(start),
                        "sic_end": int(end),
                        "label": current_section_full_description
                    })
                    continue

                match_old_range = re.match(r'^\s*(\d{4})-(\d{4})\s+(.+?)\s*$', line)
                if match_old_range:
                    start, end, label_text = match_old_range.groups()
                    result[current_section_id]["ranges"].append({
                        "sic_start": int(start),
                        "sic_end": int(end),
                        "label": label_text.strip()
                    })
                    continue

        return result

    def map_sic(self, sic: int) -> int | None:
        for ff_code, section in self.sic_dict.items():
            for r in section["ranges"]:
                if r["sic_start"] <= sic <= r["sic_end"]:
                    return int(ff_code)
        return None

    def get_dict(self) -> dict:
        return self.sic_dict

if __name__ == "__main__":
    with open('Siccodes12.txt', 'r') as f:
        ff_text = f.read()

    parser = FFIndustryParser(ff_text)
    industry_code = parser.map_sic(2852)
    print(industry_code)