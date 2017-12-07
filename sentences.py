#!/usr/bin/env python3
"""
sentences.py

Reads an input stream and breaks it up into sentences. Uses a fixed list of
non-breaking period patterns. Warns about short sentences on stderr. Outputs
each sentence on its own line.
"""

import re
import sys

# TODO: Use these?
NBP = [
  "a.m.",
  "p.m.",
  "A.M.",
  "P.M.",
  "Mr.",
  "Mrs.",
  "Ms.",
  "B.Sc.",
  "B.A.",
  "Ph.D.",
  "U.S.A.",
]

BUFFER_SIZE = 2048

def break_buffer(buf, br=r'\.', minlength=5, warnlength=9):
  """
  Breaks a buffer into a leftover fragment, a list of sentence strings, and a
  list of warning strings.
  """
  i = 0
  r = re.compile(br)
  sentences = []
  warnings = []
  leftovers = ''
  pre_s = ''
  while i < len(buf):
    m = r.search(buf, i)
    if m: # a match
      s = pre_s + buf[i:m.end() + 1]
      if len(s) <= minlength:
        pre_s = s
        continue
      elif len(s) <= warnlength:
        warnings.append("W: '{}'".format(s))

      pre_s = ''
      sentences.append(s)
      i = m.end() + 1
    else: # no match
      leftovers = buf[i:]
      i = len(buf)

  return leftovers, sentences, warnings

def sentences(stream, br=r'\.', minlength=5, warnlength=9):
  """
  Breaks up the given stream into sentences, using a fixed list of non-breaking
  period patterns and warning about short sentences, or automatically joining
  extremely-short sentences (use minlength and warnlength to control this
  behavior; set warnlength to zero or below minlength to disable warnings).
  Note that the br argument specifies what is considered a sentence break, and
  may be given as a regular expression. Sentences are yielded one-by-one, with
  carriage returns removed and newlines replaced with spaces.
  """
  leftovers = ''
  while True:
    nxt = stream.read(BUFFER_SIZE)
    buf = leftovers + nxt
    if len(nxt) < BUFFER_SIZE: # at end of file; handle leftovers differently
      leftovers, sentences, warnings = break_buffer(
        buf,
        br,
        minlength,
        warnlength
      )

      if warnlength:
        for w in warnings:
          print(w, file=sys.stderr)

      if leftovers.strip():
        sentences.append(leftovers.strip())
        if len(leftovers) < warnlength and warnlength >= minlength:
          print("W: '{}'".format(leftovers), file=sys.stderr)

      break

    else: # not at end of file
      leftovers, sentences, warnings = break_buffer(
        buf,
        br,
        minlength,
        warnlength
      )
      if warnlength:
        for w in warnings:
          print(w, file=sys.stderr)

    for s in sentences:
      yield s.replace('\n', ' ').replace('\r', '').strip()

if __name__ == "__main__":
  for s in sentences(sys.stdin):
    print(s)
