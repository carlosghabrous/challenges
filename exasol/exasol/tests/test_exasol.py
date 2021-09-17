'''
High-level tests for the  package.
'''
import exasol
def test_version():
	assert exasol.__version__ is not None