def diff_states(fs_state, db_state):
    new = fs_state.keys() - db_state.keys()
    deleted = db_state.keys() - fs_state.keys()
    existing = fs_state.keys() & db_state.keys()
    return new, deleted, existing
