# fapdoc

fapdoc is an export/import tool for pwndoc, it allow exporting pwndoc's findings to different formats such as csv.

## Setup

install requirements:

```
$ cd fapdoc
$ pip3 install -r requirements.txt
```

Setup your config:

```
$ cp config.example.ini config.ini
```

## Examples

Get available pwndoc's audits:

```
$ ./fapdoc.py -l
```

Get available findings per audit:

```
$ ./fapdoc.py -a [audit_id]
```

Get a finding:

```
$ ./fapdoc.py -a [audit_id] -f [finding_id]
```

Send a finding to jira as new issue:

```
$ ./fapdoc.py -a [audit_id] -f [finding_id] -e jira
``` 

Export an audit to csv:

```
$ ./fapdoc.py -a [audit_id] -e csv
```

## Donations

Donations are welcome via [PayPal](https://www.paypal.com/donate/?hosted_button_id=B2Q8F4Q95QX74), thank you.
