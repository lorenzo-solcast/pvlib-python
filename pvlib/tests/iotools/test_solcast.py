import pandas as pd
from pvlib.iotools import get_solcast
import pytest

@pytest.mark.parametrize("params,json_response", [
    (
        dict(
            endpoint="live/radiation_and_weather",
            api_key="1234",
            latitude = -33.856784,
            longitude = 151.215297,
            output_parameters = 'dni,ghi'
        ),
        {
        'estimated_actuals':
            [{'dni': 836, 'ghi': 561, 'period_end': '2023-09-18T05:00:00.0000000Z', 'period': 'PT30M'},
             {'dni': 866, 'ghi': 643, 'period_end': '2023-09-18T04:30:00.0000000Z', 'period': 'PT30M'},
             {'dni': 890, 'ghi': 713, 'period_end': '2023-09-18T04:00:00.0000000Z', 'period': 'PT30M'},
             {'dni': 909, 'ghi': 768, 'period_end': '2023-09-18T03:30:00.0000000Z', 'period': 'PT30M'}]
        }
    )
])
def test_get_solcast(requests_mock, params, json_response):

    mock_url = f"https://api.solcast.com.au/data/{params['endpoint']}?" \
               f"&latitude={params['latitude']}&longitude={params['longitude']}&" \
               f"output_parameters={params['output_parameters']}&format=json"

    requests_mock.get(mock_url, json=json_response)

    res = get_solcast(**params)
    pd.testing.assert_frame_equal(res, pd.DataFrame.from_dict(json_response[list(json_response.keys())[0]]))