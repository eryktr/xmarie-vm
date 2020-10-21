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
