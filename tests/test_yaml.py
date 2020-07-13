#!/usr/bin/env python

import pytest
import os, glob
import yaml

def docs_by_doctype(docs):
    '''Return synthesis and ref docs separately.'''
    synth = None
    refs = []
    for doc in docs:
        if doc['doctype'] == 'synthesis':
            assert(synth is None)
            synth = doc
        elif doc['doctype'] == 'ref':
            refs.append(doc)
        else:
            raise f"Unrecognized doctype {doc['doctype']}"
    return (synth, refs)

def check_docs(docs):
    '''Check docs read from a yaml file for correctness and completeness.'''
    try:
        synth, refs = docs_by_doctype(docs)
    except AssertionError:
        raise AssertionError('Multiple synthesis documents found.')
    assert(synth is not None)
    assert(refs != [])

def test_read_yaml():
    errors = ''
    for fname in glob.glob('data/*.yaml'):
        with open(fname, 'r') as fh:
            docs = list(yaml.safe_load_all(fh))
            try:
                check_docs(docs)
            except Exception as e:
                errors += f'Error in {fname}: {e}\n'
    if errors != '':
        raise Exception(errors)
