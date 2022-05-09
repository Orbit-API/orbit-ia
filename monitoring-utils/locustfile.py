from locust import HttpUser, between, task


class Orbit(HttpUser):
    wait_time = between(5, 15)
    
    @task
    def cadastro(self):
        self.client.post("/users", {
            "name": "Teste Usuário",
            "email": "teste@email.com",
            "password": "passwordteste",
            "phone": "123644125"
        })
    
    @task
    def exibicao(self):
        self.client.get("/users")
