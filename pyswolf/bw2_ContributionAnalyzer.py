# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 16:46:10 2020

@author: msardar2
"""

# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division
from eight import *

from bw2data import Database, get_activity
import numpy as np


class ContributionAnalysis(object):
    def sort_array(self, data, limit=25, limit_type="number", total=None):
        """
Common sorting function for all ``top`` methods. Sorts by highest value first.

Operates in either ``number`` or ``percent`` mode. In ``number`` mode, return ``limit`` values. In ``percent`` mode, return all values >= (total * limit); where ``0 < limit <= 1``.

Returns 2-d numpy array of sorted values and row indices, e.g.:

.. code-block:: python

    ContributionAnalysis().sort_array((1., 3., 2.))

returns

.. code-block:: python

    (
        (3, 1),
        (2, 2),
        (1, 0)
    )

Args:
    * *data* (numpy array): A 1-d array of values to sort.
    * *limit* (number, default=25): Number of values to return, or percentage cutoff.
    * *limit_type* (str, default=``number``): Either ``number`` or ``percent``.
    * *total* (number, default=None): Optional specification of summed data total.

Returns:
    2-d numpy array of values and row indices.

        """
        total = total or np.abs(data).sum()
        if limit_type not in ("number", "percent"):
            raise ValueError("limit_type must be either 'percent' or 'index'.")
        if limit_type == "percent":
            if not 0 < limit <= 1:
                raise ValueError("Percentage limits > 0 and <= 1.")
            limit = (data >= (total * limit)).sum()

        results = np.hstack(
            (data.reshape((-1, 1)), np.arange(data.shape[0]).reshape((-1, 1)))
        )
        return results[np.argsort(np.abs(data))[::-1]][:limit, :]

    def top_matrix(self, matrix, rows=5, cols=5):
        """
Find most important (i.e. highest summed) rows and columns in a matrix, as well as the most corresponding non-zero individual elements in the top rows and columns.

Only returns matrix values which are in the top rows and columns. Element values are returned as a tuple: ``(row, col, row index in top rows, col index in top cols, value)``.

Example:

.. code-block:: python

    matrix = [
        [0, 0, 1, 0],
        [2, 0, 4, 0],
        [3, 0, 1, 1],
        [0, 7, 0, 1],
    ]

In this matrix, the row sums are ``(1, 6, 5, 8)``, and the columns sums are ``(5, 7, 6, 2)``. Therefore, the top rows are ``(3, 1)`` and the top columns are ``(1, 2)``. The result would therefore be:

.. code-block:: python

    (
        (
            (3, 1, 0, 0, 7),
            (3, 2, 0, 1, 1),
            (1, 2, 1, 1, 4)
        ),
        (3, 1),
        (1, 2)
    )

Args:
    * *matrix* (array or matrix): Any Python object that supports the ``.sum(axis=)`` syntax.
    * *rows* (int): Number of rows to select.
    * *cols* (int): Number of columns to select.

Returns:
    (elements, top rows, top columns)

