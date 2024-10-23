from madr.utils import sanitize

def test_sanitize():
    tests = {
        "Machado de Assis": 'machado de assis',
        "Manuel        Bandeira": 'manuel bandeira',
        "Edgar Alan Poe         ": 'edgar alan poe',
        "Androides Sonham Com Ovelhas Elétricas?": 'androides sonham com ovelhas elétricas',
        "  breve  história  do tempo ": 'breve história do tempo',
        "O mundo assombrado pelos demônios": 'o mundo assombrado pelos demônios',
    }

    for k in tests:
        assert sanitize(k) == tests[k]