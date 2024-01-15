Selecting a Randomness Extractor
================================
In general, the choice of randomness extractor depends on the scenario in which it is to be used and it is not always clear which extractor is best suited to a given scenario. 
In this section, we (informally) help solve this problem, based on the section 'Overview of Extractor Library' from Cryptomite's accompanying paper (see :ref:`For2024`).
We use the notation :math:`n_1, n_2` to denote the length and :math:`k_1, k_2` to denote the :term:`min-entropy` of any first or second input string respectively. 
Additionally, :math:`m` denotes the length of an output string, :math:`\epsilon` the extractor error and :math:`O(.)` denotes asymptotic quantities.

.. image:: figures/extractor_flow_chart.png
   :width: 600

Note: there may be a small gain to be made by analysing the extractors individually if sufficiently motivated, but this flow-chart gives a good, general, approach to follow.
The individual extractor parameters are given in the following table:

.. image:: figures/Table.png
   :width: 600

