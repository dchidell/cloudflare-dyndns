import CloudFlare
from requests import get
import time
import os

__author__ = "David Chidell"


class CloudFlareDYNDNS:
    def __init__(self):
        self.domains = os.environ["DOMAINS"].split(',')
        self.sleep_time = int(os.environ.get("SLEEP_TIME", "60"))

        self.cf_email = os.environ.get("CF_EMAIL")
        self.cf_global_key = os.environ.get("CF_GLOBAL_KEY")
        self.cf_token = os.environ.get("CF_TOKEN")
        self.zone = os.environ.get("ZONE_ID")
        self.proxied = os.environ.get("PROXIED", "TRUE").upper() == "TRUE"
        self.current_ip = None

        if self.cf_token is None and (self.cf_global_key is None or self.cf_email is None):
            print("Error: CF_EMAIL and CF_GLOBAL_KEY or CF_TOKEN env vars need setting!")
            exit(1)
        elif self.cf_token is not None and (self.cf_email is not None or self.cf_global_key is not None):
            print("Neither CF_EMAIL or CF_GLOBAL_KEY should be set when using CF_TOKEN (using CF_TOKEN by default)")

        if self.cf_token is None:
            self.cf = CloudFlare.CloudFlare(email=self.cf_email, token=self.cf_global_key)
        else:
            self.cf = CloudFlare.CloudFlare(token=self.cf_token)

    @staticmethod
    def get_ip():
        try:
            return get('https://api.ipify.org').text
        except Exception as e:
            return None

    def process_ip(self):
        ip = self.get_ip()
        if ip is None:
            print(f"Error fetching IP: {e}")
            return None

        if ip != self.current_ip:
            if self.current_ip is None:
                print(f"Initial run, setting domain IPs...")
            else:
                print(f"Detected IP change. Old: {self.current_ip} New: {ip} Updating domains.")
        return ip

    def enter_update_loop(self):
        print(f'Entering update loop...')
        while True:
            ip = self.process_ip()
            if ip is not None and ip != self.current_ip:
                try:
                    self.update_domains(ip)
                    self.current_ip = ip
                except Exception as e:
                    print(f"Unable to update domain: {e} trying again in {self.sleep_time}s")

            time.sleep(self.sleep_time)

    def update_domains(self,ip):
        for domain in self.domains:
            post_dict = {"name": domain, "type": "A", "content": ip, "proxied": self.proxied}
            get_records = self.cf.zones.dns_records.get(self.zone, params={"name": domain})
            if len(get_records) == 0:
                self.cf.zones.dns_records.post(self.zone, data=post_dict)
                print(f"New record created: {domain}")
            else:
                for record in get_records:
                    self.cf.zones.dns_records.put(self.zone, record["id"], data=post_dict)
                    print(f"Existing record updated: {domain}")
