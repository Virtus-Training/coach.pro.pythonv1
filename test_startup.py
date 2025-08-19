import unittest


class TestAppStartup(unittest.TestCase):
    def test_app_instantiation(self):
        """Vérifie que la classe CoachApp peut être instanciée sans erreur."""
        try:
            from app import CoachApp

            app_instance = CoachApp()
            app_instance.destroy()

            self.assertTrue(True, "L'application s'est instanciée avec succès.")
        except Exception as e:
            self.fail(f"L'instanciation de l'application a échoué : {e}")


if __name__ == "__main__":
    unittest.main()
