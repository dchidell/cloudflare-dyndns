# cloudflare-dyndns

## Purpose:

This docker container will update a specified domain (or list of) with the current external (public) IP of the container.


## Configuration:

### Mandatory ENV variables:

CF_GLOBAL_KEY` - CloudFlare API Key (This must be the GLOBAL key)

and 

`CF_EMAIL` - CloudFlare API Email 

Both `CF_GLOBAL_KEY` and `CF_EMAIL` are required if using the GLOBAL key. 

or

`CF_TOKEN` (recommended) - CloudFlare API Token (This must be a user token, NOT the global key)

See https://github.com/cloudflare/python-cloudflare#providing-cloudflare-username-and-api-key for detailed information on CF authentication.


`DOMAINS` - A comma seperated list of domains / subdomains to be updated. E.g. DOMAINS=sub1.domain.com,sub2.domain.com

`ZONE_ID` - The cloudflare zone your domain(s) belong to. Currently only one zone is supported


### Optional ENV vars:

`SLEEP_TIME` - Seconds between attempts to check public IP. Defaults to 60

`PROXIED` - Whether the proxied flag is set in CloudFlare or not. Set to TRUE or FALSE. Defaults to TRUE.
