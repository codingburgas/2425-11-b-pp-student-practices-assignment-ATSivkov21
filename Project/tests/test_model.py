import unittest
import numpy as np
from app.utils.ai_model import SimpleLogisticRegression

class ModelTestCase(unittest.TestCase):
    def setUp(self):
        self.model = SimpleLogisticRegression()
        self.X = np.array([[0.2, 0.5, 0.3, 0.4], [0.9, 0.1, 0.5, 0.2]])
        self.y = np.array([0, 1])

    def test_fit_predict(self):
        self.model.fit(self.X, self.y, epochs=200)
        predictions = self.model.predict(self.X)
        self.assertEqual(len(predictions), 2)

    def test_predict_proba(self):
        self.model.fit(self.X, self.y)
        probas = self.model.predict_proba(self.X)
        self.assertTrue(np.all((probas >= 0) & (probas <= 1)))