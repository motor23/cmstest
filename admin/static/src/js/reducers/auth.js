const initialState = {
    isAuthenticating: false,
    isAuthenticated: false,
    accessToken: null,
    sessionToken: null,
    user: null,
    error: null
};


export default function auth(state=initialState, action={}) {
    switch (action.type) {
        case 'LOGIN_SUCCESS':
            return Object.assign({}, state, {
                isAuthenticating: false,
                isAuthenticated: true,
                accessToken: action.payload.accessToken,
                sessionToken: action.payload.sessionToken,
                user: action.payload.user,
                error: null
            });

        case 'LOGIN_FAILURE':
            return Object.assign({}, state, {
                isAuthenticating: false,
                isAuthenticated: false,
                accessToken: null,
                sessionToken: null,
                user: null,
                error: action.payload.reason
            });

        case 'LOGOUT':
            return initialState;
    }
    return state;
}