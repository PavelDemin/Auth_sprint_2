import pprint

from ua_parser import user_agent_parser

pp = pprint.PrettyPrinter(indent=4)

def get_device_from_useragent(useragent):
    parsed_string = user_agent_parser.Parse(useragent)
    return str(parsed_string['device'])
