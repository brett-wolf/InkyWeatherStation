import datetime
from datetime import timedelta
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from ConfigHandler import ConfigHandler

config = ConfigHandler()

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


class Values(object):
    pass


class calendardata:
    def __init__(self, summary, date, time):
        self.summary = summary
        self.date = date
        self.time = time


class GoogleCalendarData(object):

    def __init__(self):
        self.eventlist = None

    def _parse_data(self, eventlist):
        val = Values()
        val.events = []

        for event in eventlist:
            if "date" in event["start"]:
                date = event["start"].get("date")
            else:
                date = "0/0/0"
            if "datetime" in event["start"]:
                time = event["start"].get("datetime")
            else:
                time = "00:00"

            # TODO add a new line at the end of 20 characters or something, so it spills onto a new line
            val.events.append(calendardata(event["summary"], date, time))

            #  val.events.append(calendardata())
            #  val.events["date"].append(event["start"].get("date"))
            # if 'datetime' in event["start"]:
            #  val.events["time"].append(event["start"].get("datetime"))

            # val.events.append(calendardata())
            # val.events["summary"].append(event["summary"])

            # print(event['dateTime'])
            # val.events["summary"].append(event["summary"])
            # val.events["date"].append(event["start"].get("dateTime", event["start"].get("date"))
            # val.events["time"].append(event["start"].get("dateTime", event["start"].get("date"))

            # start = event["start"].get("dateTime", event["start"].get("date"))
            # val.events.append(start + " : " + event["summary"])

        # print(val.events)
        return val

    def GetCalendarData(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("/home/evolmonster/InkyWeatherStation/config/token.json"):
            print("using existing token")
            creds = Credentials.from_authorized_user_file(
                "/home/evolmonster/InkyWeatherStation/config/token.json", SCOPES
            )
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print("Refreshing creds")
                creds.refresh(Request())
            else:
                print("Getting new creds")
                flow = InstalledAppFlow.from_client_secrets_file(
                    "/home/evolmonster/InkyWeatherStation/config/googlesecretdesktop.json",
                    SCOPES,
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(
                "/home/evolmonster/InkyWeatherStation/config/token.json", "w"
            ) as token:
                token.write(creds.to_json())

        try:
            service = build("calendar", "v3", credentials=creds, cache_discovery=False)

            # Call the Calendar API
            now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
            week = datetime.datetime.utcnow() + timedelta(days=7)

            events_result = (
                service.events()
                .list(
                    calendarId="primary",
                    timeMin=now,
                    timeMax=week.isoformat() + "Z",
                    maxResults=10,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            events = events_result.get("items", [])

            if not events:
                print("No upcoming events found.")
                return

            self.eventlist = self._parse_data(events)

            # Prints the start and name of the next 10 events
            # for event in events:
            #  start = event["start"].get("dateTime", event["start"].get("date"))
            #  print(start, event["summary"])

        except HttpError as error:
            print(f"An error occurred: {error}")
