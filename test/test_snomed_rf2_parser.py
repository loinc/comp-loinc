"""Unit tests for SNOMED RF2 parser functions"""

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch
from typing import List, Tuple

import pandas as pd

# Import the module we're testing
try:
    from src.comp_loinc.analysis.snomed_rf2_parser import (
        _get_expressions,
        _get_labels,
        _write,
        _borrow_ontology_block_opener_and_prefixes_from_snomed,
        _validate_module_name,
        _resolve_config_arguments,
        DEFAULT_ONTOLOGY_BLOCK_OPENER,
        DEFAULT_PREFIXES_TAGS,
        SNOMED_MODULE_NAME,
        LOINC_SNOMED_MODULE_NAME,
        DEFAULTS,
    )
except ImportError:
    # If running from test directory
    import sys

    sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
    from comp_loinc.analysis.snomed_rf2_parser import (
        _get_expressions,
        _get_labels,
        _write,
        _borrow_ontology_block_opener_and_prefixes_from_snomed,
        _validate_module_name,
        _resolve_config_arguments,
        DEFAULT_ONTOLOGY_BLOCK_OPENER,
        DEFAULT_PREFIXES_TAGS,
        SNOMED_MODULE_NAME,
        LOINC_SNOMED_MODULE_NAME,
        DEFAULTS,
    )


