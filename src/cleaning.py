import pandas as pd
import numpy as np
import numpy.random as rnd
import random
from IPython.display import display

from src.logger import logger


class ParamError(Exception):
	pass


class Cleaning():

	def __init__(self, df):
		self.df = df

	def str_clean(self, columns_chars: dict, replace_char:str="", regex:bool=False):
		"""
		Summary: It replaces the unwanted chars in dataframe columns' contents with the one(s) desired.
		Args: Dataframe column names and chars to be replaced in those columns; replace char, optional; regex boolean, optional.
		Return: Dataframe columns in dataframe.
		Note: Char to replace will replace all the chars to be replaced in all the columns declared colectively.
		Raises: TypeError if the columns or the char to replace are not stringlike.
		"""
		logger.info(f"Function is called.")
		for column, char in columns_chars.items():
			if pd.api.types.is_string_dtype(self.df[column])\
			or pd.api.types.is_object_dtype(self.df[column])\
			or pd.api.types.is_categorical_dtype(self.df[column]):
				if isinstance(char, str):
					logger.debug(f"Process STARTED for column {column} and for char {char}.")
					self.df[column] = self.df[column].str.replace(pat=char, repl=replace_char, regex=regex).str.strip()
					logger.debug(f"Process COMPLETED SUCCESSFULLY for column {column} and for char {char}.\n")
					print(f"The column '{column}':cleaned.\n")
				else:
					logger.error(f"Type error for char {char} will be raised.")
					raise TypeError(f"The char '{char}' is not string.")
			else:
				logger.error(f"Type error for column {column} will be raised.")
				raise TypeError(f"The column '{column}' dtype is not stringlike.")
		return self.df[columns_chars.keys()].reset_index(drop=True)

	def case_assign(self, columns_cases:dict):
		"""
		Summary: It converts dataframe columns' cases already in place into the given cases.
		Args: Dataframe column names and cases for columns to be converted into.
		Return: Dataframe columns in dataframe.
		Raises: TypeError if columns or target cases are not stringlike or unknown.
		"""
		logger.info(f"Function is called.")
		for column, case in columns_cases.items():
			if case in ["upper", "lower", "title"]:
				if pd.api.types.is_string_dtype(self.df[column])\
				or pd.api.types.is_object_dtype(self.df[column])\
				or pd.api.types.is_categorical_dtype(self.df[column]):
					logger.debug(f"Process STARTED for column {column} and for case {case}.")
					self.df[column] = getattr(self.df[column].str, case)()
					self.df[column] = self.df[column].str.strip()
					logger.debug(f"Process COMPLETED SUCCESSFULLY for column {column} and for case {case}.\n")
					print(f"The column '{column}':{case} case assigned.\n")
				else:
					logger.error(f"Type error for column {column} will be raised.")
					raise TypeError(f"The column '{column}' dtype is not stringlike.")
			else:
				logger.error(f"Type error for case type {case} will be raised.")
				raise TypeError(f"Unknown case type, please handle case type '{case}' individually via pandas.")
		return self.df[columns_cases.keys()].reset_index(drop=True)

	def datetime_converter(self, columns:list, to:str="str"):
		"""
		Summary: It converts 'datetime-like' columns' contents into the datetime type desired.
		Args: Dataframe column names and the type that those columns are desired to be converted into.
		Return: Dataframe columns in dataframe.
		Note: The defined type in parameter 'to' will be employed for all the columns defined in the parameter 'columns'.
		Raises: ParamError if the parameter "to" is not integerlike, datetimelike, or stringlike.
		"""
		logger.info(f"Function is called.")
		for column in columns:
			if to in ["datetime", "int", "str"]:
				if pd.api.types.is_integer_dtype(self.df[column])\
				or pd.api.types.is_string_dtype(self.df[column])\
				or pd.api.types.is_object_dtype(self.df[column]):
					if to == "datetime":
						logger.debug(f"Process STARTED for column {column} and for the format {to}.")
						self.df[column] = pd.to_datetime(self.df[column], format="mixed", errors="coerce", utc=False)
						logger.debug(f"Process ENDED SUCCESSFULLY for column {column} and for the format {to}.\n")
					else:
						logger.error(f"Param error for format type{to} will be raised.")
						raise ParamError(f"When the dtype is stringlike or numeric, it is only possible to convert into datetimelike dtype.")
				elif pd.api.types.is_datetime64_any_dtype(self.df[column]):
					if to == "int":
						logger.debug(f"Process STARTED for column {column} and for the format {to}.")
						self.df[column] = pd.to_numeric(self.df[column], errors="coerce", downcast="float")
						logger.debug(f"Process ENDED SUCCESSFULLY for column {column} and for the format {to}.\n")
					elif to == "str":
						self.df[column] = self.df[column].dt.strftime("%d.%m.%Y").astype("string")
						logger.debug(f"Process ENDED SUCCESSFULLY for column {column} and for the format {to}.\n")
					else:
						logger.error(f"Param error for format type {to} will be raised.")
						raise ParamError(f"When the dtype is datetimelike, it is only possible to convert into string or numeric dtype.")
				else:
					logger.error(f"Type error for column {column} dtype will be raised.")
					raise TypeError(f"Unknown dtype {str(self.df[column].dtype)} for column {column}', please handle individually via pandas.")
			else:
				logger.error(f"Param error for desired format will be raised.")
				raise ParamError(f"The desired format in param {to} should be 'int', 'str' or 'datetime'.")
		return self.df[columns]

	def null_rows(self, columns:list, separator:str=None):
		"""
		Summary: It yields the count of null rows specific to the given columns.
		Args: Dataframe column names and a separator to construct boolean relation between the columns.
		Return: Dataframe columns in dataframe.
		Note: More complicated boolean relations such as nested boolean relations cannot be performed.
		Raises: ParamError if the parameter 'separator' is not among "|", "&", "and", and "or".
		"""
		logger.info(f"Function is called.")
		eval_string = ""
		if separator in ["|", "&", "and", "or", None]:
			logger.debug(f"Process STARTED for the separator {separator}.")
			for column in columns:
					if column != columns[-1]:
						eval_string += f"self.df['{column}'].isna() {separator} "
					else:
						eval_string += f"self.df['{column}'].isna()"
						if len(columns) == 1:
							print(f"The parameter 'separator' entry will be ignored as only one column name defined in the parameter 'columns'.")
			logger.debug(f"Process ENDED SUCCESSFULLY for the separator {separator}.\n")
		else:
			logger.error(f"Param error for desired separator will be raised.")
			raise ParamError(f"Separator unknown: please handle separator '{separator}' individually via pandas. ")
		return f"Null row count: {self.df.loc[eval(eval_string)].shape[0]}"

	def outlier_z(self, op:str, col:str, group_by:str=None, z_abs_thresh:int=3):
		"""
		Summary: It calculates z scores for the content of any given column, and construct a new column thereof.
		Args: Dataframe column name to catch outliers of; a group by column name, optional but advised; a positive z score threshold, optional.
		Return: It calls one of its methods via the 'op' parameter: either 'bins' or 'adopt'. 
				'bins' yields 1. the count of cells that either fall within or stay out of the z score threshold defined, 2. the new z score column in dataframe and 3. the first 5 rows of the either sides of the threshold.
				'adopt' yields the new dataframe that fits within the threshold.
		Note: if 'adopt' to be used in the parameter 'op', it is strongly advised to assign it to a new data frame. Otherwise, note that there will be no change in the dataframe the object carries. 
		"""	
		logger.info(f"Function is called.")
		if op in ["bins", "adopt"]:
			if group_by:
				self.df.loc[:,  f"z_scores_{col}"] = self.df.groupby(group_by)[col].transform(
					lambda values:
					(pd.to_numeric(values, errors='coerce') - pd.to_numeric(values, errors='coerce').mean()) / 
					pd.to_numeric(values, errors='coerce').std()
					if pd.to_numeric(values, errors='coerce').std() > 0 else 0
				)
			else:
				self.df.loc[:,  f"z_scores_{col}"] = self.df[col].transform(
					lambda values:
					(pd.to_numeric(values, errors='coerce') - pd.to_numeric(values, errors='coerce').mean()) / 
					pd.to_numeric(values, errors='coerce').std()
					if pd.to_numeric(values, errors='coerce').std() > 0 else 0
				)
		else:
			logger.error(f"Param error for param 'op' will be raised.")
			raise ParamError(f"Method unknown: type either 'bins' or 'adopt'.")
		z_column = self.df.loc[:,  f"z_scores_{col}"] 
		
		def _bins():
			logger.debug(f"Process STARTED for column {col} and for the param 'bins'.")
			mask_1 = z_column.abs() <= z_abs_thresh
			mask_2 = z_column.abs() > z_abs_thresh
			in_thresh_count = mask_1.sum()
			out_thresh_count = mask_2.sum()
			print(f"'{col}' has {in_thresh_count} cells in the z score range of {z_abs_thresh}.", "\n", \
				f"'{col}' has {out_thresh_count} cells out of the z score range of {z_abs_thresh}.", "\n")
			display(z_column.to_frame().head())
			
			print(f"Values inside the range {z_abs_thresh} (head):")
			display(self.df[mask_1].loc[:, [f"z_scores_{col}"]].head())
			print(f"Values outside the range {z_abs_thresh} (head):")
			display(self.df[mask_2].loc[:, [f"z_scores_{col}"]].head())
			logger.debug(f"Process COMPLETED SUCCESSFULLY for column {col} and for the param 'bins'.\n")

		def _adopt():
			logger.debug(f"Process STARTED for column {col} and for the param 'adopt'.")
			return self.df[self.df[f"z_scores_{col}"].abs() <= z_abs_thresh].reset_index(drop=True)
			logger.debug(f"Process COMPLETED SUCCESSFULLY for column {col} and for the param 'adopt'.\n")

		ops = {
		"bins" : _bins,
		"adopt" : _adopt
	}
		op = ops.get(op)
		return op()

	def outlier_iqr(self, op:str, col:str, coef:float=1.5, quantiles:list=[0.25, 0.75]):
		"""
		Summary:  It calculates interquartile range calculation.
		Return: It calls one of its methods via the 'op' parameter: either 'bins' or 'adopt'. 
				'bins' yields 1. the count of cells that either fall within or stay out of the quantiles defined, and 2. the first 5 rows of values that falls outside of the quantiles.
				'adopt' yields the new dataframe that fits within the quantiles.
		Note: if 'adopt' to be used in the parameter 'op', it is strongly advised to assign it to a new data frame. Otherwise, note that there will be no change in the dataframe the object carries.
		"""
		logger.info(f"Function is called.")
		if op in ["bins", "adopt"]:
			quantiles = sorted(quantiles)
			Q1, Q3 = self.df[col].quantile(quantiles)
			diff = Q3 - Q1
			lower = Q1 - diff * coef
			upper = Q3 + diff * coef
			under_count = (self.df[col] < lower).sum()
			above_count = (self.df[col] > upper).sum()
		else:
			logger.error(f"Param error for param 'op' will be raised.")
			raise ParamError(f"Method unknown: type either 'bins' or 'adopt'.")

		def _bins():
			logger.debug(f"Process STARTED for column {col} and for the operation 'bins'.")
			print(f"'{col}' has {under_count} cells that falls under quantile {quantiles}.\n", \
			f"'{col}' has {above_count} cells that go beyond quantile {quantiles}.\n")
			
			mask = self.df[col]
			print(f"Values inside the quantiles {quantiles} (head):")
			display(self.df[(mask >= lower) & (mask <= upper)].loc[:, [col]].head())
			print(f"Values outside the quantiles {quantiles} (head):")
			display(self.df[(mask < lower) | (mask > upper)].loc[:, [col]].head())
			logger.debug(f"Process COMPLETED SUCCESSFULLY for column {col} and for the param 'bins'.\n")

		def _adopt():
			logger.debug(f"Process STARTED for column {col} and for the operation 'adopt'.")
			return self.df[(self.df[col] >= lower) & (self.df[col] <= upper)].reset_index(drop=True)
			logger.debug(f"Process COMPLETED SUCCESSFULLY for column {col} and for the param 'adopt'.\n")

		ops = {
			"bins" : _bins,
			"adopt" : _adopt
		}
		op = ops.get(op)
		return op()

	def column_reorder(self, columns_idx:dict):
		"""
		Summary: It reorder columns of a dataframe.
		Args: column names and target indexes of these columns. 
		Return: Dataframe.
		Raise: IndexError if the specified target index is out of the index range of dataframe column list.
		"""
		logger.info(f"Function is called.")
		logger.debug(f"Process STARTED.")
		cols = self.df.columns.tolist()
		for col, index in columns_idx.items():
			if index < len(cols):
				cols.remove(col)
				cols.insert(index, col)
			else:
				logger.error(f"Index error will be raised.")
				raise IndexError("list index out of range")
		self.df = self.df[cols].reset_index(drop=True)
		logger.debug(f"Process COMPLETED SUCCESSFULLY.\n")
		return self.df

	def numeric_entry_df_generator(self, entry_num):
		"""
		Summary: It generates rows with random values for numeric columns and NaN / NaT values for the other.
		Args: Amount of rows to generate.
		Return: Generated rows in dataframe.
		Raise: TypeError if the type of sole parameter is not integerlike.
		"""
		logger.info(f"Function is called.")
		new_entry={}
		random.seed(42)
		logger.debug(f"Process STARTED.")
		for column in self.df.columns:
			new_entry[column] = []
			if isinstance(entry_num, int):
				for num in range(entry_num):
					if pd.api.types.is_integer_dtype(self.df[column]):
						new_entry[column].append(
							random.randint(
							self.df[column].min(),
							self.df[column].max())
						)
					elif pd.api.types.is_float_dtype(self.df[column]):
						new_entry[column].append(
						np.round(random.random() * self.df[column].max(), 2)
						)
					else:
						if pd.api.types.is_datetime64_any_dtype(self.df[column]):
						    new_entry[column].append(np.datetime64('NaT'))
						else:
						    new_entry[column].append(np.nan)
			else:
				logger.error(f"Type error for param entry_num will be raised.")
				raise TypeError("Please enter integer for the parameter 'entry_num'.")
		df_new_entry = pd.DataFrame(data=new_entry)
		logger.debug(f"Process COMPLETED SUCCESSFULLY.")
		return df_new_entry