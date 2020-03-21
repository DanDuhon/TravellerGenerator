import argparse

import sectorgenerator
import validation

parser = argparse.ArgumentParser(description="Generates a sector of space for use in Gurp's Travellers")
parser.add_argument("-s", default=50, dest='size', type=int, help="initial sector size")
parser.add_argument("-c", default=50, dest='cluster', type=int, help="open cluster percent")
parser.add_argument("-x", default=10, dest='survival', type=int, help="alien survival percent")
parser.add_argument("-t", default=15, dest='techlevel', type=int, help="maximum tech level")
parser.add_argument("-v", default=False, dest='validation', action='store_true', help="run validations")

args = parser.parse_args()

sectorgenerator.sectorgen(args.size, args.cluster, args.survival, args.techlevel)

if args.validation:
    validation.validation(args.techlevel)
