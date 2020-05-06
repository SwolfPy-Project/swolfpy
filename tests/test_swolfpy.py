#!/usr/bin/env python

"""Tests for `swolfpy` package."""
import pytest
from swolfpy import *
from swolfpy.ProcessModels import LF


class test_swolfpy():
    def test_LF():
        A=LF.LF()
        A.calc()
        B=A.report()
        assert len(B)==4
      
    

