import argparse

import sectorgenerator
import validation
import tkhex
import globalvariables

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
    default=12,
    type=int,
    help="maximum tech level (default=15)")
parser.add_argument(
    "-v",
    dest='validation',
    default=False,
    action='store_true',
    help="run validations")

args = parser.parse_args()
globalvariables.maxTechLevel = args.techlevel
globalvariables.alienSurvivalPercent = args.survival

sectorgenerator.sectorgen()

if args.validation:
    validation.validation(args.techlevel)
    
tkhex.SystemDisplay()
