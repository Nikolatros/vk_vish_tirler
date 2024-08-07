from dataclasses import dataclass
import requests
import pandas as pd
from config import TOKEN_USER, OWNER_ID, VERSION


@dataclass
class Parser:
    """Parse posts from vk group"""

    __TOKEN_USER: str = TOKEN_USER
    __OWNER_ID: int = OWNER_ID
    __VERSION: float | str = VERSION

    def _response_process(eslf, response: dict) -> pd.DataFrame:
        """Porcess response from vk api.
        Extract counts from embedded stats dicts.
        Return truncated pd.DataFrame with only essential columns

        Args:
            response (dict): response from vk.api (wall.get)

        Raises:
            AssertionError: Validate response

        Returns:
            pd.DataFrame: Processed response
        """

        # Convert to json
        response = response.json()

        # Check that response is valid data with posts
        try:
            data_raw = pd.DataFrame(response["response"]["items"])
        except KeyError:
            error_info = response["error"]
            print(f"{error_info['error_code']=}")
            print(f"{error_info["error_msg"]=}")
            raise AssertionError()

        # Unpack dicts in columns
        for column in ["likes", "comments", "reposts", "views"]:
            new_column = column + "_count"
            data_raw[new_column] = data_raw[column].apply(lambda x: x["count"])

        # Convert unix-date to datetime
        data_raw["date"] = pd.to_datetime(data_raw["date"], unit="s")

        # Set datatype to columns with text
        data_raw[["text", "post_type"]] = data_raw[["text", "post_type"]].astype(
            "string"
        )

        # List of useful columns to truncate dataframe
        columns = [
            "id",
            "date",
            "text",
            "comments_count",
            "likes_count",
            "reposts_count",
            "views_count",
            "post_type",
        ]

        return data_raw[columns]

    def parse_posts(self, conut: int = 100, offset: int = 0) -> pd.DataFrame:
        """Parsing and processing posts. \n
        Return pd.DataFrame with only essential columns: \n
        ['id', 'date', 'text', 'comments_count',
        'likes_count', 'reposts_count', 'views_count', 'post_type']

        Args:
            conut (int, optional): Number of postss to parse. Defaults to 100.
            offset (int, optional): The bias of number posts. Defaults to 0.

        Returns:
            pd.DataFrame: Processed posts from vk api
        """

        # Get response from vk api
        response = requests.get(
            url="https://api.vk.com/method/wall.get",
            params={
                "access_token": self.__TOKEN_USER,
                "owner_id": self.__OWNER_ID,
                "v": self.__VERSION,
                "offset": offset,
                "count": conut,
                "filter": "owner",
            },
        )

        # Get processed data
        data = self._response_process(response)

        return data
