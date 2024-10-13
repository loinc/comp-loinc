"""Tests

Running: python -m unittest discover

In addition to explicit assertions, will also effectively test (via errors) that:
- SPARQL queries return at least some results

todo: consider deleting SPARQL results in output/ after reading into df, as failsafe for accidental cache reads
todo: ideally would test max depth & depth counts, but very slow (at least >5min; dk how long)
todo: loinc-part-hierarchy-all.owl: if becomes non-flat later, could be good to add tests using child-counts.sparql and
 top-branches.sparql
todo: add rdfs:label to more queries? (mainly for debugging / interrogation)
"""
import unittest
from typing import Dict, Set

import pandas as pd

try:
    # noinspection PyUnresolvedReferences pycharm_confused_by_test_root
    from test.config import PROJECT_DIR, TEST_IN_DIR, TEST_OUT_DIR, TEST_SPARQL_QEURY_DIR
    # noinspection PyUnresolvedReferences pycharm_confused_by_test_root
    from test.utils import sparql_ask, sparql_select
except ModuleNotFoundError:
    from config import PROJECT_DIR, TEST_IN_DIR, TEST_OUT_DIR, TEST_SPARQL_QEURY_DIR
    from utils import sparql_ask, sparql_select


class CompLoincTest(unittest.TestCase):
    """CompLOINC tests"""

    def all(self):
        """Wrapper for running all at once. Used for debugging."""
        self.test_terms_list()
        self.test_part_list()
        self.test_part_hierarchy()
        self.test_term_primary_model()
        self.test_term_supplementary_model()
        self.test_snomed_part_mappings()
        self.test_loinc_snomed_ontology_equivalence()

    @staticmethod
    def _part_model_unique_prop_counts(df: pd.DataFrame) -> Set[int]:
        """Get property counts"""
        prop_counts: Dict[str, int] = df.groupby('class').size().to_dict()
        return set(prop_counts.values())
    
    def _test_n_classes(self, onto_filename: str, n=50) -> pd.DataFrame:
        """Test that n classes are present"""
        df: pd.DataFrame = sparql_select(onto_filename, 'all-classes.sparql')
        self.assertGreater(len(df), n)
        return df

    def _test_no_nulls(self, df: pd.DataFrame):
        """Ensure no NULLs in DataFrame"""
        self.assertFalse(bool(df.isna().any().any()))

    def _tests_common(self, onto_filename: str):
        """Common tests to run on all artefacts"""
        df: pd.DataFrame = self._test_n_classes(onto_filename)
        self._test_no_nulls(df)

    def _test_child_counts(self, onto_filename: str, n=10) -> pd.DataFrame:
        """Test variation in child counts

        :param n: How many children to expect. Default=10 (arbitrary)
        """
        df: pd.DataFrame = sparql_select(onto_filename, 'child-counts.sparql')
        self.assertGreaterEqual(len(set(df['directSubclassCount'])), n)
        return df

    def test_terms_list(self):
        """Tests for term list

        todo: test non-empty / certain vals: rdfs:label, loinc_class, loinc_class_type, loinc_number, long_common_name
        """
        onto_filename = 'loinc-terms-list-all.owl'
        self._tests_common(onto_filename)

        # Test that expected class is at top of hierarchy
        root_confirmed = not sparql_ask(onto_filename, 'terms-root-check.sparql')
        self.assertTrue(root_confirmed)

        # Test for expected top level branches
        df: pd.DataFrame = sparql_select(onto_filename, 'terms-tree-top-branches.sparql')
        branch_names = set([x.replace('https://loinc.org/LTC___', '').lower() for x in df['subclass']])
        self.assertSetEqual(branch_names, {'surveys', 'laboratory', 'clinical', 'claims_attachments'})

        # Test that all top level branches have (arbitrary number of) descendants
        df2: pd.DataFrame = sparql_select(onto_filename, 'terms-tree-top-branch-descendants.sparql')
        branch_desc_counts: Dict[str, int] = df2.groupby('branch').size().to_dict()
        for v in branch_desc_counts.values():
            self.assertGreater(v, 5)

        # Test variation in child counts
        self._test_child_counts(onto_filename)

    def test_part_list(self):
        """Tests for part list

        todo: test non-empty / certain vals: rdfs:label, part-type-name, part_display_name, part_name, part_number
        """
        onto_filename = 'loinc-part-list-all.owl'
        self._tests_common(onto_filename)

    def test_part_hierarchy(self):
        """Tests for the part hierarchy"""
        onto_filename = 'loinc-part-hierarchy-all.owl'
        self._tests_common(onto_filename)

        # Test that expected class is at top of hierarchy
        root_confirmed = not sparql_ask(onto_filename, 'parts-root-check.sparql')
        self.assertTrue(root_confirmed)

    def test_term_primary_model(self):
        """Tests for terms using the primary part model

        todo: In cases where n props is 5 and not 6, check to ensure missing prop is as expected? If is always same
        todo: Consider test for rad- and document- model props
        todo: If rename to TIME_ASPECT was unintentional and we undo, update here.
        """
        onto_filename = 'loinc-term-primary-def.owl'
        core_props = {
            'http://loinc.org/property/COMPONENT',
            'http://loinc.org/property/PROPERTY',
            'http://loinc.org/property/SYSTEM',
            'http://loinc.org/property/SCALE_TYP',
            'http://loinc.org/property/METHOD_TYP',
            # TIME_ASP(E)CT: 2024/10 w/out 'E' is how it is spelled in release. But we rename it.
            'http://loinc.org/property/TIME_ASPCT',
            'http://loinc.org/property/TIME_ASPECT',
        }
        self._tests_common(onto_filename)

        # Test that all classes have equivalence properties
        df: pd.DataFrame = sparql_select(onto_filename, 'all-existential-equivalences.sparql')
        self._test_no_nulls(df)  # check all classes have equivalence properties

        # Test for correct number of props (basic LOINC model)
        df = df[df['onProperty'].isin(core_props)]  # filter out rad- and document- model props
        unique_n_props: Set[int] = self._part_model_unique_prop_counts(df)
        self.assertEqual(unique_n_props, {5, 6})

    def test_term_supplementary_model(self):
        """Tests for terms using the supplementary part model

        FYI: Supplementary model has greater variation in the number of patterns (specific combos of props). It also
        is only defined on the core LOINC model (i.e. doesn't define rad- or document- models).

        todo: Test specific patterns (combos of props)? (more relevant after OBA / DOSDP)
        """
        onto_filename = 'loinc-term-supplementary-def.owl'
        self._tests_common(onto_filename)

        # Test for expected range in number of equivlance properties
        df: pd.DataFrame = sparql_select(onto_filename, 'all-existential-equivalences.sparql')
        unique_n_props: Set[int] = self._part_model_unique_prop_counts(df)
        self.assertGreaterEqual(min(unique_n_props), 5)
        self.assertLessEqual(min(unique_n_props), 13)

        # Test all classes have equivalence properties
        self._test_no_nulls(df)

    def test_snomed_part_mappings(self):
        """Tests for SNOMED part mappings"""
        onto_filename = 'snomed-parts.owl'
        main_branch = 'https://loinc.org/138875005'  # SCT   SNOMED CT Concept (SNOMED RT+CTV3)
        self._tests_common(onto_filename)
        df: pd.DataFrame = sparql_select(onto_filename, 'top-branches.sparql')

        # Test for a number of top level branches
        self.assertGreaterEqual(len(df), 5)  # n=arbitrary

        # Test main branch exists
        self.assertIn(main_branch, df['class'].values)

        # Test variation in child counts
        df2: pd.DataFrame = self._test_child_counts(onto_filename)

        # Test main branch has several children
        main_branch_children: int = list(df2[df2['class'] == main_branch]['directSubclassCount'])[0]
        self.assertGreaterEqual(main_branch_children, 5)  # n=arbitrary

    def test_loinc_snomed_ontology_equivalence(self):
        """Tests for equivalence between CompLOINC and LOINC(-SNOMED) Ontology"""
        onto_filename = 'loinc-snomed-equiv.owl'
        self._tests_common(onto_filename)

        # Test all classes have equivalence properties
        df: pd.DataFrame = sparql_select(onto_filename, 'all-class-equivalences.sparql')
        df = df[df['class'].str.startswith('https://loinc.org/LP')]  # filter because equiv only declared on LOINC parts
        self._test_no_nulls(df)


# Debugging / development
DEBUG = False
if DEBUG:
    CompLoincTest().all()
