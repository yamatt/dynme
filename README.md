Update an IP for your DNS provider using their API. Handy for if you want to run your own Dynamic DNS system.

# License
AGPLv3

# Usage

Get your own IP:

    $ python -m dynme.myip
    123.123.123.123

## NameSilo

1. [Generate API Key](https://www.namesilo.com/account_api.php) It should look something like `f441c72e8a391e9788d3b`.
1. Find the record for the domain you want to update:

        $ python -m dynme.namesilo.listdns --key f441c72e8a391e9788d3b example.com
    
        home.example.com	A	7200	0e1169e8e8a391e949b04b3e4a73

    What is of value there is `0e1169e8e8a391e949b04b3e4a73` above the `<host>` entry for the domain you are interested in changing.
    
1. Update the record with an IP:

        $ python -m dynme.namesilo.updatedns -k f441c72e8a391e9788d3b --domain example.com --id $(python -m dynme.namesilo.listdns -k f441c72e8a391e9788d3b example.com | grep home.example.com | cut -f4) --subdomain home --ip $(python -m dynme.myexternalip)
    
### Note

Unfortunately `id` is updated every time the record is changed.

## Notes

Use `--loglevel INFO` to get more detailed logging.
