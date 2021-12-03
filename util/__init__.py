import yaml
import os
from dataclasses import dataclass
from typing import List

# For compatibility between Pycharm and vanilla command line run configurations
if os.path.exists('./localconfig.yaml'):
    config_path = './localconfig.yaml'
elif os.path.exists('../localconfig.yaml'):
    config_path = '../localconfig.yaml'
else:
    print('[-] Error: Failed to find localconfig.yaml file')

if os.path.exists('./results/README.md'):
    results_path = './results'
elif os.path.exists('../results/README.md'):
    results_path = '../results'
else:
    print('[-] Error: Failed to find results directory')

with open(config_path, 'r') as f:
    SETTINGS = yaml.safe_load(f)


@dataclass
class InclusionCriteria:
    pc_open: List[str]
    pc_lap: List[str]
    anast_open: List[str]
    anast_lap: List[str]

    def get_all_pc(self):
        return self.pc_open + self.pc_lap

    def get_all_anast(self):
        return self.anast_open + self.anast_lap

    def get_all_lap(self):
        return self.pc_lap + self.anast_lap

    def get_all_open(self):
        return self.pc_open + self.anast_open


inclusionCriteria = InclusionCriteria(
    pc_open=['0DBE0ZZ', '0DTH0ZZ', '0DTF0ZZ', '0DTK0ZZ', '0DTL0ZZ', '0DTG0ZZ', '0DTN0ZZ', '4571', '4572', '4573',
             '4574', '4575', '4576', '4578'],
    pc_lap=['0DBE3ZZ', '0DBGFZZ', '0DBLFZZ', '0DBMFZZ', '0DBNFZZ', '0DTMFZZ', '0DTLFZZ', '0DTGFZZ', '0DTNFZZ',
            '0DBE4ZZ', '0DTF4ZZ', '0DTH4ZZ', '0DTL4ZZ', '0DTG4ZZ', '0DTN4ZZ', '1731', '1732', '1733', '1734', '1735',
            '1736', '1739'],
    anast_open=['0D1H0ZH', '0D1H0ZK', '0D1H0ZL', '0D1H0ZM', '0D1H0ZN', '0D1H0ZP', '0D1K0ZK', '0D1K0ZL', '0D1K0ZM',
                '0D1K0ZN', '0D1K0ZP', '0D1L0ZL', '0D1L0ZM', '0D1L0ZN', '0D1L0ZP', '0D1M0ZM', '0D1M0ZN', '0D1M0ZP',
                '0D1N0ZN', '0D1N0ZP', '0D190ZL', '0D1A0ZH', '0D1A0ZK', '0D1A0ZL', '0D1A0ZM', '0D1A0ZN', '0D1B0ZH',
                '0D1B0ZK', '0D1B0ZL', '0D1B0ZM', '0D1B0ZN', '4594', '4593'],
    anast_lap=['0D1H4ZH', '0D1H4ZK', '0D1H4ZL', '0D1H4ZM', '0D1H4ZN', '0D1H4ZP', '0D1K4ZK', '0D1K4ZL', '0D1K4ZM',
               '0D1K4ZN', '0D1K4ZP', '0D1L4ZL', '0D1L4ZM', '0D1L4ZN', '0D1L4ZP', '0D1M4ZM', '0D1M4ZN', '0D1M4ZP',
               '0D1N4ZN', '0D1N4ZP', '0D194ZL', '0D1A4ZH', '0D1A4ZK', '0D1A4ZL', '0D1A4ZM', '0D1A4ZN', '0D1B4ZH',
               '0D1B4ZK', '0D1B4ZL', '0D1B4ZM', '0D1B4ZN']
)

labels = ['DIED', 'LOS', 'anastomotic_leak']
