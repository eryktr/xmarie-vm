from xmarievm import api


def test_run_no_debug():
    code = '''
    Load X
    Add Y
    ShiftL X
    Halt
    
    X, DEC 2
    Y, DEC 1
    '''

    snapshots = api.run(code, debug=False)

    assert len(snapshots) == 1
    assert snapshots[0].AC == 12


def test_run_debug():
    code = '''
    Load X
    Add Y
    Halt
    
    X, DEC 5
    Y, DEC 2
    '''

    snapshots = api.run(code, debug=True)

    assert len(snapshots) == 3
    assert snapshots[-1].AC == 7
