#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2024 Harm Brouwer <me@hbrouwer.eu>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#import janus as js
import janus_swi as js
import numpy as np
import re

# ---- Last modified: October 2024, Harm Brouwer ----

def dfs_load_world(filename):
    """Load DFS world specification

    Args:
        filename (:obj:`str`):
            world specification

    """
    js.consult(filename, data=None, module='user')

                ########################
                #### model sampling ####
                ########################

"""<module> Model sampling [dfs_sample_models.pl]

Sample models from a world specification.

"""

def dfs_sample_model():
    """dfs_sample_model(-Model) is det.

    Sample a model from the world specificiations.

    ---

    Returns:
        (:obj:`str`):
            formal model structure
    """
    q = js.query_once(
            """
            dfs_sample_model(_Model),
            term_string(model(_Model),Model).
            """)
    return q["Model"]

def dfs_sample_models(num_models):
    """dfs_sample_models(+NumModels,-ModelSet) is det.
        
    ModelSet is a set of NumModels sampled models.

    @see dfs_sample_model.

    ---

    Args:
        num_models (:obj:`int`):
            number of models to be sampled

    Returns:
        (:obj:`list` of :obj:`str`): 
            formal model structures
    """
    q = js.query_once(
            """
            dfs_sample_models(_NumModels,_Models),
            findall(
                model(_Model),
                member(_Model,_Models),
                _WrappedModels),
            term_string(_WrappedModels,Models).
            """,
            {"_NumModels": num_models})
    return re.findall("(model\(\(\[.*?\],\[.*?\]\)\))", q["Models"])

def dfs_sample_models_mt(num_threads, num_models):
    """dfs_sample_models_mt(+NumThreads,+NumModels,-ModelSet) is det.

    ModelSet is a set of NumModels sampled models.
       
    @see dfs_sample_model.

    ---

    Args:
        num_threads (:obj:`int`):
            number of parallel sampling threads
        num_models (:obj:`int`):
            number of models to be sampled per thread

    Returns:
        (:obj:`list` of :obj:`str`): 
            formal model structures
    """
    q = js.query_once(
            """
            dfs_sample_models_mt(_NumThreads,_NumModels,_Models),
            findall(
                model(_Model),
                member(_Model,_Models),
                _WrappedModels),
            term_string(_WrappedModels,Models).
            """,
            {"_NumThreads": num_threads,
             "_NumModels": num_models})
    return re.findall("(model\(\(\[.*?\],\[.*?\]\)\))", q["Models"])

                ######################
                #### vector space ####
                ######################

"""<module> Vector space [dfs_vector_space.pl]

Conversion between sets of models and vector space.

"""

def dfs_model_to_vector(model):
    """dfs_model_to_vector(+Model,-ModelVector) is det.

    ModelVector is a set of tuples (AtomicProp,State) representing
    the State of each atomic proposition AtomicProp in Model.

    ---

    Args:
        model (:obj:`str`):
            formal model structure

    Returns:
        (:obj:`str`):
            tuples of atomic propositions and their states in the model

    """
    q = js.query_once(
            """
            read_term_from_atom(_ModelAtom,_ModelTerm,[]),
            _ModelTerm =.. [model|[_Model]],
            dfs_model_to_vector(_Model,_Vector),
            term_string(_Vector,Vector).
            """,
            {"_ModelAtom": model})
    return q["Vector"] 

def dfs_models_to_matrix(models):
    """dfs_models_to_matrix(+ModelSet,-ModelMatrix) is det.

    Convert a set of models into a vector space.

    @see dfs_model_to_vector/2.

    ---

    Args:
        models (:obj:`list` of :obj:`str`): 
            formal model structures

    Returns:
        (:obj:`list` of :obj:`str`):
            tuples of atomic propositions and their states in each model

    """
    q = js.query_once(
            """
            read_term_from_atom(_ModelsAtom,_ModelsTerm,[]),
            findall(
                _Model,
                member(model(_Model),_ModelsTerm),
                _Models),
            dfs_models_to_matrix(_Models,_Matrix),
            term_string(_Matrix,Matrix).
            """,
            {"_ModelsAtom": "[" + (','.join(models)) + "]"})
    return re.findall("(\[.*?\])",q["Matrix"][1:-1])

def dfs_vector_to_model(vector):
    """dfs_vector_to_model(+ModelVector,-Model) is det.

    Converts ModelVector, a set of tuples (AtomicProp,State) representing
    the State of each atomic proposition AtomicProp, into a Model.

    ---

    Args:
        vector (:obj:`str`):
            tuples of atomic propositions and their states in the model

    Returns:
        (:obj:`str`):
            formal model structure

    """
    q = js.query_once(
            """
            read_term_from_atom(_VectorAtom,_VectorTerm,[]),
            dfs_vector_to_model(_VectorTerm,_Model),
            term_string(_Model,Model).
            """,
            {"_VectorAtom": vector})
    return "model((" + q["Model"] + "))"

