# FEB 2018	chrisw
#

# imports
import logging
from optparse import OptionParser
import os
import re

import datetime

import BMEG_pb2
from google.protobuf.json_format import MessageToJson
import json

# global vars
verbose = True

# methods and functions


def getOptions():
    "parse options"
    usage_text = []
    usage_text.append("%prog [options]")

    description_text = []
    description_text.append("Convert GMT file to protobuf messages.")

    parser = OptionParser(usage="\n".join(usage_text),
                          description="\n".join(description_text))

    parser.add_option("-v", action="store_true", default=False,
                      dest="verbose", help="Switch for verbose mode.")

    parser.add_option("--gmt-file", action="store", default=None,
                      type="string", dest="gmt_file", help="[REQUIRED] gmt file name")
    parser.add_option("--metadata-file", action="store", default=None,
                      type="string", dest="metadata_file", help="[REQUIRED] metadata file name")

    (options, args) = parser.parse_args()

    return (options, args, parser)


def checkRequiredArguments(opts, parser):
    missing_options = []
    for option in parser.option_list:
        if re.match(r'^\[REQUIRED\]', option.help) and eval('opts.' + option.dest) is None:
            missing_options.extend(option._long_opts)
    if len(missing_options) > 0:
        parser.error('Missing REQUIRED parameters: ' + str(missing_options))


def getNow():
    """
    Get a datetime object for utc NOW.
    Convert to ISO 8601 format with datetime.isoformat()
    """
    now = datetime.datetime.utcnow()
    return now


def getTimeDelta(startDatetime):
    """
    get a timedelta object. Get seconds elapsed with timedelta.total_seconds().
    """
    endDatetime = datetime.datetime.utcnow()
    timedeltaObj = endDatetime - startDatetime
    return timedeltaObj


def convert_pb_to_compact_json(pb_obj):
    # MessageToJson does not have option to output compact JSON !!!
    strJson = MessageToJson(pb_obj)
    objJson = json.loads(strJson)
    strJson = json.dumps(objJson, separators=(',', ':'))
    return strJson


def gmt_to_protobuf_jsonl(gmt_file_name, attributes, output_file_name="gmt_pb.jsonl"):
    attributes["filename"] = os.path.basename(gmt_file_name)
    outfile = open(output_file_name, mode="w")
    with open(gmt_file_name, "r") as fileObj:
        for line in fileObj:
            line = line.rstrip("\r\n")
            fields = line.split("\t")
            geneset_pb = BMEG_pb2.gmt_geneset()
            geneset_pb.geneset_name = fields[0]
            geneset_pb.description = fields[1]
            geneset_pb.genes.extend(fields[2:])

            geneset_pb.filename = attributes["filename"]
            geneset_pb.sets_name = attributes["sets_name"]
            geneset_pb.source = attributes["source"]

            strJson = convert_pb_to_compact_json(geneset_pb)
            outfile.write("%s\n" % (strJson))

    fileObj.close()
    outfile.close()
    return None


def collect_attributes(metadata_file_name):
    attributes = {}
    with open(metadata_file_name, "r") as fileObj:
        for line in fileObj:
            fields = line.rstrip("\r\n").split("\t", 1)
            key = fields[0].lower()
            val = fields[1]
            if key in ["source", "sets_name"]:
                attributes[key] = val
            else:
                pass
    return attributes

#:####################################


def main():
    startTime = getNow()
    (options, args, parser) = getOptions()

    checkRequiredArguments(options, parser)

    if options.verbose:
        logLevel = logging.DEBUG
    else:
        logLevel = logging.INFO
    logFormat = "%(asctime)s %(levelname)s %(funcName)s:%(lineno)d %(message)s"
    logging.basicConfig(level=logLevel, format=logFormat)

    logging.debug('options:\t%s' % (str(options)))
    logging.debug('args:\t%s' % (str(args)))

    # convert metadata to protobuf
    attributes = collect_attributes(options.metadata_file)

    # convert gmt file to protobuf
    gmt_to_protobuf_jsonl(options.gmt_file, attributes)

    runTime = getTimeDelta(startTime).total_seconds()
    logging.info("%s ran for %s s." %
                 (os.path.basename(__file__), str(runTime)))
    logging.shutdown()
    return None


# main program section
if __name__ == "__main__":
    main()
