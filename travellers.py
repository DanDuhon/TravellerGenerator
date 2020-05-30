import argparse

import sectorgenerator
import validation
import tkhex

parser = argparse.ArgumentParser(
    description="Generates a sector of space for use in Traveller")
parser.add_argument("-s", dest='size', default=10, type=int,
                    help="initial sector size (default=50)")
parser.add_argument(
    "-x",
    dest='survival',
    default=10,
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
    default=True,
    action='store_true',
    help="run validations")

args = parser.parse_args()

sectorgenerator.sectorgen(
    args.size,
    args.survival,
    args.techlevel)

if args.validation:
    validation.validation(args.techlevel)

tkhex.SystemDisplay()
