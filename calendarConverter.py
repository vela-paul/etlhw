# Re-define the ICS file path since previous context was lost
ics_file_path = "calendar.ics"

# Read and parse ICS file
with open(ics_file_path, "r", encoding="utf-8") as file:
    lines = file.readlines()

# Initialize variables for parsing
events = []
event = {}
inside_event = False

for line in lines:
    line = line.strip()
    if line == "BEGIN:VEVENT":
        inside_event = True
        event = {}
    elif line == "END:VEVENT":
        inside_event = False
        events.append(event)
    elif inside_event:
       

        if line.startswith("DTSTART:"):
            dtstart_value = line.split(";", 1)[1].split(":")[1].strip()  # Get the value after 'DTSTART:'
            event["DTSTART"] = dtstart_value
            continue

        if ":" in line:
            if(line.find(":mailto:") != -1):
                mailto_index = line.find(":mailto:")
                email_part = line[mailto_index + 8:]
              
                name = email_part.split("@")[0]  # Extract name before '@'
                prenume = name.split(".")[0]  # Assuming name is in format 'first.last'
                nume = name.split(".")[1] 
                event["FirstName"] = prenume
                event["LastName"] = nume
               
            key, value = line.split(":", 1)
            key = key.split(";")[0]  # Remove parameters
            if key in event:
                if isinstance(event[key], list):
                    event[key].append(value)
                else:
                    event[key] = [event[key], value]
            else:
                event[key] = value

# Create DataFrame and show
import pandas as pd
from datetime import datetime

def parse_ics_datetime(dt_string):
    """Parse ICS datetime format like 20250602T110000 to readable format"""
    if not dt_string:
        return ""
    try:
        
        
        dt_obj = datetime.strptime(dt_string, "%Y%m%dT%H%M%S")
        # Return in readable format
        return dt_obj.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return dt_string  # Return original if parsing fails

# Convert event dicts into structured rows
structured_events = []
for ev in events:
    structured_events.append({
        "FirstName": ev.get("FirstName", ""),
        "LastName": ev.get("LastName", ""),
        "Summary": ev.get("SUMMARY", ""),
        "Description": ev.get("DESCRIPTION", ""),
        "Start": ev.get("DTSTART", ""),
        "End": parse_ics_datetime(ev.get("DTEND", "")),
     
    })

structured_events.sort(key=lambda x: x.get("LastName", ""))

# Save to CSV
csv_path = "calendar.csv"
df_events = pd.DataFrame(structured_events)
df_events.to_csv(csv_path, index=False)

#to do fix datetime format