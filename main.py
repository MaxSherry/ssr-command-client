'''
@Author: tyrantlucifer
@E-mail: tyrantlucifer@gmail.com
@Date: 2020/12/8 下午14:20
'''

import argparse
import traceback

from funcitions.Functions import *

u = Update()
d = Display()
h = Handler()


def get_parser():
    parser = argparse.ArgumentParser(description=color.blue("The ssr command client based Python."),
                                     epilog=color.yellow('Powered by ') +
                                            color.green('tyrantlucifer') +
                                            color.yellow('. If you have any questions,you can send e-mails to ') +
                                            color.green('tyrantlucifer@gmail.com'))
    parser.add_argument("-l", "--list", action="store_true", help="show ssr list")
    parser.add_argument("-p", "--port", default=1080, metavar="local_port", type=int,
                        help="assign local proxy port,use with -s")
    parser.add_argument("-s", "--start", metavar="ssr_id", type=int, help="start ssr proxy")
    parser.add_argument("-S", "--stop", default=0, metavar="ssr_id", type=int, help="stop ssr proxy")
    parser.add_argument("-u", "--update", action="store_true", help="update ssr list")
    parser.add_argument("-v", "--version", action="store_true", help="display version")
    parser.add_argument("--upgrade", action="store_true", help="upgrade ssr command client")
    parser.add_argument("--display-json", metavar="ssr_id", type=int, help="display ssr json info")
    parser.add_argument("--test-speed", action="store_true", help="test all ssr nodes download and upload speed")
    parser.add_argument("--fast-node", action="store_true", help="find most fast by delay and start ssr proxy")
    parser.add_argument("--setting-url", metavar="ssr_subscribe_url", help="setting ssr subscribe url")
    parser.add_argument("--setting-address", metavar="ssr_local_address", help="setting ssr local address")
    parser.add_argument("--list-url", action="store_true", help="list ssr subscribe url")
    parser.add_argument("--add-url", metavar="ssr_subscribe_url", help="add ssr subscribe url")
    parser.add_argument("--remove-url", metavar="ssr_subscribe_url", help="remove ssr subscribe url")
    parser.add_argument("--list-address", action="store_true", help="list ssr local address")
    parser.add_argument("--parse-url", metavar="ssr_url", help="pares ssr url")
    parser.add_argument("--append-ssr", metavar="ssr_file_path", help="append ssr nodes from file")
    parser.add_argument("-b", action="store_true", help="append_ssr file is base64")
    parser.add_argument("--clear-ssr", metavar="ssr_id", nargs="?", const="fail",
                        help="if ssr_id is not empty, clear ssr node by ssr_id, else clear fail nodes")
    parser.add_argument("-all", action="store_true", help="clear all ssr node")
    parser.add_argument("--add-ssr", metavar="ssr_url", help="add ssr node")
    parser.add_argument("--test-again", metavar="ssr_node_id", type=int, help="test ssr node again")
    parser.add_argument("--print-qrcode", metavar="ssr_node_id", type=int, help="print ssr node qrcode")
    parser.add_argument("--setting-global-proxy", action="store_true",
                        help="setting system global proxy,only support on " + color.red('Ubuntu Desktop'))
    parser.add_argument("--setting-pac-proxy", action="store_true",
                        help="setting system pac proxy,only support on " + color.red('Ubuntu Desktop'))
    parser.add_argument("--close-system-proxy", action="store_true",
                        help="close system proxy,only support on " + color.red('Ubuntu Desktop'))
    # TODO
    # parser.add_argument("--setting-auto-start", action="store_true", help="setting ssr auto start, only support on " + color.red('Linux'))
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    if args.list:
        d.displaySSRList()
    elif args.update:
        u.updateSubscribe()
    elif args.fast_node:
        h.startFastNode()
    elif args.start is not None:
        h.start(ssr_id=args.start, port=args.port, update=u)
    elif args.stop is not None:
        h.stop(ssr_id=args.stop, port=args.port)
    elif args.version:
        d.displayVersion()
    elif args.setting_url:
        u.updateSubcribeUrl(args.setting_url)
    elif args.append_ssr:
        if not os.path.isfile(args.append_ssr):
            logger.error(f'append_ssr file {args.append_ssr} is not exists')
            return
        with open(args.append_ssr, 'r', encoding='UTF-8') as f:
            txt = f.read()
        if args.b:
            txt = ParseShadowsocksR.base64Decode(txt)
        ssr_set = set()
        for line in txt.splitlines():
            for ssr in re.findall(r'ssr://[0-9a-zA-Z=-_/+]+', line):
                ssr_set.add(ssr)
        for ssr in ssr_set:
            try:
                u.addSSRNode(ssr)
            except Exception as e:
                logger.error(f'add ssr node error {ssr}')
                logger.error(traceback.format_exc())
    elif args.clear_ssr:
        u.clearSSRNodes(args.clear_ssr, args.all)
    elif args.setting_address:
        u.updateLocalAddress(args.setting_address)
    elif args.list_url:
        d.displaySuscribeUrl()
    elif args.add_url:
        u.addSSRSubcribeUrl(args.add_url)
    elif args.remove_url:
        u.removeSSRSubcribeUrl(args.remove_url)
    elif args.list_address:
        d.displayLocalAddress()
    elif args.parse_url:
        d.parseSSRUrl(args.parse_url)
    elif args.add_ssr:
        u.addSSRNode(args.add_ssr)
    elif args.test_again:
        u.testSSRNodeConnect(ssr_id=args.test_again)
    elif args.print_qrcode:
        d.printQrCode(ssr_id=args.print_qrcode)
    elif args.setting_global_proxy:
        h.openGlobalProxy()
    elif args.setting_pac_proxy:
        h.openPacProxy()
    elif args.close_system_proxy:
        h.closeProxy()
    elif args.test_speed:
        u.testSSRSpeed()
    elif args.display_json:
        d.displaySSRJson(ssr_id=args.display_json)
    elif args.upgrade:
        d.upgrade()
    else:
        parser.print_help()


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
