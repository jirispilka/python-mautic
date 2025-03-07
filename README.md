# Mautic Python

Python wrapper for Mautic API based on [requests-oauthlib](https://github.com/requests/requests-oauthlib)
Forked from: https://github.com/sharon-asana/python-mautic

## Installation

Clone repo from GitHub:

```bash
$ git clone https://github.com/divio/python-mautic.git
```

Then install it by running:

```bash
$ python setup.py install
```

## Quickstart

Put your Mautic API credentials in `apitester/oauth2_app.py`.
Run Flask app to get OAuth2 token:

```bash
$ python apitester/oauth2_app.py
```

This way you'll have `creds.json` in a temporary directory. Now you can start using Mautic API:

```python
from python_mautic import MauticOauth2Client, Contacts
from python_mautic.utils import read_token_tempfile
token = read_token_tempfile()
mautic = MauticOauth2Client(base_url='<base URL>', client_id='<Mautic Public Key>', token=token)
contacts = Contacts(client=mautic)
print(contacts.get_list())
```

## Filter (where)

The API allows filtering with a kind of a query builder when using PHP.
The implementation is very simple using Python.

Add a dictionary with 3 attributes for each filter:
1. column
2. expr
3. val

```python
where = {
       'where[0][col]': '<field_name>',
       'where[0][expr]': '<expression>',
       'where[0][val]': '<value>'
   }
contacts = Contacts(client=mautic)
contacts_list = contacts.get_list(minimal=True, limit=step,where=where)
```

The list of possible expressions is in the API docs: [List Contacts](https://developer.mautic.org/#list-contacts), [Doctrine Query Builder](https://www.doctrine-project.org/projects/doctrine-orm/en/2.7/reference/query-builder.html#the-expr-class)
