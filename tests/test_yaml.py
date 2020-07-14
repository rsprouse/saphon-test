#!/usr/bin/env python

import pytest
import os, glob
import yaml

def docs_by_doctype(docs):
    '''Return synthesis and ref docs separately.'''
    synth = None
    refs = []
    for doc in docs:
        try:
            assert(doc['doctype'] in ('synthesis', 'ref'))
        except AssertionError:
            raise AssertionError(f"Unrecognized doctype \'{doc['doctype']}\'")
        if doc['doctype'] == 'synthesis':
            try:
                assert(synth is None)
            except AssertionError:
                raise AssertionError('Multiple synthesis documents found')
            synth = doc
        elif doc['doctype'] == 'ref':
            refs.append(doc)
    return (synth, refs)

def check_docs(docs):
    '''Check docs read from a yaml file for correctness and completeness.'''
    synth, refs = docs_by_doctype(docs)
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
    try:
        assert(errors == '')
    except AssertionError:
        print(errors)
        raise AssertionError(errors)
