from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily, StateSetMetricFamily
from datetime import datetime

import logging
logger = logging.getLogger('CustomPrometheusServer')

# For test/debug basic operation - register in main
class CustomMetricsCollector(object):
    def __init__(self):
        self.fake_buffer_delta = 1
        self.fake_buffer_level = -self.fake_buffer_delta # compensate for internal read during server init
        self.fake_buffer_max = 10
        self.fake_rx_pkt_delta = 10
        self.fake_rx_pkts = -self.fake_rx_pkt_delta # compensate for internal read during server init
        self.fake_status = True

    def collect(self):
        # Normally you'd fetch real data from your back-end system using an RPC such as REST or gRPC.
        # Here we fake the data internally.

        # Ever-increasing counter
        self.fake_rx_pkts = self.fake_rx_pkts + self.fake_rx_pkt_delta

        # Triangle-wave guage cycles from 0-10 and back
        self.fake_buffer_level = self.fake_buffer_level + self.fake_buffer_delta
        if self.fake_buffer_level > self.fake_buffer_max:
            self.fake_buffer_level = self.fake_buffer_max-1
            self.fake_buffer_delta = self.fake_buffer_delta*-1
        elif self.fake_buffer_level < 0:
            self.fake_buffer_delta = self.fake_buffer_delta*-1
            self.fake_buffer_level = 1

        # Toggle the status
        if self.fake_status is True:
            self.fake_status = False
        else:
            self.fake_status = True
            
        logger.debug("SampleMetricsCollector()")

        # Fake gauge - non-monotonic type of data - can increase, decrease
        label_names = ['portnum','type', 'speed']
        label_values = ['1', 'Ethernet', '100GBPS']
        g = GaugeMetricFamily('buffer_level_bytes', 'The number of bytes stored in a buffer', labels=label_names)
        g.add_metric(labels=label_values, value=self.fake_buffer_level)
        yield g
        
        # Fake counter - monotonic type of data (never decreases)
        # We'll reuse labels to illustrate how many metrics can have the same metadata, useful for query grouping
        c = CounterMetricFamily('rx_packets', 'The number of packets received', labels=label_names)
        c.add_metric(labels=label_values, value=self.fake_rx_pkts)
        yield c

        # Enumerated "State" values
        s = StateSetMetricFamily('port_link_status', 'Link state of an interface (port)', labels=label_names)
        s.add_metric(labels=label_values,value={'UP':True} if self.fake_status else {'DOWN':False}, timestamp=datetime.now().timestamp())
        yield s

        # Repeat the block of metrics but change labels & values to simulate multple "ports"
        label_values = ['2', 'Ethernet', '50GBPS']

        # Fake gauge, value is the complement of the first port's value
        g = GaugeMetricFamily('buffer_level_bytes', 'The number of bytes stored in a buffer', labels=label_names)
        g.add_metric(labels=label_values, value=self.fake_buffer_max-self.fake_buffer_level)
        yield g
        
        # Fake counter - value is twice the first port's
        # We'll reuse labels to illustrate how many metrics can have the same metadata, useful for query grouping
        c = CounterMetricFamily('rx_packets', 'The number of packets received', labels=label_names)
        c.add_metric(labels=label_values, value=self.fake_rx_pkts*2)
        yield c

        # Status value - opposite of first port's status
        s = StateSetMetricFamily('port_link_status', 'Link state of an interface (port)', labels=label_names)
        s.add_metric(labels=label_values,value={'UP':True} if not self.fake_status else {'DOWN':False}, timestamp=datetime.now().timestamp())
        yield s

