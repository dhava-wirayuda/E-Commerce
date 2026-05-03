import random
from locust import HttpUser, task, between, events

class ECommerceUser(HttpUser):
    # Jeda antar request (simulasi user membaca/scroll) selama 1-5 detik
    wait_time = between(1, 5)

    # 1. SEMUA USER (Weight: 10) - Membuka List Produk
    @task(10)
    def open_home(self):
        with self.client.get("/api/products", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Gagal memuat produk: {response.status_code}")

    # 2. SEBAGIAN BESAR USER (Weight: 7) - Melihat Detail Produk
    @task(7)
    def view_detail(self):
        # Mengambil detail produk ID 1
        self.client.get("/api/products/1")

    # 3. BEBERAPA USER (Weight: 3) - Mencoba Login
    @task(3)
    def login(self):
        payload = {
            "username": "admin",
            "password": "admin123"
        }
        self.client.post("/api/user/login", json=payload)

    # 4. SEDIKIT USER (Weight: 1) - Memberikan Review
    @task(1)
    def post_review(self):
        payload = {
            "productId": 1,
            "user": "Python Locust User",
            "rating": 5,
            "comment": "Testing dari Python!",
            "date": "2024-03-05"
        }
        self.client.post("/api/reviews", json=payload)

# Untuk menjalankan via command line:
# locust -f locustfile.py
