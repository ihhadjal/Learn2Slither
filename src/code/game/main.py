import argparse
from agent import Agent

parser = argparse.ArgumentParser()

parser.add_argument("-sessions", type=int, default=100)
parser.add_argument("-save", type=str, default=None)
parser.add_argument("-load", type=str, default=None)
parser.add_argument("-visual", type=str, default="on")
parser.add_argument("-dontlearn", action="store_true")

args = parser.parse_args

my_agent = Agent()

if args.load:
    my_agent.load(args.load)

if args.dontlearn:
    my_agent.learning = False

# def training():
#     for _ in range(args.session):