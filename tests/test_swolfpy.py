#!/usr/bin/env python

"""Tests for `swolfpy` package."""


from swolfpy import *
from swolfpy.ProcessModels import LF


class TestPyswolf():
    def test():
        A=LF.LF()
        A.calc()
        B=A.report()
        assert len(B)==3
      
    

