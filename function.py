#!/usr/bin/env python3

from datetime import datetime, timedelta
import requests
from twilio.rest import Client
from dateutil.parser import parse


def get_country_cases(country, start_date, end_date):
    resp = requests.get(f"https://api.covid19api.com/country/{country}/status/confirmed",
                        params={"from": start_date,
                                "to": end_date})
    return resp.json()


def send_whatsapp_message(msg):
    account_sid = '<insert>'
    auth_token = '<insert>'
    Client(account_sid, auth_token).messages.create(
        from_='whatsapp:<insert>',
        to='whatsapp:<insert>',
        body=msg
    )


def main():
    country = "US"
    today = datetime.now().date()
    week_ago = today - timedelta(days=7)
    print("Getting COVID data")
    cases = get_country_cases(country, week_ago, today)
    latest_day = cases[-1]
    earliest_day = cases[0]
    percentage_increase = (latest_day['Cases'] - earliest_day['Cases']) / (earliest_day['Cases'] / 100)
    msg = f"There were {latest_day['Cases']} confirmed COVID cases in {country} " \
          f"on {parse(latest_day['Date']).date()}\n"
    if percentage_increase > 0:
        msg += f"This is {round(abs(percentage_increase), 4)}% increase over the last week. " \
               f"Travel is not recommended."
    else:
        msg += f"This is {round(abs(percentage_increase), 4)}% decrease over the last week. " \
               f"Travel may be OK."
    print("Sending Whatsapp message")
    send_whatsapp_message(msg)
    print("Job finished successfully")