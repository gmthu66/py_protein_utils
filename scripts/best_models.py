#!/usr/bin/env python2.5

from optparse import OptionParser
from rosettautil.rosetta import rosettaScore

usage = "%prog [options] --term=scoreterm silent files"
parser=OptionParser(usage)
parser.add_option("--term",dest="term",help="score term to use")
(options,args) = parser.parse_args()

scores = rosettaScore.SilentScoreTable()

for silent_file in args:
    scores.add_file(silent_file)

score_gen = scores.score_generator(options.term)
best_models = {} # key is a structure ID, value is a pair in form (tag,score)
for tag,score in score_gen:
    split_tag = tag.split("_")
    model_id = "_".join(split_tag[0:len(split_tag)-1])
    try:
        (current_best_tag,current_best_score) = best_models[model_id]
    except KeyError:
        best_models[model_id] = (tag,score)
        continue
    if score < current_best_score:
        best_models[model_id] = (tag,score)
print "tag",options.term
for tag in best_models:
    print best_models[tag][0],best_models[tag][1]