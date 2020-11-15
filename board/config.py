from argparse import ArgumentParser


class BoardConfig(dict):
    def __init__(self):
        super().__init__()

        # Set up defaults
        self.__setitem__('host', '127.0.0.1')
        self.__setitem__('port', 5000)
        self.__setitem__('test', False)

    @property
    def http_host(self):
        return self['host']

    @property
    def http_port(self):
        return self['port']

    @property
    def test_mode(self):
        return self['test']


def __load_args(namespace):

    cmdargs = vars(namespace)
    config.update(cmdargs)


config = BoardConfig()


# Handle command line arguments
argparser = ArgumentParser()
argparser.add_argument('--test', action='store_const', const=True, default=False, help='Run in testing mode')
argparser.add_argument('--host', nargs='?', default=None, help='API HTTP host')
argparser.add_argument('--port', nargs='?', default=None, type=int, help='API HTTP port')
__load_args(argparser.parse_args())
