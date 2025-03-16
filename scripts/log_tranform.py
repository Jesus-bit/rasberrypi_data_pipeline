import re
from collections import Counter


class LogTransformer:
    def __init__(self, log_file):
        self.log_file = log_file
        self.error_count = 0
        self.info_count = 0
        self.debug_count = 0

    def parse_logs(self):
        log_pattern = re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} - .* - (INFO|DEBUG|ERROR)')
        
        with open(self.log_file, 'r') as file:
            for line in file:
                match = log_pattern.search(line)
                if match:
                    level = match.group(1)
                    if level == 'INFO':
                        self.info_count += 1
                    elif level == 'DEBUG':
                        self.debug_count += 1
                    elif level == 'ERROR':
                        self.error_count += 1

    def get_summary(self):
        return {
            'INFO': self.info_count,
            'DEBUG': self.debug_count,
            'ERROR': self.error_count
        }


if __name__ == "__main__":
    log_transformer = LogTransformer("./data/raw_logs/app_debug.log")
    log_transformer.parse_logs()
    print(log_transformer.get_summary())
