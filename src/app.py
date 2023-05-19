from diff_finder import DiffFinder
from flask import Flask
from controllers.blueprints import index_bp
from cpl_adapter import CPLAdapter
import argparse
import logging
import yaml

app = Flask(__name__)

def parse_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('--data-folder', type=str, help='config folder location', default='data')
    parser.add_argument('--config-file', type=str, help='config file location (inside --data-folder)', default='config.yaml')
    parser.add_argument('--port', '-p', type=int, help='Port that the app will listen on', default=8080)
    parser.add_argument('--log-level', type=str, help='Log Level', choices=["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"], default='INFO')
    args = parser.parse_args()
    return args

def main(args):
    logger.info(f'Initializing app')

    logger.info(f'Reading config file: {args.data_folder}/{args.config_file}')
    with open(f'{args.data_folder}/{args.config_file}', 'r') as fd:
        config = yaml.safe_load(fd)

    cpl_config = "config/cpl.yaml"
    adapter = CPLAdapter(logger, cpl_config)

    diff_finder = DiffFinder(logger, adapter, config, args.data_folder)
    diff_finder.run()

    app.config['logger'] = logger
    app.config['diff_finder'] = diff_finder
    app.config['user_config'] = config
    app.config['user_keys'] = [x['name'] for x in config['configs']]
    app.register_blueprint(index_bp)
    port = args.port
    #app.run(host='0.0.0.0', port=port, debug=(args.log_level=='DEBUG'), use_reloader=False)

if __name__ == "__main__":
    args = parse_args()
    logging.basicConfig(format='{"asctime": "%(asctime)s", "filename": "%(filename)s", "lineno": "%(lineno)d", "name": "%(name)s", "levelname": "%(levelname)s", "message": "%(message)s"}', level=args.log_level)
    logger = logging.getLogger('cpl-museum-passes')
    logger.setLevel(args.log_level)
    main(args)