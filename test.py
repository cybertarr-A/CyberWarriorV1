from modules.ai_analysis import AICore

# Create mock result objects with expected attributes
class MockReconData:
    def __init__(self):
        self.headers = {"Server": "Apache", "Content-Type": "text/html"}

class MockScanData:
    def __init__(self):
        self.open_ports = [22, 80, 443]

class MockExploitData:
    def __init__(self):
        self.findings = ["SQL Injection found", "XSS vulnerability"]

def test_ai_analyze():
    ai = AICore()

    recon_data = MockReconData()
    scan_data = MockScanData()
    exploit_data = MockExploitData()

    summary = ai.analyze(recon_data, scan_data, exploit_data)
    print("AI Analysis Summary:\n", summary)

if __name__ == "__main__":
    test_ai_analyze()
