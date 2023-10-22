import pandas as pd
class TestClass:
    def test_text_prg(self):
        df = pd.read_csv("src/lang/text_prg.csv")
        assert True not in df.isna().iloc[0].to_list()

    def test_two(self):
        class Perso:
            def check(self):
                pass
        x = Perso
        assert hasattr(x, "check")