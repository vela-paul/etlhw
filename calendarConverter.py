import pandas as pd
from datetime import datetime, timedelta

class CalendarIngestor:
    def __init__(self, ics_file_path: str = "raw_data/calendar.ics", csv_path: str = "transformed_data/calendar.csv"):
        self.ics_file_path = ics_file_path
        self.csv_path = csv_path
        self.lines = []
        self.events = []
        self.structured_events = []
        self.df_events = None

    def parse_file(self):
        """Read ICS file and extract VEVENT blocks into self.events."""
        with open(self.ics_file_path, "r", encoding="utf-8") as file:
            self.lines = [line.strip() for line in file if line.strip()]
        inside_event = False
        event = {}
        for line in self.lines:
            if line == "BEGIN:VEVENT":
                inside_event = True
                event = {}
            elif line == "END:VEVENT":
                inside_event = False
                self.events.append(event)
            elif inside_event:
                # Date/time
                if line.startswith("DTSTART;"):
                    dtstart = line.split(";", 1)[1].split(":", 1)[1]
                    event["DTSTART"] = dtstart
                    continue
                if line.startswith("DTEND;"):
                    dtend = line.split(";", 1)[1].split(":", 1)[1]
                    event["DTEND"] = dtend
                    continue
                # Extract email and name
                if ":mailto:" in line:
                    mailto = line.split(":mailto:", 1)[1]
                    event["Email"] = mailto
                    name_part = mailto.split("@")[0]
                    first, last = name_part.split(".") if "." in name_part else (name_part, "")
                    event["FirstName"] = first
                    event["LastName"] = last
                # Generic key:value
                if ":" in line:
                    key, value = line.split(":", 1)
                    key = key.split(";", 1)[0]
                    if key in event:
                        if isinstance(event[key], list):
                            event[key].append(value)
                        else:
                            event[key] = [event[key], value]
                    else:
                        event[key] = value

    @staticmethod
    def parse_ics_datetime(dt_string: str) -> str:
        """Convert ICS datetime like 20250602T110000 to YYYY-MM-DD HH:MM:SS."""
        if not dt_string:
            return ""
        
        
        try:
            if 'T' not in dt_string and len(dt_string) == 8:
                dt_obj = datetime.strptime(dt_string, "%Y%m%d")
                # explicitly set time to 00:00:00
                return dt_obj.strftime("%Y-%m-%d 00:00:00")
           

            dt_obj = datetime.strptime(dt_string, "%Y%m%dT%H%M%S")
            dt_obj = dt_obj - timedelta(hours=3)
            return dt_obj.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            return dt_string

    def build_dataframe(self) -> pd.DataFrame:
        """Build a pandas DataFrame from parsed events."""
        for ev in self.events:
            
            record = {
                "firstName": ev.get("FirstName", ""),
                "lastName": ev.get("LastName", ""),
                "summary": ev.get("SUMMARY", ""),
                "description": ev.get("DESCRIPTION", ""),
                "start_time": self.parse_ics_datetime(ev.get("DTSTART", "")),
                "end_time": self.parse_ics_datetime(ev.get("DTEND", "")),
                "email": ev.get("FirstName", "")+'.'+ ev.get("LastName", "")+"@endava.com",
                "event_id": ev.get("EVENT-ID","")
            }
            if record.get("LastName") == "Vela":
                print(record)
            self.structured_events.append(record)
        self.structured_events.sort(key=lambda x: x.get("LastName", ""))
        self.df_events = pd.DataFrame(self.structured_events)
        return self.df_events

    def save_csv(self):
        """Save the DataFrame to CSV. Call build_dataframe() first."""
        if self.df_events is None:
            raise ValueError("No data to save. Build DataFrame first.")
        self.df_events.fillna({"Description":"Undescribed Uni-Task"},inplace=True)
       

        self.df_events['start_time'] = pd.to_datetime(self.df_events['start_time'])
        self.df_events['end_time']   = pd.to_datetime(self.df_events['end_time'])
        self.df_events.to_csv(self.csv_path, index=False)


if __name__ == "__main__":
    ingestor = CalendarIngestor()
    ingestor.parse_file()
    ingestor.build_dataframe()
    ingestor.save_csv()