def dfs_matrix_to_models(matrix):
    """dfs_matrix_to_models(+ModelMatrix,-ModelSet) is det.

    Convert a vector space into a set of models.

    @see dfs_vector_to_model/2.

    ---

    Args:
        matrix (:obj:`list` of :obj:`str`):
            tuples of atomic propositions and their states in each model

    Returns:
        (:obj:`list` of :obj:`str`): 
            formal model structures

    """
    ms = []
    for v in matrix:
        ms.extend([dfs_vector_to_model(v)])
    return ms

### split this over two functions ...
def dfs_vector_from_models(formula, models):
    """dfs_vector(+Formula,+ModelSet,-Vector) is det.

    A formula P is true in a model M iff [[P]]^M,g = 1 given an arbitrary
    variable assignment g.

    ---

    Args:
        formula (:obj:`string`):
            a first-order logic formula
        models (:obj:`list` of :obj:`str`): 
            formal model structures

    Returns:
        (:obj:`ndarray`):
            vector for formula

    """
    q = js.query_once(
            """
            read_term_from_atom(_FormulaAtom,_FormulaTerm,[]),
            read_term_from_atom(_ModelsAtom, _ModelsTerm, []),
            findall(
                _Model,
                member(model(_Model),_ModelsTerm),
                _Models),
            dfs_vector(_FormulaTerm,_Models,_Vector),
            term_string(_Vector,Vector).
            """,
            {"_FormulaAtom": formula,
             "_ModelsAtom": "[" + (','.join(models)) + "]"})
    return np.fromstring(q["Vector"][1:-1], dtype = int, sep = ",")

def dfs_vector_from_matrix(formula, matrix):
    """dfs_vector(+Formula,+ModelMatrix,-Vector) is det.

    A formula P is true in a model M iff [[P]]^M,g = 1 given an arbitrary
    variable assignment g.

    ---

    Args:
        formula (:obj:`string`):
            a first-order logic formula
        matrix (:obj:`list` of :obj:`str`):
            tuples of atomic propositions and their states in each model

    Returns:
        (:obj:`ndarray`):
            vector for formula

    """
    models = dfs_matrix_to_models(matrix)
    return dfs_vector_from_models(formula, models)

def dfs_atomic_propositions(models):
    """atomic_propositions(+ModelSet,-AtomicProps) is det.

    AtomicProps is the list of all atomic propositions in ModelSet.

    ---

    Args:
        models (:obj:`list` of :obj:`str`): 
            formal model structures

    Returns:
       (:obj:`list` of :obj:`str`): 
            atomic propositions
    """
    q = js.query_once(
            """
            read_term_from_atom(_ModelsAtom, _ModelsTerm, []),
            findall(
                _Model,
                member(model(_Model),_ModelsTerm),
                _Models),
            dfs_vector_space:atomic_propositions(_Models,_AtomicPropositions),
            term_string(_AtomicPropositions,AtomicPropositions).        
            """,
            {"_ModelsAtom": "[" + (','.join(models)) + "]"})
    return re.findall("(\w*?\(.*?\))", q["AtomicPropositions"][1:-1])

def dfs_models_to_numpy(models):
    """Convert models to a vector space

    Args:
        models (:obj:`list` of :obj:`str`): 
            formal model structures

    Returns:
        models (:obj:`dict`)
            tuples of atomic proposition and their corresponding vector
    """
    model_space = dict()
    atoms = dfs_atomic_propositions(models)
    for atom in atoms:
        model_space[atom] = dfs_vector_from_models(atom, models)
    return model_space

                ###################
                #### sentences ####
                ###################

"""<module> Sentence generation

Generation of sentence-semantics (and vice versa) mappings.

"""

def dfs_sentences():
    """dfs_sentences(-SenSemTuples) is det.

    SenSemTuples is a list of all sentence-semantics mappings generated.

    ---

    Returns:
        mappings (:obj:`list` of :obj:`tuple` of :obj:`str`)
            tuples of sentence-semantics mappings

    """
    q = js.query_once(
            """
            findall(
                mapping(_Sen,[_Sem]),
                sentence((_Sen,_Sem)),
                _SPMs),
            term_string(_SPMs,SPMs).
            """)
    return re.findall("mapping\((\[.*?\]),\[(.*?)\]\)", q["SPMs"])

def dfs_mappings_to_vectors(mappings, models):
    """Compute vectors for sentence-semantics mappings

    Returns:
        mappings (:obj:`list` of :obj:`tuple` of :obj:`str`/`ndarray`)
            tuples of sentence-semantics-vector mappings

    """
    vector_mappings = []
    for sentence, semantics in mappings:
        vector = dfs_vector_from_models(semantics, models)
        vector_mappings.extend([(sentence, semantics, vector)])
    return vector_mappings
