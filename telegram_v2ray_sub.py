import re
import json
import base64

from flask import Flask, request
from snscrape.modules.telegram import TelegramChannelScraper

import settings

app = Flask(__name__)


@app.route('/sub')
def subscription():
    channel_name = request.args.get('channel', settings.DEFAULT_CHANNEL)
    if channel_name is None:
        return 'channel name is required'

    desired_protocols = request.args.get('protocols', '')
    config_count = int(request.args.get('count', settings.CONFIG_COUNT))
    post_count = settings.POST_COUNT

    valid_protocols = {'vless', 'vmess', 'ss', 'trojan'}
    if desired_protocols:
        if len(set(desired_protocols.split(',')) - valid_protocols) == 0:
            target_protocols = desired_protocols.split(',')
        else:
            return 'some protocols are invalid'
    else:
        target_protocols = valid_protocols

    result = ''
    config_counter = 0
    post_counter = 0

    for i, post in enumerate(TelegramChannelScraper(channel_name).get_items()):
        if post.content is None:
            continue
        post_counter += 1

        post_id = post.url.split('/').pop()
        for config_idx, config in find_configs(target_protocols, post.content):
            config_name = channel_name + '-' + post_id + '-' + str(config_idx + 1)
            final_config = rename_config(config, config_name)
            if final_config == '':
                continue

            result += final_config + '\n'
            config_counter += 1
            if config_counter >= config_count:
                break

        if config_counter >= config_count or post_counter >= post_count:
            break

    if not result:
        return 'invalid channel'

    return result


def find_configs(target_protocols, text):
    for config_idx, conf in enumerate(re.findall(f'(({"|".join(target_protocols)}):\/\/[^\s]+)', text)):
        config, _ = conf

        if config.count('://') > 1:
            idx = 0
            splitted_configs = config.split('://')
            for inner_idx, inner_config in enumerate(splitted_configs):
                for target_protocol in target_protocols:
                    if inner_config.endswith(target_protocol) and len(splitted_configs) >= inner_idx + 1:
                        final_config = inner_config[-len(target_protocol):] + '://' + splitted_configs[inner_idx + 1]
                        yield config_idx + idx, final_config
                        idx += 1
                        break
        else:
            yield config_idx, config


def rename_config(config, config_name):
    protocol = config.split('://')[0]
    if protocol == 'vmess':
        decoded_config = ''
        for i in range(len(config))[::-1]:
            try:
                config_b64 = config[len(protocol):i]
                decoded_config = base64.b64decode(config_b64).decode('utf-8')
                break
            except:
                pass

        if not decoded_config:
            return ''

        parsed_config = json.loads(decoded_config)
        parsed_config['ps'] = config_name
        stringify_config = json.dumps(parsed_config)
        encoded_config = base64.b64encode(stringify_config.encode('utf-8')).decode('utf-8')
        return protocol + '://' + encoded_config

    else:
        if config.count('#') < 1:
            return ''

        hashtag_index = config.index('#')
        return config[:hashtag_index + 1] + config_name


if __name__ == "__main__":
    app.run(debug=True)
