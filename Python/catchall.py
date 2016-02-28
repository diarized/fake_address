#!/usr/bin/env python

import sys
import email
import smtplib
import psycopg2 as sql


def db_connect():
    pg_database = 'mail'
    pg_user = 'catchall'
    pg_pass = 'hurr444yah1p'
    connection = sql.connect(database=pg_database, user=pg_user, password=pg_pass)
    return connection


def get_fake_sender(real_sender, recipient):
    # return '4576asd@address.stonith.pl'
    connection = db_connect()
    cursor = connection.cursor()
    cursor.execute("SELECT sender, recipient FROM get_fake_sender(%s, %s) AS (sender VARCHAR(160), recipient VARCHAR(160))", (real_sender, recipient))
    fake_sender = cursor.fetchone()
    return fake_sender[0]


if __name__ == "__main__":
    msg = email.message_from_file(sys.stdin)
    recipient = msg['To']
    recipient_name, recipient_email = email.utils.parseaddr(recipient)
    sender_full = msg.get('From')
    sender_name, sender_email = email.utils.parseaddr(sender_full)
    
    with open('/tmp/aaa.txt', 'a') as fh:
        fh.write("Original sender name: {}, sender e-mail: {}, recipient e-mail: {}".format(sender_name, sender_email, recipient_email))

    fake_sender = get_fake_sender(sender_email, recipient_email)

    with open('/tmp/aaa.txt', 'a') as fh:
        fh.write("Original sender name: {}, sender e-mail: {}, fake sender: {}".format(sender_name, sender_email, fake_sender))
    
    del msg['From']
    msg['From'] = fake_sender
    server = smtplib.SMTP('localhost')
    server.sendmail(fake_sender, recipient, msg.as_string())
    server.quit()
