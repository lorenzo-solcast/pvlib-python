""" Functions to access data from the Solcast API.
.. codeauthor:: Solcast<modelling@solcast.com.au>
"""
import requests
import pandas as pd

BASE_URL = "https://api.solcast.com.au/data"


# TODO: https://pvlib-python.readthedocs.io/en/stable/user_guide/variables_style_rules.html
PARAMETERS_MAPPING = dict(

)


def get_solcast(
        endpoint,
        api_key,
        **kwargs
):
    """retrieves weather, irradiance and power data from the Solcast API
    and returns it into a Pandas DataFrame.

    Parameters
    ----------
    endpoint : str
        one of Solcast API endpoint:
            - live/radiation_and_weather
            - live/rooftop_pv_power
            - live/advanced_pv_power
            - historic/radiation_and_weather
            - historic/rooftop_pv_power
            - forecast/radiation_and_weather
            - forecast/rooftop_pv_power
            - forecast/advanced_pv_power
            - tmy/radiation_and_weather
            - tmy/rooftop_pv_power

    api_key : str
        To access Solcast data you will need a commercial API key: https://toolkit.solcast.com.au/register.

    kwargs : dict
        the parameters to pass to the api. For a full list of parameters for each endpoint
        see the API docs: https://docs.solcast.com.au/


    Examples
    --------
    - Making a request for live weather data:
        get_solcast(
            endpoint="live/radiation_and_weather",
            latitude=-33.856784,
            longitude=151.215297,
            output_parameters='dni,ghi',
            api_key="your-key"
        )

    - Making a request for historic rooftop power
        get_solcast(
            endpoint="historic/rooftop_pv_power",
            latitude=-33.856784,
            longitude=151.215297,
            start="2022-10-25T12:00",
            end="2022-10-26T12:00",
            api_key="your-key"
        )

    - making a request for forecast advanced pv power
        get_solcast(
            endpoint="forecast/advanced_pv_power",
            resource_id="5f86-4c8f-2cb3-0215",
            hours=3,
            api_key="your-key"
        )

    - making a request form TMY data
        get_solcast(
            endpoint="tmy/radiation_and_weather",
            latitude=-33.856784,
            longitude=151.215297,
            output_parameters='air_temp',
            api_key="your-key"
        )
    """

    params = dict(
        format="json",
        **kwargs
    )

    response = requests.get(
        url= '/'.join([BASE_URL, endpoint]),
        params=params,
        headers={"Authorization": f"Bearer {api_key}"}
    )

    if response.status_code == 200:
        j = response.json()
        print(j)
        df = pd.DataFrame.from_dict(j[list(j.keys())[0]])
        return df
    else:
        raise Exception(response.json())