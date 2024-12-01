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
