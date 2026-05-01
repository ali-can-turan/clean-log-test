import os
import sys
import re
import pytest
import pandas as pd
import numpy as np
from src.cleaning import Cleaning 


class TestCleaning():
	"""Below, all the methods of Cleaning class in the src/cleaning module are tested."""
	print("\nTest started.")
	
	@pytest.fixture(scope="module", autouse=True)
	def data_setup(self):
		data = {
			"input": [".as_d", "a.sd_", np.nan],
			"date": ["12.12.2001", "12.12.2001", np.datetime64("NaT")],
		}
		df_raw = pd.DataFrame(data)
		df_test = Cleaning(df_raw)
		yield df_test
		print("\nTest ended.")

	@pytest.mark.data_cleaning
	def test_str_clean(self, data_setup):
		test = data_setup.str_clean(columns_chars={"input": r"[_.]"}, regex=True)
		has_chars = test["input"].str.contains(r"[_.]").any()
		assert has_chars == False, "str_clean function does not work properly."

	@pytest.mark.data_cleaning
	def test_case_assign(self, data_setup):
		test = data_setup.case_assign(columns_cases={"input":"upper"})
		not_cased = test["input"].str.contains(r"[a-z]").any()
		assert not_cased == False, "case_assign function does not function properly."

	@pytest.mark.important
	def test_datetime_converter(self, data_setup):
		print(f"Input dtype is {data_setup.df["date"].dtype}")
		test = data_setup.datetime_converter(columns=["date"], to="datetime")
		converted = pd.api.types.is_datetime64_dtype(test["date"])
		assert converted, "datetime_converter function does not function properly."

	@pytest.mark.other
	def test_null_rows(self, data_setup):
		test = data_setup.null_rows(columns=["input"])
		assert int("".join(re.findall(r"\d+", test))) == 1, "One null row/cell could NOT be found."

	@pytest.mark.skip(reason="Not necessary at the moment.")
	def test_outlier_z(self):
		pass

	@pytest.mark.skip(reason="Not necessary at the moment.")
	def test_outlier_iqr(self):
		pass

	@pytest.mark.other
	def test_column_reorder(self, data_setup):
		test = data_setup.column_reorder(columns_idx={"date": 0})
		zero_index = test.columns.tolist()[0]
		assert zero_index == "date", "Column could not be reordered."

	@pytest.mark.important
	def test_numeric_entry_df_generator(self, data_setup):
		test = data_setup.numeric_entry_df_generator(2)
		print(test)
		assert not test.notnull().values.any(), "A df of null cells should have been constructed."