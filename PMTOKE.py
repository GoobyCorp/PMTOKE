#!/usr/bin/env python3

__author__ = "GoobyCorp"
__description__ = "A script to modify PMTOK saves"

from zlib import crc32
from struct import pack
from os.path import isfile
from json import loads, dumps
from argparse import ArgumentParser

def read_file(filename: str, *, json: bool = False, text: bool = False) -> (str, bytes, bytearray, list, dict):
	with open(filename, "r" if any([json, text]) else "rb") as f:
		data = f.read()
		if json:
			data = loads(data)
	return data

def write_file(filename: str, data: (str, bytes, bytearray, list, dict)) -> None:
	if type(data) in [list, dict]:
		data = dumps(data, indent=2)

	if type(data) == str:
		with open(filename, "w", newline="\n") as f:
			f.write(data)
	else:
		with open(filename, "wb") as f:
			f.write(data)

def main() -> None:
	# create the argument parser
	parser = ArgumentParser(description=__description__)
	parser.add_argument("input", type=str, help="The file to read from")
	parser.add_argument("-o", "--ofile", type=str, help="The file to output to")
	parser.add_argument("-d", "--disable-checks", action="store_true", help="Disable initial checksum check")

	# create modification argument group
	mod_parser = parser.add_argument_group("modifications")
	mod_parser.add_argument("--coins", type=int, help="The number of coins you want")
	mod_parser.add_argument("--hp", type=int, help="The max HP you want")
	mod_parser.add_argument("--confetti", type=int, help="The max confetti you want")
	mod_parser.add_argument("--repair", action="store_true", help="Repair all damaged items")

	# parse the arguments
	args = parser.parse_args()

	assert isfile(args.input), "The specified input file doesn't exist"

	# read the save, check the original checksum, and parse the JSON
	udata = read_file(args.input, text=True)
	cksm = int.from_bytes(bytes.fromhex(udata[-8:]), "big")  # CRC32 checksum
	udata = udata[:-8]
	assert args.disable_checks or cksm == crc32(udata.encode("UTF8")), "Invalid CRC32!"
	jdata = loads(udata)

	# handle modification arguments
	if args.coins:
		jdata["Header"]["Coin"] = args.coins
		jdata["Pouch"]["coin"]  = args.coins

	if args.hp:
		jdata["Header"]["HP"] = args.hp
		jdata["Header"]["MaxHP"] = args.hp
		jdata["Pouch"]["hp"] = args.hp
		jdata["Pouch"]["hp_max"] = args.hp

	if args.confetti:
		jdata["Pouch"]["confetti_paper"] = args.confetti
		jdata["Pouch"]["confetti_paper_max"] = args.confetti

	if args.repair:
		for x in jdata["Pouch"]["equipment"]["bag"]:
			inv_item = jdata["Pouch"]["equipment"]["bag"][x]
			if "type" in inv_item and "usedEndurance" in inv_item and "usedBreakRate" in inv_item:
				if inv_item["type"] > -1 and inv_item["usedEndurance"] > 0 or inv_item["usedBreakRate"] > 0:
					jdata["Pouch"]["equipment"]["bag"][x]["usedEndurance"] = 0
					jdata["Pouch"]["equipment"]["bag"][x]["usedBreakRate"] = 0

	# prepare, checksum, and write modified data
	mdata = dumps(jdata, indent=2, separators=(",", " : "))
	mdata += pack(">I", crc32(mdata.encode("UTF8"))).hex()
	mdata = mdata.replace("\r\n", "\n")  # fix newlines
	write_file("modded.bin" if args.ofile is None else args.ofile, mdata)

if __name__ == "__main__":
	main()