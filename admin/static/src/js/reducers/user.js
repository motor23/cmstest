const initialState = {
    isLoggedIn: false,
    token: null,
    error: null,
    name: 'root'
};


export default function user(state=initialState, action={}) {
    if (action.type === 'AUTH_LOGIN_SUCCESS') {
        return {
            ...initialState,
            isLoggedIn: true,
            token: action.payload.token
        };
    }

    if (action.type === 'AUTH_LOGIN_FAILURE') {
        return {
            ...initialState,
            error: action.payload.reason
        };
    }

    if (action.type === 'AUTH_LOGOUT') {
        return {
            ...initialState
        };
    }

    return state;
}