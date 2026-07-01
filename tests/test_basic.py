import unittest

from core.compiler import ATUCompiler


class ATUCompilerTest(unittest.TestCase):
    def test_compile(self):
        compiler = ATUCompiler()
        output = compiler.compile([{"trace_id": "1", "spans": []}])
        self.assertEqual(len(output), 1)
        self.assertEqual(output[0]["episode_id"], "1")
        self.assertIs(output[0]["labels"]["success"], True)


if __name__ == "__main__":
    unittest.main()
