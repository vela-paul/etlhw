import pandas as pd
from datetime import datetime, timedelta
import re
import csv
from io import StringIO


class MeetingIngestor:
    def __init__(self, file_paths):
        # accept single path or list of paths
        if isinstance(file_paths, str):
            file_paths = [file_paths]
        self.file_paths = file_paths
        # tables to hold results
        self.meetings_df = pd.DataFrame()
        self.participants_df = pd.DataFrame()
        self.interventions_df = pd.DataFrame()

    def parse_duration(self, s):
        if not s: return 0
        hours = minutes = seconds = 0
        match = re.search(r'(\d+)h', s)
        if match: hours = int(match.group(1))
        match = re.search(r'(\d+)m', s)
        if match: minutes = int(match.group(1))
        match = re.search(r'(\d+)s', s)
        if match: seconds = int(match.group(1))
        return int(timedelta(hours=hours, minutes=minutes, seconds=seconds).total_seconds())

    def parse_date(self, s):
        try:
            return datetime.strptime(s.strip(), "%m/%d/%y, %I:%M:%S %p")
        except ValueError as e:
            print(f"Failed to parse '{s}': {e}")
        return None
    

    def ingest(self):
        meeting_records = []
        participant_records = []
        interventions = []

        for index, fp in enumerate(self.file_paths):
            with open(fp, 'r', encoding='utf-8') as f:
                # strip empty lines
                lines = [l.rstrip('\n') for l in f if l.strip()]
            # parse summary section
            summary = {}
            for line in lines:
                key_val = line.split(',', 1)
                key = key_val[0].strip()
                val = key_val[1].strip().strip('"') if len(key_val) > 1 else ''
                val = val.strip(',.')
                if key == 'Meeting title':
                    summary['meeting_title'] = val
                elif key == 'Attended participants':
                    summary['total_attendees'] = int(val)
                elif key == 'Start time':
                    summary['start_time'] = val
                elif key == 'End time':
                    summary['end_time'] = val
                elif key == 'Meeting duration':
                    summary['duration'] = val
                elif key == 'Average attendance time':
                    summary['avg_attendance'] = val
                # stop at participants header
                if key.startswith('2. Participants'):
                    break
                if key.startswith('3. In-Meeting Activities'):
                    break
            summary['meeting_id'] = index + 1  # unique ID for each meeting
            meeting_records.append(summary)
            # parse participants table
            idx = next(i for i, l in enumerate(lines) if l.startswith('2. Participants'))
            header = [h.strip() for h in lines[idx + 1].split(',')]
       
            # stop participants at activities section
            act_idx = next((i for i, l in enumerate(lines) if l.startswith('3. In-Meeting Activities')), len(lines))
            for row in lines[idx + 2:act_idx-1]:
                reader = csv.reader(StringIO(row))
                columns = next(reader)
                record = dict(zip(header, columns))
             
                record["First Join"]=self.parse_date(record["First Join"])
                record["Last Leave"]=self.parse_date(record["Last Leave"])
                record["In-Meeting Duration"] = self.parse_duration( record["In-Meeting Duration"])
                record["meeting_id"]=index+1
                participant_records.append(record)
                

        
        self.meetings_df = pd.DataFrame(meeting_records)
        self.participants_df = pd.DataFrame(participant_records)
        self.interventions_df = pd.DataFrame(interventions)
        return self.meetings_df, self.participants_df, self.interventions_df
    

# Example usage:
ingestor = MeetingIngestor(("raw_data/Dava (2).csv", "raw_data/Dava (1).csv", "raw_data/Dava.csv"))
meetings_df, participants_df, interventions_df = ingestor.ingest()

print(participants_df)


meetings_df.to_csv("transformed_data/meetings.csv", index=False)
participants_df.to_csv("transformed_data/participants.csv", index=False)


