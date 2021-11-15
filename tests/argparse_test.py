import argparse

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('n',
                    help='Number peepeepoopoo',
                    type=int)


args = parser.parse_args()
print(args)
print(args.num)

