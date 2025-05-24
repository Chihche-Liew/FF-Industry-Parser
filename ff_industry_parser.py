import re

class FFIndustryParser:
    def __init__(self, text: str):
        self.text = text
        self.sic_dict = self._parse_ff_industry(text)

    @staticmethod
    def _parse_ff_industry(text: str) -> dict:
        result = {}
        current_section = None

        for line in text.splitlines():
            line = line.rstrip()
            if not line.strip():
                continue

            match_section = re.match(r'^\s*(\d*)\s+([A-Za-z&]+)\s+(.+)$', line)
            if match_section:
                sec_id, name, description = match_section.groups()
                current_section = sec_id
                result[sec_id] = {
                    "name": name,
                    "description": description,
                    "ranges": []
                }
                continue

            match_range = re.match(r'^\s*(\d{4})-(\d{4})\s+(.+)$', line)
            if match_range and current_section:
                start, end, label = match_range.groups()
                result[current_section]["ranges"].append({
                    "sic_start": int(start),
                    "sic_end": int(end),
                    "label": label.strip()
                })

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
    with open('Siccodes49.txt', 'r') as f:
        ff_text = f.read()

    parser = FFIndustryParser(ff_text)
    industry_code = parser.map_sic(2852)
    print(industry_code)