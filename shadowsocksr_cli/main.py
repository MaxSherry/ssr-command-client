"""
@author: tyrantlucifer
@contact: tyrantlucifer@gmail.com
@blog: https://tyrantlucifer.com
@file: main.py
@time: 2021/2/18 21:36
@desc: shadowsocksr-cli入口函数
"""

import argparse
import traceback

from shadowsocksr_cli.functions import *


def get_parser():
    parser = argparse.ArgumentParser(description=color.blue("The shadowsocksr command client based Python."),
                                     epilog=color.yellow('Powered by ') + color.green('tyrantlucifer') + color.yellow(
                                         ". If you have any questions,you can send e-mails to ") + color.green(
                                         "tyrantlucifer@gmail.com"))
    parser.add_argument("-l", "--list", action="store_true", help="show ssr list")
    parser.add_argument("-p", "--port", default=1080, metavar="local_port", type=int,
                        help="assign local proxy port,use with -s")
    parser.add_argument("-s", "--start", metavar="ssr_id", type=int, help="start ssr proxy")
    parser.add_argument("-S", "--stop", nargs='?', const=-1, metavar="ssr_id", type=int, help="stop ssr proxy")
    parser.add_argument("-u", "--update", action="store_true", help="update ssr list")
    parser.add_argument("-v", "--version", action="store_true", help="display version")
    parser.add_argument("--generate-clash", action="store_true", help="generate clash config yaml")
    parser.add_argument("--display-json", metavar="ssr_id", type=int, help="display ssr json info")
    parser.add_argument("--test-speed", type=int, metavar="ssr_id", help="test ssr nodes download and upload speed")
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
    parser.add_argument("--http", metavar="action[start stop status]", help="Manager local http server")
    parser.add_argument("--http-port", metavar="http server port", default=80, type=int,
                        help="assign local http server port")
    parser.add_argument("--setting-global-proxy", action="store_true",
                        help="setting system global proxy,only support on " + color.red('Ubuntu Desktop'))
    parser.add_argument("--setting-pac-proxy", action="store_true",
                        help="setting system pac proxy,only support on " + color.red('Ubuntu Desktop'))
    parser.add_argument("--close-system-proxy", action="store_true",
                        help="close system proxy,only support on " + color.red('Ubuntu Desktop'))
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    if args.list:
        DisplayShadowsocksr.display_shadowsocksr_list()
    elif args.update:
        UpdateConfigurations.update_subscribe()
    elif args.fast_node:
        HandleShadowsocksr.select_fast_node(args.port)
    elif args.start is not None:
        HandleShadowsocksr.start(ssr_id=args.start, local_port=args.port)
    elif args.stop is not None:
        HandleShadowsocksr.stop(ssr_id=args.stop, local_port=args.port)
    elif args.version:
        DisplayShadowsocksr.display_version()
    elif args.setting_url:
        UpdateConfigurations.reset_subscribe_url(args.setting_url)
    elif args.append_ssr:
        if not os.path.isfile(args.append_ssr):
            logger.error(f'append_ssr file {args.append_ssr} is not exists')
            return
        with open(args.append_ssr, 'r', encoding='UTF-8') as f:
            txt = f.read()
        if args.b:
            txt = ParseShadowsocksr.base64_decode(txt)
        ssr_set = set()
        for line in txt.splitlines():
            for ssr in re.findall(r'ssr://[0-9a-zA-Z=-_/+]+', line):
                ssr_set.add(ssr)
        for ssr in ssr_set:
            try:
                UpdateConfigurations.append_ssr_node(ssr)
            except Exception as e:
                logger.error(f'add ssr node error {ssr}')
                logger.error(traceback.format_exc())
    elif args.clear_ssr:
        UpdateConfigurations.clear_ssr_nodes(args.clear_ssr, args.all)
    elif args.setting_address:
        UpdateConfigurations.update_local_address(args.setting_address)
    elif args.list_url:
        DisplayShadowsocksr.display_subscribe_url()
    elif args.add_url:
        UpdateConfigurations.add_subscribe_url(args.add_url)
    elif args.remove_url:
        UpdateConfigurations.remove_subscribe_url(args.remove_url)
    elif args.list_address:
        DisplayShadowsocksr.display_local_address()
    elif args.parse_url:
        DisplayShadowsocksr.display_shadowsocksr_json_by_url(args.parse_url)
    elif args.add_ssr:
        UpdateConfigurations.add_shadowsocksr_by_url(args.add_ssr)
    elif args.test_again is not None:
        UpdateConfigurations.update_shadowsocksr_connect_status(ssr_id=args.test_again)
    elif args.print_qrcode is not None:
        DisplayShadowsocksr.display_qrcode(ssr_id=args.print_qrcode)
    elif args.setting_global_proxy:
        UpdateSystemProxy.open_global_proxy(args.port, args.http_port)
    elif args.setting_pac_proxy:
        UpdateSystemProxy.open_pac_proxy(args.port, args.http_port)
    elif args.close_system_proxy:
        UpdateSystemProxy.close_proxy(args.port, args.http_port)
    elif args.test_speed is not None:
        DisplayShadowsocksr.display_shadowsocksr_speed(ssr_id=args.test_speed)
    elif args.display_json is not None:
        DisplayShadowsocksr.display_shadowsocksr_json(ssr_id=args.display_json)
    elif args.generate_clash:
        GenerateClashConfig.generate_clash_config()
    elif args.http:
        HandleHttpServer.handle_http_server(args.http, args.port, args.http_port)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