"""
        top_rows = np.argsort(np.abs(np.array(matrix.sum(axis=1)).ravel()))[
            : -rows - 1 : -1
        ]
        top_cols = np.argsort(np.abs(np.array(matrix.sum(axis=0)).ravel()))[
            : -cols - 1 : -1
        ]
        elements = []
        for row, x in enumerate(top_rows):
            for col, y in enumerate(top_cols):
                if matrix[x, y] != 0:
                    elements.append((x, y, row, col, float(matrix[x, y])))
        return elements, top_rows.astype(int), top_cols.astype(int)

    def hinton_matrix(self, lca, rows=5, cols=5):
        coo, b, t = self.top_matrix(lca.characterized_inventory, rows=rows, cols=cols)
        coo = [row[2:] for row in coo]  # Don't need matrix indices
        ra, rp, rb = lca.reverse_dict()
        flows = [self.get_name(rb[x]) for x in b]
        activities = [self.get_name(ra[x]) for x in t]
        return {
            "results": coo,
            "total": lca.score,
            "xlabels": activities,
            "ylabels": flows,
        }

    def annotate(self, sorted_data, rev_mapping):
        """Reverse the mapping from database ids to array indices"""
        return [(row[0], rev_mapping[row[1]]) for row in sorted_data]

    def top_processes(self, matrix, **kwargs):
        """Return an array of [value, index] technosphere processes."""
        return self.sort_array(np.array(matrix.sum(axis=0)).ravel(), **kwargs)

    def top_emissions(self, matrix, **kwargs):
        """Return an array of [value, index] biosphere emissions."""
        return self.sort_array(np.array(matrix.sum(axis=1)).ravel(), **kwargs)

    def annotated_top_processes(self, lca, names=True, **kwargs):
        """Get list of most damaging processes in an LCA, sorted by ``abs(direct impact)``.

        Returns a list of tuples: ``(lca score, supply, activity)``. If ``names`` is False, they returns the process key as the last element.

        """
        ra, rp, rb = lca.reverse_dict()
        results = [
            (score, lca.supply_array[int(index)], ra[int(index)])
            for score, index in self.top_processes(
                lca.characterized_inventory, **kwargs
            )
        ]
        if names:
            results = [(x[0], x[1], get_activity(x[2])) for x in results]
        return results

    def annotated_top_emissions(self, lca, names=True, **kwargs):
        """Get list of most damaging biosphere flows in an LCA, sorted by ``abs(direct impact)``.

        Returns a list of tuples: ``(lca score, inventory amount, activity)``. If ``names`` is False, they returns the process key as the last element.

        """
        ra, rp, rb = lca.reverse_dict()
        results = [
            (score, lca.inventory[index, :].sum(), rb[index])
            for score, index in self.top_emissions(
                lca.characterized_inventory, **kwargs
            )
        ]
        if names:
            results = [(x[0], x[1], get_activity(x[2])) for x in results]
        return results

    def get_name(self, key):
        return get_activity(key).get("name", "Unknown")

    def d3_treemap(
        self, matrix, rev_bio, rev_techno, limit=0.025, limit_type="percent"
    ):
        """
Construct treemap input data structure for LCA result. Output like:

.. code-block:: python

    {
    "name": "LCA result",
    "children": [{
        "name": process 1,
        "children": [
            {"name": emission 1, "size": score},
            {"name": emission 2, "size": score},
            ],
        }]
    }

        """
        total = np.abs(matrix).sum()
        processes = self.top_processes(matrix, limit=limit, limit_type=limit_type)
        data = {"name": "LCA result", "children": [], "size": total}
        for dummy, tech_index in processes:
            name = self.get_name(rev_techno[tech_index])
            this_score = np.abs(matrix[:, int(tech_index)].toarray().ravel()).sum()
            children = []
            for score, bio_index in self.sort_array(
                matrix[:, int(tech_index)].toarray().ravel(),
                limit=limit,
                limit_type=limit_type,
                total=total,
            ):
                children.append(
                    {
                        "name": self.get_name(rev_bio[bio_index]),
                        "size": float(abs(matrix[int(bio_index), int(tech_index)])),
                    }
                )
            children_score = sum([x["size"] for x in children])
            if children_score < (0.95 * this_score):
                children.append({"name": "Others", "size": this_score - children_score})
            data["children"].append(
                {
                    "name": name,
                    "size": this_score,
                    # "children": children
                }
            )
        return data

    # def top_emissions_for_process(self, process, **kwargs):
    #     if hasattr(process, "id"):
    #         process = process.id
    #     if not hasattr(self.dicts, 'reverse'):
    #         self.construct_reverse_dicts()
    #     return self._top(array(self.weighted_biosphere[:,process].todense(
    #         )).ravel(), self.dicts.reverse.biosphere, **kwargs)

    # def top_processes_for_emission(self, biosphere_flow, **kwargs):
    #     if hasattr(biosphere_flow, "id"):
    #         biosphere_flow = biosphere_flow.id
    #     if not hasattr(self.dicts, 'reverse'):
    #         self.construct_reverse_dicts()
    #     return self._top(array(self.weighted_biosphere[biosphere_flow,:
    #         ].todense()).ravel(), self.dicts.reverse.technosphere, **kwargs)

    # def top_processes_for_emission_inventory(self, emission, **kwargs):
    #     """Get the most important inventory processes for an emission"""
    #     if hasattr(emission, "id"):
    #         emission = emission.id
    #     if not hasattr(self.dicts, 'reverse'):
    #         self.construct_reverse_dicts()
    #     return self._top(array(self.calculated_biosphere[emission,:].todense(
    #         )).ravel(), self.dicts.reverse.technosphere, **kwargs)