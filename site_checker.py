import requests
import datetime
import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('site_checker.log'),
        logging.StreamHandler()
    ]
)

def site_checker(url: str, timeout: int = 10) -> dict:
    """
    Check if a website is online and return status information.
    """
    try:
        start_time = datetime.datetime.now()
        response = requests.get(url, timeout=timeout)
        end_time = datetime.datetime.now()

        response_time = (end_time - start_time).total_seconds()

        result = {
            'url': url,
            'timestamp': datetime.datetime.now().isoformat(),
            'success': response.status_code == 200,
            'status_code': response.status_code,
            'response_time': response_time,
            'error': None
        }

        if response.status_code == 200:
            logging.info(f" Website is UP - Status: {response.status_code}, Response time: {response_time:.2f}s")
        else:
            logging.warning(f" Website returned status {response.status_code} - Response time: {response_time:.2f}s")

        return result
    
    except requests.exceptions.ConnectionError:
        error_msg = "Connection error - Website might be down"
        logging.error(f" {error_msg}")
        return {
            'url': url,
            'timestamp': datetime.datetime.now().isoformat(),
            'success': False,
            'status_code': None,
            'response_time': None,
            'error': error_msg
        }
    
    except requests.exceptions.Timeout:
        error_msg = f"Request timed out after {timeout} seconds"
        logging.error(f" {error_msg}")
        return{
            'url': url,
            'timestamp': datetime.datetime.now().isoformat(),
            'success': False,
            'status_code': None,
            'response_time': None,
            'error': error_msg
        }
    
    except requests.exceptions.RequestException as e:
        error_msg = f"Request failed: {str(e)}"
        logging.error(f" {error_msg}")
        return{
            'url': url,
            'timestamp': datetime.datetime.now().isoformat(),
            'success': False,
            'status_code': None,
            'response_time': None,
            'error': error_msg
        }
    
# Comment this section out when you are finished testing locally

# if __name__ == "__main__":

#     test_url = "https://curiosityincode.com/"

#     print("Starting website check...")
#     result = site_checker(test_url)

#     print("\n--- TEST RESULTS ---")
#     print(f"URL: {result['url']}")
#     print(f"Time: {result['timestamp']}")
#     print(f"Success: {result['success']}")

#     if result['success']:
#         print(f"Status Code: {result['status_code']}")
#         print(f"Response Time: {result['response_time']:.2f} seconds")
#     else:
#         print(f"Error: {result['error']}")

#     print("\nCheck the 'site_checker.log' file for logged messages!")

# Comment this section out when you are finished testing locally

if __name__ == "__main__":
    test_sites = {
        "Primary Domain":  "https://curiosityincode.com/",
        "Google": "https://google.com",
        "GitHub": "https://github.com",
        "Bad Url": "https://this-definitely-does-not-exist.com"
    }

    print("Starting website checks for multiple sites...")
    print("=" * 50)

    all_results = []

    for site_name, url in test_sites.items():
        print(f"\n Checking {site_name}...")
        result = site_checker(url)
        all_results.append(result)

        if result['success']:
            print(f" {site_name} is UP ({result['response_time']:.2f}s)")
        else:
            print(f" {site_name} is DOWN - {result['error']}")

    print("\n" + "=" * 50)
    print("SUMMARY REPORT")
    print("=" * 50)

    up_count = sum(1 for r in all_results if r['success'])
    down_count = len(all_results) - up_count

    print(f"Total sites checked: {len(all_results)}")
    print(f"Sites UP: {up_count}")
    print(f"Sites DOWN: {down_count}")

    if down_count > 0:
        print(f"\n Sites that are DOWN:")
        for result in all_results:
            if not result['success']:
                print(f"   - {result['url']}: {result['error']}")
    
    print(f"\n. Check the 'site_checker.log' file for detailed logged messages!")