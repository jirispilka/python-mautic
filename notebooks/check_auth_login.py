from mautic import Contacts, MauticOauth2Client
from mautic.config import Config
from mautic.utils import read_token_tempfile

token = read_token_tempfile()
mautic = MauticOauth2Client(
    base_url=Config.BASE_URL.__str__(), client_id=Config.CLIENT_ID.get_secret_value(), token=token
)
contacts = Contacts(client=mautic)

print(contacts.get_list())
