import numpy as np
import tqdm

from utils.email_sender import send_mail
from utils.secrets import (
    DICT_USERS,
    EMAIL_BASE,
)
from utils.vars import (
    DES_CONTEXT,
    FLG_TEST_MODE,
    LINK_AMAZON,
)


def create_gifts_list():
    list_users = list(DICT_USERS)
    np.random.shuffle(list_users)

    list_users_pairs = list_users + [list_users[0]]
    list_users_pairs = [(list_users_pairs[i], list_users_pairs[i+1]) for i in range(len(list_users))]
    for des_name_gift_from, des_name_gift_to in tqdm.tqdm(list_users_pairs, desc="Sending emails"):
        send_gift_mail(
            des_name_gift_from=des_name_gift_from,
            des_name_gift_to=des_name_gift_to,
        )


def send_gift_mail(
        des_name_gift_from: str,
        des_name_gift_to: str,
):
    data = {
        'des_context': DES_CONTEXT,
        'des_name_gift_from': des_name_gift_from,
        'des_name_gift_to': des_name_gift_to,
        'link_amazon': LINK_AMAZON,
    }

    list_recipients = [EMAIL_BASE] if FLG_TEST_MODE else [DICT_USERS[des_name_gift_from]]

    send_mail(
        data=data,
        list_recipients=list_recipients,
    )


if __name__ == '__main__':
    create_gifts_list()

