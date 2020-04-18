from twisted.trial import unittest

from jiaowu.console.instruction import Instruction


class ConsoleTest(unittest.TestCase):
    def test_instruction_validity1(self):
        ins=Instruction("applyforexamonly -cn 12345")
        self.assertEqual( ins.is_valid(),True)

    def test_instruction_validity2(self):
        ins=Instruction("applyforexamonly -cn ")
        self.assertEqual( ins.is_valid(),False)

    def test_instruction_validity3(self):
        ins=Instruction("applyforexamonly -ci 12345 ")
        self.assertEqual( ins.is_valid(),True)

    def test_instruction_validity4(self):
        ins=Instruction("applyforexamonly -ci ")
        self.assertEqual( ins.is_valid(),False)

    def test_instruction_validity5(self):
        ins=Instruction("quit ")
        self.assertEqual( ins.is_valid(),True)

    def test_instruction_validity6(self):
        ins=Instruction("quit -x ")
        self.assertEqual( ins.is_valid(),False)

    def test_instruction_validity7(self):
        ins = Instruction("checkcurriculum ")
        self.assertEqual(ins.is_valid(), False)

    def test_instruction_validity8(self):
        ins = Instruction("checkcurriculum -y 2018 -t 1 -g 2018 -m xxx")
        self.assertEqual(ins.is_valid(), True)

    def test_instruction_validity9(self):
        ins = Instruction("checktimetable ")
        self.assertEqual(ins.is_valid(), True)

    def test_instruction_validity10(self):
        ins = Instruction("checkgrades")
        self.assertEqual(ins.is_valid(), False)

    def test_instruction_validity11(self):
        ins = Instruction("checkgrades -y 2018 -t 1")
        self.assertEqual(ins.is_valid(), True)

    def test_instruction_validity12(self):
        ins = Instruction("checknews")
        self.assertEqual(ins.is_valid(), True)

    def test_instruction_validity13(self):
        ins = Instruction("saveasexcel -fp xxx -dt xx")
        self.assertEqual(ins.is_valid(), True)