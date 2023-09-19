import pandas as pd
from pvlib.iotools.solcast import get_solcast_live, format_df
import pytest

@pytest.mark.parametrize("endpoint,params,json_response", [
    (   "live/radiation_and_weather",
        dict(
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
def test_get_solcast(requests_mock, endpoint, params, json_response):

    mock_url = f"https://api.solcast.com.au/data/{endpoint}?" \
               f"&latitude={params['latitude']}&longitude={params['longitude']}&" \
               f"output_parameters={params['output_parameters']}&format=json"

    requests_mock.get(mock_url, json=json_response)

    pd.testing.assert_frame_equal(
        get_solcast_live(**params),
        format_df(pd.DataFrame.from_dict(json_response[list(json_response.keys())[0]]))
    )