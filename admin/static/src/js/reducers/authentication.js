export default function authentication(state, action) {
    state = state || {
            token: localstorage.getItem('auth.token'),
            isAuthenticated: false
    };
    switch (action.type) {
        case 'AUTHENTICATION_REQUEST':
            return Object.assign({}, state, {
            });
        case 'AUTHENTICATION_SUCCESS':
            return Object.assign({}, state, {
            });
        case 'AUTHENTICATION_FAILURE':
            return Object.assign({}, state, {
            });
        default:
            return state;
    }
}