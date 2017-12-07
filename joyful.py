#!/usr/bin/env python3
"""
joyful.py

Streaming skip-gram analysis of words.

---

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import re
import sys
import math
import collections

SKIP_SIZE = 4

def find_associations(stream, max_skip=None):
  """
  Finds associations between words in the given input stream, processing one
  line at a time. Words on separate lines are considered unrelated. Words that
  are no more than max_skip distance apart are marked as associated; set
  max_skip to None or 0 to associate every word-pair on each line. The return
  value is a two-level dictionary that maps from words to associated-words to
  association-counts. Each association is entered twice (once under each word
  in it) so that lookups can be done from either end.
  """
  assoc = collections.defaultdict(lambda: collections.defaultdict(lambda: 0))
  counts = collections.defaultdict(lambda: 0)
  for line in stream:
    words = re.split(r"\s+", line.strip())
    for i in range(len(words) - 1):

      if max_skip:
        window = words[i:i+max_skip]
      else:
        window = words[i:]

      current = window[0]

      counts[current] += 1

      for w in window[1:]:
        assoc[current][w] += 1
        assoc[w][current] += 1

  return assoc

def report_associations(assoc, word):
  """
  Reports the associations of a given word in a n associations structure.
  Returns a string.
  """
  result = ""
  others = assoc[word]
  total = sum(others[k] for k in others)
  pct = [ (others[k]/total, k) for k in others ]
  for p, k in sorted(pct, key=lambda e: (1-e[0], e[1])):
    result += "{:10.3g}% : {}\n".format(p*100, k)

  return result

def entropy(assoc, word):
  """
  Returns the entropy of the given word in the given association. This is a
  general measure of how much information the presence of that word gives you
  about the presence of other words, with lower entropy indicating a
  more-informative word.
  """
  h = 0
  others = assoc[word]
  total = sum(others[k] for k in others)
  pct = [ (others[k]/total, k) for k in others ]
  for k in others:
    p = others[k]/total
    h += p * math.log(p)

  return -h

if __name__ == "__main__":
  mode = "associations"
  while '-e' in sys.argv:
    mode = "entropy"
    sys.argv.remove('-e')
  assoc = find_associations(sys.stdin)
  if mode == "entropy":
    elist = sorted([(entropy(assoc, w), w) for w in assoc])
    for e, w in elist:
      print("{:.3g}: {}".format(e, w))
  else: # default: associations
    for k in sorted(list(assoc.keys())):
      print(k + ":")
      print(report_associations(assoc, k))
