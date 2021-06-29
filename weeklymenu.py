#!/usr/bin/env python3
from icalevents.icalevents import events
from datetime import datetime, timedelta
url = open('calendar.url', 'r').readline().strip()

def fixup(s):
  parts = s.split(', ')
#  if len(parts) == 1:
#   return s
  ret = []
  part = []
  for p in parts:
    if p.split()[0].lower() in ('defrost', 'marinate', 'order', 'buy', 'pick', 'pickup'):
      if part:
        ret.append(' '.join(part) + '<br />')
      part = []
      # I solemnly swear I will not put a comma in an instruction item
      ret.append('<span class="special">' + p + '</span>')
    else:
      part.append(p)
  if part:
    ret.append(', '.join(part))
  return '\n'.join(ret)


# Figure out tomorrow
tomorrow = (datetime.now() + timedelta(1)).replace(hour=0,minute=0,second=0,microsecond=0)
finish = tomorrow + timedelta(10)

outfile = open('menu.html', 'w', encoding='utf-16')
outfile.write('''
<html>
<head>
<style>
html, body {font-family: Arial, sans-serif}
.day {font-weight: bold; text-align: left; font-size: 120%; padding-top: 1.5em; padding-bottom: 0.5em;}
.daypart {width: 1px; vertical-align: top;}
.special {font-weight: bold; 
          box-shadow: 1px 1px 2px 1px; 
          border-radius: 30px; 
          background-color: rgba(17, 199, 255, 0.28); 
          padding: 1px 5px 1px 5px;
          display: inline-block; 
          margin-left: -5px;
          margin-top: 3px;
          margin-bottom: 3px}
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
