import os
import pickle

import pandas as pd
import pkg_resources


def _convert(data):
    df = pd.DataFrame(data, columns=["url"])
    length_of_url = []  # length of url
    number_of_letters = []  # number of alphanumeric characters
    number_of_digits = []  # number of digits
    count_of_dotcom = []  # count of '.com'
    count_of_codot = []  # count of '.co.'
    count_of_dotnet = []  # count of '.net'
    count_of_forward_slash = []  # count of '/'
    count_of_percentage = []  # count of '%'
    count_of_upper_case = []  # count of upper case characters
    count_of_lower_case = []  # count of upper case characters
    count_of_dot = []  # count of "."
    count_of_upper_case = []  # count of upper case characters
    count_of_lower_case = []  # count of lower case characters
    count_of_dot_info = []  # count of '.info'
    count_of_https = []  # count of 'https'
    count_of_www_dot = []  # count of 'www.'
    count_of_not_alphanumeric = []  # count of non-alphanumeric characters

    for item in df["url"]:
        try:
            length_of_url.append(len(item))
        except:
            length_of_url.append(0)

        try:
            number_of_letters.append(sum(c.isalpha() for c in item))
        except:
            number_of_letters.append(0)

        try:
            number_of_digits.append(sum(c.isdigit() for c in item))
        except:
            number_of_digits.append(0)

        try:
            count_of_dotcom.append(item.count(".com"))
        except:
            count_of_dotcom.append(0)

        try:
            count_of_codot.append(item.count(".co."))
        except:
            count_of_codot.append(0)

        try:
            count_of_dotnet.append(item.count(".net"))
        except:
            count_of_dotnet.append(0)

        try:
            count_of_forward_slash.append(item.count("/"))
        except:
            count_of_forward_slash.append(0)

        try:
            count_of_percentage.append(item.count("%"))
        except:
            count_of_percentage.append(0)

        try:
            count_of_dot.append(item.count("."))
        except:
            count_of_dot.append(0)

        try:
            count_of_upper_case.append(sum(c.isupper() for c in item))
        except:
            count_of_upper_case.append(0)

        try:
            count_of_lower_case.append(sum(c.islower() for c in item))
        except:
            count_of_lower_case.append(0)

        try:
            count_of_dot_info.append(item.count(".info"))
        except:
            count_of_dot_info.append(0)

        try:
            count_of_https.append(item.count("https"))
        except:
            count_of_https.append(0)

        try:
            count_of_www_dot.append(item.count("www."))
        except:
            count_of_www_dot.append(0)

        try:
            count_of_not_alphanumeric.append(sum(not c.isalnum() for c in item))
        except:
            count_of_not_alphanumeric.append(0)

    df["length_of_url"] = length_of_url
    df["number_of_letters"] = number_of_letters
    df["number_of_digits"] = number_of_digits
    df["count_of_dotcom"] = count_of_dotcom
    df["count_of_codot"] = count_of_codot
    df["count_of_dotnet"] = count_of_dotnet
    df["count_of_forward_slash"] = count_of_forward_slash
    df["count_of_upper_case"] = count_of_upper_case
    df["count_of_lower_case"] = count_of_lower_case
    df["count_of_dot"] = count_of_dot
    df["count_of_upper_case"] = count_of_upper_case
    df["count_of_lower_case"] = count_of_lower_case
    df["count_of_dot_info"] = count_of_dot_info
    df["count_of_https"] = count_of_https
    df["count_of_www_dot"] = count_of_www_dot
    df["count_of_not_alphanumeric"] = count_of_not_alphanumeric
    df["count_of_percentage"] = count_of_percentage

    ## Amount of symbols to letters ratio
    df["not_alphanumeric_to_letters_ratio"] = (
        df["count_of_not_alphanumeric"] / df["number_of_letters"]
    )

    ## Amount of '%' to length ratio
    df["percentage_to_length_ratio"] = df["count_of_percentage"] / df["length_of_url"]

    ## Amount of '%' to length ratio
    df["percentage_to_length_ratio"] = df["count_of_percentage"] / df["length_of_url"]

    ## Amount of '/' to length ratio
    df["forwards_slash_to_length_ratio"] = (
        df["count_of_forward_slash"] / df["length_of_url"]
    )

    ## Amount captialised vs. non-capitalised
    df["upper_case_to_lower_case_ratio"] = (
        df["count_of_upper_case"] / df["count_of_lower_case"]
    )
    X = df[
        [
            "length_of_url",
            "number_of_letters",
            "number_of_digits",
            "count_of_dotcom",
            "count_of_codot",
            "count_of_dotnet",
            "count_of_forward_slash",
            "count_of_upper_case",
            "count_of_lower_case",
            "count_of_dot",
            "count_of_dot_info",
            "count_of_https",
            "count_of_www_dot",
            "count_of_not_alphanumeric",
            "count_of_percentage",
            "percentage_to_length_ratio",
            "forwards_slash_to_length_ratio",
        ]
    ]

    return X


def _predict(name):
    data = [name]
    X = _convert(data)
    dir_path = os.path.dirname(__file__)
    tree = pickle.load(open(dir_path + "/tree.pkl", "rb"))
    installed_packages = pkg_resources.working_set
    installed_packages_list = sorted(
        ["%s==%s" % (i.key, i.version) for i in installed_packages]
    )
    results = {}
    results["tree"] = tree.predict(X)
    xgb_model = pickle.load(open(dir_path + "/xgb.pkl", "rb"))
    results["xgb"] = xgb_model.predict(X)
    lgb_model = pickle.load(open(dir_path + "/lgb.pkl", "rb"))
    results["lgb"] = lgb_model.predict(X)
    rfc_model = pickle.load(open(dir_path + "/rfc.pkl", "rb"))
    results["rfc"] = rfc_model.predict(X)
    return results

def _metrics():
    dir_path = os.path.dirname(__file__)
    source = pickle.load(open(dir_path + "/metrics.pkl", "rb"))
    return source