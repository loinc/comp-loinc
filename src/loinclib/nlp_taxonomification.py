"""All things dealing with taxonomies based on NLP approaches."""
import os
import typing as t
from pathlib import Path

import pandas as pd

from comp_loinc.groups.property_use import Part


# todo: ideally not hard code. Best to solve via OO, i'm not sure
inpath = os.getcwd() / Path('output/analysis/dangling/dangling.tsv')


# Inputs --------------------------------------------------------------------------------------------------------------
def parts_to_tsv(parts: t.List[Part], outpath: Path):
    """Save list of Part objects to TSV.

    todo: Consider handling dupe labels within this func
    """
    outdir = Path(os.path.dirname(outpath))
    if not outdir.exists():
        outdir.mkdir(parents=True)
    df = pd.DataFrame([{
        'id': p.part_number,
        'display': p.part_display,
        'type': p.part_type,
        'is_search': p.is_search,
    } for p in parts])
    df.to_csv(outpath, sep='\t', index=False)


# Semantic clusterign --------------------------------------------------------------------------------------------------
# TODO: these seem to be based on semantic clustering method
# todo: I think that the deduping should be decoupled from clustring
# todo: install packages
# todo: write a 'main' for this to connect these together
def process_large_loinc_dataset(csv_path):
    """
    Process large LOINC dataset with duplicates
    """
    from collections import Counter
    import numpy as np
    from sentence_transformers import SentenceTransformer
    from sklearn.cluster import MiniBatchKMeans
    from sklearn.preprocessing import normalize

    # Load and preprocess
    df = pd.read_csv(csv_path)

    # Get display terms and their frequencies
    term_counts = Counter(df['display'])
    unique_terms = list(term_counts.keys())

    # Step 1: Initial frequency analysis
    print(f"Total unique terms: {len(unique_terms)}")
    print(f"Most common terms (top 10):")
    for term, count in term_counts.most_common(10):
        print(f"  {term}: {count}")

    # Step 2: Generate embeddings (memory-efficient batch processing)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    batch_size = 1000
    embeddings = []

    for i in range(0, len(unique_terms), batch_size):
        batch = unique_terms[i:i + batch_size]
        batch_embeddings = model.encode(batch)
        embeddings.append(batch_embeddings)

    embeddings = np.vstack(embeddings)
    embeddings = normalize(embeddings)

    return unique_terms, embeddings, term_counts


def create_hierarchical_clusters(unique_terms, embeddings, term_counts):
    """
    Create hierarchical clusters using a multi-level approach
    """
    from sklearn.cluster import MiniBatchKMeans
    from collections import defaultdict

    # Use different granularities of clustering
    n_clusters_levels = [100, 500, 2000]  # Adjustable based on data
    hierarchy = defaultdict(dict)

    for level, n_clusters in enumerate(n_clusters_levels):
        kmeans = MiniBatchKMeans(n_clusters=n_clusters,
                                 batch_size=1000,
                                 random_state=42)
        clusters = kmeans.fit_predict(embeddings)

        # Store cluster assignments
        hierarchy[f'level_{level}'] = {
            'clusters': clusters,
            'centroids': kmeans.cluster_centers_
        }

    return hierarchy


def analyze_patterns_in_clusters(unique_terms, hierarchy, term_counts):
    """
    Analyze patterns within clusters to establish relationships
    """
    import re
    from collections import defaultdict

    patterns = {
        'of': r'(.*) of (.*)',
        'with': r'(.*) with (.*)',
        'in': r'(.*) in (.*)',
        'by': r'(.*) by (.*)',
        # Add more medical-specific patterns
        'type': r'(.*) type(.*)',
        'grade': r'(.*) grade(.*)',
        'stage': r'(.*) stage(.*)',
    }

    cluster_patterns = defaultdict(lambda: defaultdict(list))

    # Analyze patterns within each cluster
    for level in hierarchy:
        clusters = hierarchy[level]['clusters']
        for term_idx, cluster_id in enumerate(clusters):
            term = unique_terms[term_idx]
            count = term_counts[term]

            # Check for patterns
            for pattern_name, pattern in patterns.items():
                if re.match(pattern, term, re.IGNORECASE):
                    cluster_patterns[level][cluster_id].append({
                        'term': term,
                        'pattern': pattern_name,
                        'frequency': count
                    })

    return cluster_patterns


