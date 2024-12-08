import json


def parse_json(result_json):
    return json.loads(result_json)


def format_results(results):
    return [
        {
            "ID": result.id,
            "Name": result.user_name,
            "Test": result.test_type,
            "Result": parse_json(result.result),
            "Date": result.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for result in results
    ]


class TestResults:
    def __init__(self):
        self.pvt_before = []
        self.pvt_after = []
        self.nasa_tlx = {}

    def add_pvt_before(self, reaction_time):
        self.pvt_before.append(reaction_time)
        print(213)

    def add_pvt_after(self, reaction_time):
        self.pvt_after.append(reaction_time)

    def add_nasa_tlx(self, question, response):
        self.nasa_tlx[question] = response

    def get_summary(self):
        if not self.pvt_before and not self.pvt_after and not self.nasa_tlx:
            return "Нет данных для отображения."

        summary = "Результаты PVT:\n"
        if self.pvt_before:
            avg_before = sum(self.pvt_before) / len(self.pvt_before)
            summary += f"- Среднее время реакции (до): {avg_before:.3f} сек\n"
        if self.pvt_after:
            avg_after = sum(self.pvt_after) / len(self.pvt_after)
            summary += f"- Среднее время реакции (после): {avg_after:.3f} сек\n"

        summary += "\nРезультаты NASA-TLX:\n"
        for question, response in self.nasa_tlx.items():
            summary += f"- {question}: {response}/20\n"

        return summary

