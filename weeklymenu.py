#!/usr/bin/env python3
from icalevents.icalevents import events
from datetime import datetime, timedelta
url = open('calendar.url', 'r').readline().strip()

def fixup(s):
  for w in ('Defrost', 'defrost', 'Marinate', 'marinate', 'buy', 'Buy'):
    parts = s.split(f', {w} ')
    if len(parts) > 1:
      parts[1] = '<br /><span class="special">' + w[0].upper() + w[1:] + ' ' + parts[1] + '</span>'
    s = '\n'.join(parts)
  return s

# Figure out tomorrow
tomorrow = (datetime.now() + timedelta(1)).replace(hour=0,minute=0,second=0,microsecond=0)
finish = tomorrow + timedelta(10)

outfile = open('menu.html', 'w')
outfile.write('''
<html>
<head>
<style>
html, body {font-family: Arial, sans-serif}
.day {font-weight: bold; text-align: left; font-size: 120%; padding-top: 1.5em; padding-bottom: 0.5em;}
.daypart {width: 1px; vertical-align: top;}
.special {font-weight: bold; box-shadow: 1px 1px 2px 1px; border-radius: 30px; background-color: rgba(17, 199, 255, 0.28); padding: 1px 5px 1px 5px; margin-left: -5px;}
</style>
</head>
<body>
''')

es = events(url, fix_apple=True, start=tomorrow, end=finish)
es.sort()
print(len(es), ' events')
lastday = None
lastmeal = None
ttail = None
for event in es:
  ed = f'<thead><tr><th class="day" colspan="2">{event.start:%A}, {event.start:%B} {event.start.day}, {event.start.year}</th></tr></thead>\n'

  if lastday != ed:
    if ttail:
      outfile.write(ttail)
    ttail = '</tbody></table>\n'
    outfile.write('<table border="0">\n')
    outfile.write(ed)
    outfile.write('<tbody>\n')
    lastday = ed


  outfile.write(f'<tr><td class="daypart"><b>{event.description}</b>:</td>\n')
  outfile.write(f'<td>{fixup(event.summary)}</td></tr>')

  
if ttail:
  outfile.write(ttail)
outfile.write('''
</body>
</html>
''')

outfile.close()
