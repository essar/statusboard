from argparse import ArgumentParser


class BoardConfig:
    def __init__(self):
        # Set up defaults
        self.http_host = "127.0.0.1"
        self.http_port = 5000
        self.test_mode = False


def __load_args(namespace):

    cmdargs = vars(namespace)
    if 'host' in cmdargs:
        config.http_host = cmdargs['host']
    if 'port' in cmdargs:
        config.http_host = int(cmdargs['port'])
    if 'test' in cmdargs:
        config.test_mode = cmdargs['test']


config = BoardConfig()


# Handle command line arguments
argparser = ArgumentParser()
argparser.add_argument('--test', action='store_const', const=True, default=False, help='Run in testing mode')
argparser.add_argument('--host', nargs='?', default=config.http_host, help='API HTTP host')
argparser.add_argument('--port', nargs='?', default=config.http_port, type=int, help='API HTTP port')
__load_args(argparser.parse_args())