def extract_hierarchical_relationships(cluster_patterns, hierarchy):
    """
    Extract hierarchical relationships based on patterns and clustering
    """
    relationships = []

    # Extract relationships within clusters
    for level in cluster_patterns:
        for cluster_id, patterns in cluster_patterns[level].items():
            # Sort terms by frequency within cluster
            patterns.sort(key=lambda x: x['frequency'], reverse=True)

            # If we have multiple terms with patterns in the same cluster
            if len(patterns) > 1:
                # Use the most frequent term as potential parent
                parent = patterns[0]['term']
                for child in patterns[1:]:
                    relationships.append({
                        'parent': parent,
                        'child': child['term'],
                        'relationship_type': child['pattern'],
                        'confidence': 'high' if child['pattern'] in ['of', 'type'] else 'medium',
                        'cluster_level': level,
                        'cluster_id': cluster_id
                    })

    return relationships


def create_visualizations(unique_terms, embeddings, relationships=None):
    """
    Create both t-SNE visualization for clusters and hierarchical visualization
    """
    import numpy as np
    from sklearn.manifold import TSNE
    import plotly.express as px
    import plotly.graph_objects as go
    import networkx as nx

    # t-SNE visualization
    tsne = TSNE(n_components=2, random_state=42, perplexity=30)
    embeddings_2d = tsne.fit_transform(embeddings)

    # Create interactive scatter plot with plotly
    fig_tsne = px.scatter(
        x=embeddings_2d[:, 0],
        y=embeddings_2d[:, 1],
        text=unique_terms,
        title='t-SNE visualization of LOINC terms'
    )
    fig_tsne.update_traces(
        textposition='top center',
        hovertemplate='<b>%{text}</b><extra></extra>'
    )

    # If we have hierarchical relationships, create a separate network graph
    if relationships:
        g = nx.DiGraph()
        for rel in relationships:
            g.add_edge(rel['parent'], rel['child'])

        # Create network layout
        pos = nx.spring_layout(g)

        # Create network visualization
        edge_trace = go.Scatter(
            x=[], y=[],
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')

        node_trace = go.Scatter(
            x=[], y=[],
            mode='markers+text',
            hoverinfo='text',
            text=list(g.nodes()),
            textposition="top center"
        )

        # Add positions to traces
        for edge in g.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_trace['x'] += (x0, x1, None)
            edge_trace['y'] += (y0, y1, None)

        for node in g.nodes():
            x, y = pos[node]
            node_trace['x'] += (x,)
            node_trace['y'] += (y,)

        fig_hierarchy = go.Figure(data=[edge_trace, node_trace],
                                  layout=go.Layout(
                                      title='Hierarchical Relationships',
                                      showlegend=False,
                                      hovermode='closest'
                                  ))

        return fig_tsne, fig_hierarchy

    return fig_tsne


# Lexical approaches ---------------------------------------------------------------------------------------------------
def create_term_hierarchy(terms):
    """
    First approach using text similarity and substring relationships
    to establish potential hierarchical connections
    """
    # todo: data types?
    import spacy
    from itertools import combinations

    # Load SpaCy model for better text processing
    # TODO: OSError: [E050] Can't find model 'en_core_web_md'. It doesn't seem to be a Python package or a valid path
    #  to a data directory.
    nlp = spacy.load('en_core_web_md')

    # Structure to store relationships
    relationships = []

    # Get all pairs of terms
    term_pairs = list(combinations(terms, 2))

    for term1, term2 in term_pairs:
        # Check for substring relationships
        if term1.lower() in term2.lower():
            relationships.append((term1, term2, 'potential_parent'))
        elif term2.lower() in term1.lower():
            relationships.append((term2, term1, 'potential_parent'))
        else:
            # Calculate semantic similarity
            doc1 = nlp(term1)
            doc2 = nlp(term2)
            similarity = doc1.similarity(doc2)

            if similarity > 0.8:  # Threshold can be adjusted
                relationships.append((term1, term2, 'related'))

    return relationships


def extract_patterns(terms):
    """
    Look for common patterns in terminology that might
    indicate hierarchical relationships
    """
    import re

    patterns = {
        'of': r'(.*) of (.*)',
        'with': r'(.*) with (.*)',
        'in': r'(.*) in (.*)',
        'by': r'(.*) by (.*)'
    }

    term_patterns = {}
    for term in terms:
        matches = []
        for pattern_name, pattern in patterns.items():
            if re.match(pattern, term, re.IGNORECASE):
                matches.append(pattern_name)
        term_patterns[term] = matches

    return term_patterns


def main():
    """Run everything here. Assumes inputs already present."""
    df_in = pd.read_csv(inpath, sep='\t')
    # todo: dedupe?
    # todo: data type?
    hierarchy = create_term_hierarchy(df_in['display'].tolist())
    print()


if __name__ == '__main__':
    main()
