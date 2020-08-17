#!/usr/bin/python

from CloudFlareDYNDNS import CloudFlareDYNDNS


def main():
    updater = CloudFlareDYNDNS()

    # This blocks
    updater.enter_update_loop()


if __name__ == "__main__":
    main()
