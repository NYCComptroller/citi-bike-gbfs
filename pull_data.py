from requests import Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import json
from os import makedirs

makedirs('data', exist_ok=True)

# copying a retry strategy from: https://www.peterbe.com/plog/best-practice-with-retries-with-requests
def requests_retry_session(
    retries=5,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

stations_get = requests_retry_session().get('https://gbfs.citibikenyc.com/gbfs/en/station_information.json')
status_get = requests_retry_session().get('https://gbfs.citibikenyc.com/gbfs/en/station_status.json')

status_get.raise_for_status() # should raise error and end execution if there was a connection error

status_json = status_get.json() # should raise error if the json is unparsable 

timestamp = status_json['last_updated']

with open(f"data/{timestamp}_stations.json", 'w') as stations_file:
    json.dump(stations_get.json(), stations_file)

with open(f"data/{timestamp}_status.json", 'w') as status_file:
    json.dump(status_json, status_file)