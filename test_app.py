
import unittest
import app

class TestDriveFin(unittest.TestCase):

    def setUp(self):
        self.cliente = app.app.test_client()

    def test_pagina_inicial(self):
        resposta = self.cliente.get("/")
        self.assertEqual(resposta.status_code, 200)

    def test_resumo_financeiro(self):
        resposta = self.cliente.get("/resumo")
        self.assertEqual(resposta.status_code, 200)

        dados = resposta.get_json()
        self.assertIn("total_receitas", dados)
        self.assertIn("total_despesas", dados)
        self.assertIn("lucro_liquido", dados)

        lucro_esperado = round(
            dados["total_receitas"] - dados["total_despesas"], 2
        )
        self.assertAlmostEqual(
            dados["lucro_liquido"], lucro_esperado, places=2
        )

    def test_cadastro_invalido(self):
        resposta = self.cliente.post("/lancamentos", json={
            "descricao": "Combustivel",
            "tipo": "despesa",
            "valor": -50
        })
        self.assertEqual(resposta.status_code, 400)

if __name__ == "__main__":
    unittest.main()
