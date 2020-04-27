import os
import json
from datetime import datetime


HOME = os.getenv("HOME")
RAW_DATA = HOME + "/Development/speedtest/raw/speeds.json"


def read_raw_speeds():
    with open(RAW_DATA) as f:
        lines = f.read().splitlines()

    measurements = {}
    key = None
    for i, l in enumerate(lines):
        if i % 4 == 0:
            # It's a date
            key = l
        if i % 4 == 1:
            # It's an entry
            d = json.loads(l)
            download = float("%.5g" % (d["download"] / 10 ** 6))
            upload = float("%.5g" % (d["upload"] / 10 ** 6))
            measurements[key] = (download, upload)

    return measurements


def find_mean_speed(measurements):
    downloads, uploads = zip(*measurements.values())

    mean_download = sum(downloads) / len(downloads)
    mean_upload = sum(uploads) / len(uploads)

    mean_speeds = [
        "Download average speed is: {}Mbit/s".format(mean_download),
        "Upload average speed is: {}Mbit/s".format(mean_upload),
    ]

    return mean_speeds


def find_all_breaches(measurements):
    breaches = []
    for date, (download, upload) in measurements.items():
        if download < 50 and upload < 7:
            breaches.append(
                "{}: Breach with download at {}Mbit/s and upload at {}Mbit/s".format(
                    date, download, upload
                )
            )
        elif download < 50:
            breaches.append(
                "{}: Breach with download at {}Mbit/s".format(date, download)
            )
        elif upload < 7:
            breaches.append("{}: Breach with upload at {}Mbit/s".format(date, upload))

    return breaches


def write_history(mean_speeds, all_breaches):
    history_file = HOME + "/Development/speedtest/history/" + str(datetime.now())

    with open(history_file, "w") as outfile:
        for ms in mean_speeds:
            outfile.write(ms + "\n")

        outfile.write("\n")

        for ab in all_breaches:
            outfile.write(ab + "\n")


def main():
    measurements = read_raw_speeds()

    mean_speeds = find_mean_speed(measurements)
    all_breaches = find_all_breaches(measurements)

    write_history(mean_speeds, all_breaches)


if __name__ == "__main__":
    main()
