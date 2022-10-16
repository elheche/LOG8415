import requests
import time
from typing import Literal
from typing import Dict, Any, List
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat


def http_get(
        url: str, headers: Dict[str, Any] = None, proxies: Dict[str, Any] = None, timeout: int = None
             ) -> (int, Dict[str, Any], bytes):
    response = requests.get(url, headers=headers, proxies=proxies, timeout=timeout)

    response_json = None
    try:
        response_json = response.json()
    except Exception as e:
        # print(e)
        pass

    response_content = None
    try:
        response_content = response.content
    except Exception as e:
        print(e)

    return response.status_code, response_json, response_content


def run_test_scenario(
        test_type: Literal[1, 2], url: str, headers: Dict[str, Any] = None, proxies: Dict[str, Any] = None,
        timeout: int = None
) -> List[int]:
    status_codes = []
    if test_type == 1:
        print("Running Test Scenario 1: 1000 GET Requests Sequentially...")
        for i in range(1000):
            status_code, _, _ = http_get(url, headers, proxies, timeout)
            status_codes.append(status_code)
    else:
        print("Running Test Scenario 2: 500 GET Requests, then one minute sleep, followed by 1000 GET Requests...")
        for i in range(500):
            status_code, _, _ = http_get(url, headers, proxies, timeout)
            status_codes.append(status_code)
        time.sleep(60)
        print("1 minute sleep")
        for i in range(1000):
            status_code, _, _ = http_get(url, headers, proxies, timeout)
            status_codes.append(status_code)
    return status_codes


def run_test_scenario_with_multithreading(
        scenarios: List[int], url: str, headers: Dict[str, Any] = None, proxies: Dict[str, Any] = None,
        timeout: int = None
) -> (List[int], float):
    t1 = time.time()
    results = []
    executor = ThreadPoolExecutor(max_workers=2)
    for result in executor.map(run_test_scenario, scenarios, repeat(url), repeat(headers), repeat(proxies),
                               repeat(timeout)):
        results.append(result)
    t2 = time.time()
    t = t2 - t1
    return results, t


def main():
    print('--------------------')

    # URL list
    # urls = ["https://www.google.com/" for i in range(2)]
    urls = ["http://log8415-lab1-elb-1921159422.us-east-1.elb.amazonaws.com/cluster1",
            "http://log8415-lab1-elb-1921159422.us-east-1.elb.amazonaws.com/cluster2"]
    # headers
    headers = {"Content-Type": "application/json"}

    # Running Test scenario for Cluster 1
    results_cluster_1, time_cluster_1 = run_test_scenario_with_multithreading(scenarios=[1, 2], url=urls[0],
                                                                              headers=headers)

    # Running Test scenario for Cluster 2
    results_cluster_2, time_cluster_2 = run_test_scenario_with_multithreading(scenarios=[1, 2], url=urls[1],
                                                                              headers=headers)


if __name__ == "__main__":
    main()
