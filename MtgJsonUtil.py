import logging
import os

import requests

import Model


def changeDirectory() -> None:
    # change working directory to directory of file

    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)


def cacheResult(func):
    # Function Decorator for Cacheing Results

    cache = dict()

    def wrapper(*args):
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result

    return wrapper


@cacheResult
def getMtgJson() -> str:
    # Fetch JSON File from MTGJSON

    # url for MTGJSONv5 API
    url = "https://mtgjson.com/api/v5/AllPrintings.json"

    # need user agent header to avoid 403
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
    }

    logging.info("Fetching MTGJSON File from MTGJSON: " + url)

    # send request and recieve response
    response = requests.get(url, headers=headers)

    # make sure response was successful
    if response.status_code == 200:
        return response.content.decode("utf-8")
    else:
        print("Could not get MTGJSON File, STATUS CODE: " + str(response.status_code))
        raise Exception(
            "Could not get MTGJSON File, STATUS CODE: " + str(response.status_code)
        )


def downloadMtgJson() -> None:
    # Download JSON File from MTGJSON

    logging.info("Saving MTGJSON File")

    changeDirectory()

    with open("resources/AllPrintings.json", "w") as json_file:
        json_file.write(getMtgJson())


def parseMtgJson() -> Model.MtgData:
    # Parse JSON File from MTGJSON into local models

    return Model.MtgData.fromMtgJson(getMtgJson())


def saveParsedMtgJson() -> None:
    # Save parsed data as json file

    logging.info("Saving Parsed Data")

    changeDirectory()

    with open("static/cardData.json", "w") as json_file:
        json_file.write(parseMtgJson().toJson())


if __name__ == "__main__":
    saveParsedMtgJson()
