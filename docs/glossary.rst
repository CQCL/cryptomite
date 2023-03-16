Glossary
========

.. glossary::

    min-entropy
        The min-entropy, :math:`k`, of a random variable, :math:`X \in \{ 0,1\}^n`, is defined as 

        .. math::
            k = H_{\infty}(X) = -\log _{ \max x \in \{ 0,1\}^n} \Pr (X = x | \lambda)

        where  :math:`\lambda` is any additional side information a physical observer may have.
        This can be interpreted as the minimum amount of random bits a random variable :math:`X` has, conditioned on the side information :math:`\lambda`.

    block min-entropy
        A set of random variables :math:`X_i`` for :math:`i \in \mathbb{Z}` is said to have block min entropy :math:`k`, if 
    
        .. math::
           k = H_{\infty}(X_i) = -\log _{ \max x \in \{ 0,1\}^n} \Pr (X_i = x | X_0, X_1, ..., X_{i-1}, \lambda)

        for all :math:`i`, where :math:`\lambda` is any additional side information a physical observer may have. 
        This can be interpreted as the minimum amount of random bits a random variable :math:`X_i` has, even when conditioned on all previous random variables in the set and side information :math:`\lambda`.

    statistical distance
        The statistical distance, :math:`\Delta`, between two random variables, :math:`X` and :math:`Z` :math:`\in \{0,1\}^n` is defined as
    
        .. math::
            \Delta(X,Z) = \frac{1}{2} \sum_{v \in \{ 0,1 \}^n} | \Pr(X=v | \lambda) - \Pr(Z=v | \lambda)|

        where :math:`\lambda` is any additional side information a physical observer may have. 
        This is a measure of how close, or indistinguishable, two distributions are to one another.

    perfect randomness
        A distribution :math:`X` on :math:`\{0,1\}^n` is said to be perfectly random, if, 

        .. math::
            \Delta(X, U_n) = 0

        where :math:`U_n` is the uniform variable on :math:`\{0,1\}^n`.
        This definition is equivalent to saying that the variable :math:`X` is completely indistinguishable from the uniform distribution to a physical observer.
        Note: This is a composable definition, any random variable :math:`X` satisfying this definition can be safely used in practical applications. 

    near-perfect randomness
        A random variable :math:`X`` on :math:`\{0,1\}^n` is said to be near-perfectly random, if, 

        .. math::
            \Delta(X, U_n) \leq \epsilon

        where :math:`U_n` is the uniform variable on :math:`\{0,1\}^n`. 
        This definition is equivalent to saying that the variable :math:`X` is :math:`\epsilon` close to indistinguishable from the uniform distribution to a physical observer.
        Note: This is a composable definition, any random variable :math:`X` satisfying this definition can be safely used in practical applications. 

    deterministic randomness extractor
        A :math:`(k, \epsilon, n, m)`-deterministic randomness extractor is a function

        .. math::
            \mathrm{Ext}_d: \{ 0,1\}^n \rightarrow \{0,1\}^m

        such that, for every random variable :math:`X` on :math:`\{ 0,1\}^n` with min-entropy :math:`H_{\infty}(X) \geq k`, then, 

        .. math::
            \Delta(\mathrm{Ext}_d(X), U_m) \leq \epsilon

        where :math:`U_m` is the uniform variable on :math:`\{0,1\}^m`.
        In words, a deterministic extractor is a deterministic function that maps a random variable :math:`X` to a new variable :math:`\mathrm{Ext}_d(X)` that is near-perfect, as defined in :term:`near-perfect randomness`.

    seeded randomness extractor
        A :math:`(k, \epsilon, n, d, m)`-seeded randomness extractor is a function 

        .. math::
            \mathrm{Ext}_s: \{ 0,1\}^{n} \times \{0,1\}^{d} \rightarrow \{0,1\}^m

        such that, for every random variable :math:`X` on :math:`\{ 0,1\}^{n}` with min-entropy :math:`H_{\infty}(X) \geq k`, and every :math:`S` on :math:`\{ 0,1\}^d` with min-entropy :math:`H_{\infty}(Y) =  d` then, 

        .. math::
            \Delta(\mathrm{Ext}_s(X, S), U_m) \leq \epsilon

        where :math:`U_m` is the uniform distribution on :math:`\{0,1\}^m`. 
        In words, a seeded extractor is a randomized function that maps a random variable :math:`X` to a new variable :math:`\mathrm{Ext}_s(X, S)` that is near-perfect, as defined in :term:`near-perfect randomness`.

    2-source randomness extractor
        A :math:`(k_1, k_2, \epsilon, n_1, n_2, m)`-2-weak-source randomness extractor is a function 
    
        .. math::
            \mathrm{Ext}_2: \{ 0,1\}^{n_1} \times \{0,1\}^{n_2} \rightarrow \{0,1\}^m

        such that, for every independent random variable :math:`X` on :math:`\{ 0,1\}^{n_1}` with min-entropy :math:`H_{\infty}(X) \geq k_1`, and :math:`Y` on :math:`\{ 0,1\}^{n_2}` with min-entropy :math:`H_{\infty}(Y) \geq k_2` then,

        .. math::
            \Delta(\mathrm{Ext}_2(X, Y), U_m) \leq \epsilon

        where :math:`U_m` is the uniform variable on :math:`\{0,1\}^m`. 
        In words, a 2-weak-source extractor is a weakly randomized function that maps a random variable :math:`X` to a new variable :math:`\mathrm{Ext}_2(X, Y)` that is near-perfect, as defined in :term:`near-perfect randomness`. 

    strong seeded extractor
        A strong seeded randomness extractor is any :math:`\mathrm{Ext}_s` s.t. 

        .. math::
            \Delta( (\mathbf{Ext}_s(X, S), S), (U_m, S) ) \leq \epsilon

        where :math:`U_m` is the uniform variable on :math:`\{0,1\}^m`. 
        Note, we use bold font to denote strong extractors.
        In words, a strong seeded extractor is a randomized function that maps a random variable :math:`X` to a new variable :math:`\mathbf{Ext}_s(X, S)` that is near-perfect, as defined in :term:`near-perfect randomness` and where :math:`\mathrm{Ext}_s(X, S)` is (near-) independent of :math:`X`.

        Intuitively, this has 3 main implications: 

        #. The seed :math:`S` can be made public without compromising the uniformity of the extractor output.
        #. The seed :math:`S` can be concatenated with the output :math:`\mathbf{Ext_s}(X,S)` to get a longer, (near-)perfect output. 
        #. The seed :math:`S` can be re-used with different input sources.