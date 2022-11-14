import argparse

import sectorgenerator
import validation
import tkhex
import globalstuff

parser = argparse.ArgumentParser(
    description="Generates a sector of space for use in Traveller")
parser.add_argument(
    "-x",
    dest='survival',
    default=0,
    type=int,
    help="alien survival percent (default=10)")
parser.add_argument(
    "-t",
    dest='techlevel',
    default=15,
    type=int,
    help="maximum tech level (default=15)")
parser.add_argument(
    "-v",
    dest='validation',
    default=True,
    action='store_true',
    help="run validations")

args = parser.parse_args()
globalstuff.maxTechLevel = args.techlevel
globalstuff.alienSurvivalPercent = args.survival

sectorgenerator.sectorgen()

if args.validation:
    validation.validation(args.techlevel)
    
#tkhex.SystemDisplay()
