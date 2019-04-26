#!/usr/bin/env python3

# RITSEC Demos Week 13
# Medium 3

import csv, sys, requests

def get_ip_country(ip):
    """
    Get a country from an IP address.
    :param ip: an IP address
    :return: a country string
    """
    api_key = "194ebecf7ed60089c87d452064649063f04c95cd17b151f38e423225"
    response = requests.get("https://api.ipdata.co/" + ip + "?api-key=" + api_key).json()
    country = dict(response).get("country_name")
    return country

def count_logins(log):
    """
    Count the number of login attempts per IP address.
    :param log: the syslog text
    :return: dictionaries of ip addresses, usernames, and login counts
    """
    ip_dict = {}
    success_dict = {}
    for line in log:

        # error login count
        if "error: maximum authentication attempts exceeded for" in line:
            values = line.strip().split()
            # find the word directly preceding
            identifier1 = values.index("from")
            identifier2 = values.index("for")
            # increment it to get the IP address value
            ip = values[identifier1 + 1]
            username = values[identifier2 + 1]
            if ip in ip_dict.keys():
                # increment the number of attempts for this address
                ip_dict[ip + "--" + username] += 1
            else:
                # create a new entry for the address
                ip_dict[ip + "--" + username] = 1

        # successful login count
        if "session opened for" in line:
            values = line.strip().split()
            # find the word directly preceding
            identifier3 = values.index("user")
            username = values[identifier3 + 1]

            if username in success_dict.keys():
                # increment the number of attempts for this address
                success_dict[username] += 1
            else:
                # create a new entry for the address
                success_dict[username] = 1

    # return the dictionary of addresses and login attempt counts
    return ip_dict, success_dict

def dict_to_csv(filename, dict):
    """
    Create a CSV file from a dictionary.
    :param dict: a dictionary of IPs and login attempt counts
    :return: None
    """
    with open(filename, 'w+', newline='') as graph_file:
        filewriter = csv.writer(graph_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['Count', 'IP', 'Username', 'Location'])

        # sort the dictionary by values
        output = sorted(dict, key=dict.get, reverse=True)

        # get the information per row and write the output
        for key in output:
            key_split = key.split("--")
            ip = key_split[0]
            username = key_split[1]
            count = dict[key]
            country = get_ip_country(ip)
            filewriter.writerow([count, ip, username, country])

    # close the csv file
    graph_file.close()

# main program
if __name__ == "__main__":
    # open the file and read in the data
    syslog_file = open("auth.log", "r")
    syslog_data = syslog_file.read().split("\n")
    csv_path = "logins.csv"

    # get the dictionaries
    ip_dict, success_dict = count_logins(syslog_data)

    # write the failed login attempts (count, IP, username, location) to a file
    dict_to_csv(csv_path, ip_dict)
    print("See", csv_path, "for failed login attempts (count, IP, username, location).")

    # get the total number of successful logins
    total = 0
    for value in success_dict.values():
        total += value

    # get the most commonly used login name and it's total
    output = sorted(success_dict, key=success_dict.get, reverse=True)
    username = output[0]
    username_total = success_dict.get(username)

    # print the number of successful login attempts and the most common login name
    print("Number of successful logins:", total)
    print("Most commonly used login name:", username, "(" + str(username_total) + ")")

    # close the file
    syslog_file.close()