class TestSnomedRF2Parser(unittest.TestCase):
    """Test cases for SNOMED RF2 parser functions"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_owl_file = os.path.join(self.temp_dir, "test_owl.tsv")
        self.temp_labels_file = os.path.join(self.temp_dir, "test_labels.tsv")
        self.temp_output_file = os.path.join(self.temp_dir, "test_output.ofn")

    def tearDown(self):
        """Clean up test fixtures"""
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_get_expressions_valid_input(self):
        """Test _get_expressions with valid input data"""
        # Create test OWL data
        test_data = {
            "owlExpression": [
                "Ontology(<http://test.example.org>)",
                "Prefix(owl:=<http://www.w3.org/2002/07/owl#>)",
                "SubClassOf(:123456 :789012)",
                "EquivalentClasses(:345678 ObjectIntersectionOf(:901234 :567890))",
            ]
        }
        df = pd.DataFrame(test_data)
        df.to_csv(self.temp_owl_file, sep="\t", index=False)

        ontology_opener, prefixes, axioms = _get_expressions(self.temp_owl_file)

        self.assertEqual(ontology_opener, "Ontology(<http://test.example.org>")
        self.assertEqual(len(prefixes), 1)
        self.assertIn("Prefix(owl:=<http://www.w3.org/2002/07/owl#>)", prefixes)
        self.assertEqual(len(axioms), 2)
        self.assertIn("SubClassOf(:123456 :789012)", axioms)

    def test_get_expressions_missing_ontology_header(self):
        """Test _get_expressions when ontology header is missing"""
        test_data = {
            "owlExpression": [
                "SubClassOf(:123456 :789012)",
                "EquivalentClasses(:345678 ObjectIntersectionOf(:901234 :567890))",
            ]
        }
        df = pd.DataFrame(test_data)
        df.to_csv(self.temp_owl_file, sep="\t", index=False)

        with patch(
            "src.comp_loinc.analysis.snomed_rf2_parser._borrow_ontology_block_opener_and_prefixes_from_snomed"
        ) as mock_borrow:
            mock_borrow.return_value = (
                DEFAULT_ONTOLOGY_BLOCK_OPENER,
                DEFAULT_PREFIXES_TAGS,
            )
            ontology_opener, prefixes, axioms = _get_expressions(self.temp_owl_file)

        self.assertEqual(ontology_opener, DEFAULT_ONTOLOGY_BLOCK_OPENER)
        self.assertEqual(prefixes, DEFAULT_PREFIXES_TAGS)
        mock_borrow.assert_called_once()

    def test_get_labels_valid_input(self):
        """Test _get_labels with valid input data"""
        test_data = {
            "conceptId": ["123456", "789012"],
            "term": ["Test Concept 1", "Test Concept (special chars!)"],
        }
        df = pd.DataFrame(test_data)
        df.to_csv(self.temp_labels_file, sep="\t", index=False)

        labels = _get_labels(self.temp_labels_file)

        self.assertEqual(len(labels), 2)
        # Check that special characters are removed
        self.assertIn(
            'AnnotationAssertion(<http://www.w3.org/2000/01/rdf-schema#label> :123456 "Test Concept 1")',
            labels,
        )
        self.assertIn(
            'AnnotationAssertion(<http://www.w3.org/2000/01/rdf-schema#label> :789012 "Test Concept special chars")',
            labels,
        )

    def test_write_function(self):
        """Test _write function creates proper OWL output"""
        ontology_opener = "Ontology(<http://test.example.org>)"
        prefixes = ["Prefix(owl:=<http://www.w3.org/2002/07/owl#>)"]
        axioms = ["SubClassOf(:123456 :789012)"]
        labels = [
            'AnnotationAssertion(<http://www.w3.org/2000/01/rdf-schema#label> :123456 "Test")'
        ]

        _write(self.temp_output_file, ontology_opener, prefixes, axioms, labels)

        with open(self.temp_output_file, "r") as f:
            content = f.read()

        self.assertIn("Prefix(owl:=<http://www.w3.org/2002/07/owl#>)", content)
        self.assertIn("Ontology(<http://test.example.org>)", content)
        self.assertIn("    SubClassOf(:123456 :789012)", content)
        self.assertIn(
            '    AnnotationAssertion(<http://www.w3.org/2000/01/rdf-schema#label> :123456 "Test")',
            content,
        )
        self.assertTrue(content.strip().endswith(")"))

    def test_validate_module_name_valid(self):
        """Test _validate_module_name with valid module names"""
        # These should not raise exceptions
        _validate_module_name(SNOMED_MODULE_NAME)
        _validate_module_name(LOINC_SNOMED_MODULE_NAME)

    def test_validate_module_name_invalid(self):
        """Test _validate_module_name with invalid module name"""
        with self.assertRaises(ValueError) as context:
            _validate_module_name("invalid_module")

        self.assertIn(
            "Module 'invalid_module' not found in DEFAULTS", str(context.exception)
        )
        self.assertIn("Available modules:", str(context.exception))

    def test_resolve_config_arguments_with_module(self):
        """Test _resolve_config_arguments with module-based defaults"""
        args_dict = {
            "by_module_name": SNOMED_MODULE_NAME,
            "inpath_owl": None,
            "inpath_labels": "/custom/path/labels.tsv",
            "outpath": None,
        }

        resolved = _resolve_config_arguments(args_dict.copy())

        # Should use module defaults but override with custom labels path
        self.assertEqual(resolved["inpath_labels"], "/custom/path/labels.tsv")
        self.assertNotIn("by_module_name", resolved)
        # Should have inpath_owl and outpath from defaults
        self.assertIn("inpath_owl", resolved)
        self.assertIn("outpath", resolved)

    def test_resolve_config_arguments_without_module(self):
        """Test _resolve_config_arguments without module name"""
        args_dict = {
            "by_module_name": None,
            "inpath_owl": "/path/to/owl.tsv",
            "inpath_labels": "/path/to/labels.tsv",
            "outpath": "/path/to/output.ofn",
        }

        resolved = _resolve_config_arguments(args_dict.copy())

        # Should use provided paths
        self.assertEqual(resolved["inpath_owl"], "/path/to/owl.tsv")
        self.assertEqual(resolved["inpath_labels"], "/path/to/labels.tsv")
        self.assertEqual(resolved["outpath"], "/path/to/output.ofn")
        self.assertNotIn("by_module_name", resolved)

    @patch("src.comp_loinc.analysis.snomed_rf2_parser._get_expressions")
    def test_borrow_ontology_block_opener_success(self, mock_get_expressions):
        """Test _borrow_ontology_block_opener_and_prefixes_from_snomed when file exists"""
        mock_get_expressions.return_value = (
            "test_ontology",
            ["test_prefix"],
            ["test_axiom"],
        )

        ontology, prefixes = _borrow_ontology_block_opener_and_prefixes_from_snomed(
            "/fake/path"
        )

        self.assertEqual(ontology, "test_ontology")
        self.assertEqual(prefixes, ["test_prefix"])

    @patch("src.comp_loinc.analysis.snomed_rf2_parser._get_expressions")
    def test_borrow_ontology_block_opener_file_not_found(self, mock_get_expressions):
        """Test _borrow_ontology_block_opener_and_prefixes_from_snomed when file doesn't exist"""
        mock_get_expressions.side_effect = FileNotFoundError("File not found")

        with patch("builtins.print") as mock_print:
            ontology, prefixes = _borrow_ontology_block_opener_and_prefixes_from_snomed(
                "/fake/path"
            )

        self.assertEqual(ontology, DEFAULT_ONTOLOGY_BLOCK_OPENER)
        self.assertEqual(prefixes, DEFAULT_PREFIXES_TAGS)
        mock_print.assert_called_once()
        self.assertIn("Warning: SNOMED OWL file not found", mock_print.call_args[0][0])

    @patch("src.comp_loinc.analysis.snomed_rf2_parser._get_expressions")
    def test_borrow_ontology_block_opener_empty_data_error(self, mock_get_expressions):
        """Test _borrow_ontology_block_opener_and_prefixes_from_snomed with empty data"""
        mock_get_expressions.side_effect = pd.errors.EmptyDataError("No data")

        with patch("builtins.print") as mock_print:
            ontology, prefixes = _borrow_ontology_block_opener_and_prefixes_from_snomed(
                "/fake/path"
            )

        self.assertEqual(ontology, DEFAULT_ONTOLOGY_BLOCK_OPENER)
        self.assertEqual(prefixes, DEFAULT_PREFIXES_TAGS)
        mock_print.assert_called_once()
        self.assertIn(
            "Warning: SNOMED OWL file at /fake/path is empty",
            mock_print.call_args[0][0],
        )


if __name__ == "__main__":
    unittest.main()
