from prometheus_client import start_http_server, Summary
from prometheus_client.core import REGISTRY
from custom_metrics_collector import custom_metrics
import time, argparse

import logging
logger = logging.getLogger('CustomPrometheusServer')

def run():
    # Here we can register one or more collector callback handlers.
    REGISTRY.register(custom_metrics.CustomMetricsCollector())

    # Replace PORT with a cmd-line parameter
    start_http_server(args.port)
    while True:
        # Do nothing in foreground; server thread processes http requests
        time.sleep(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Custom Prometheus Metrics Server')
    parser.add_argument('--port', default='8000', type=int, help='server port to listen on [8000]')
    args = parser.parse_args()

    logger.setLevel(logging.DEBUG)
    log_format = '[%(asctime)-15s] [%(levelname)08s] %(module)s.%(funcName)s-%(lineno)d: %(message)s'
    logging.basicConfig(format=log_format)
    logger.info("Prometheus server listening on port %s" % args.port)
    run()
