export function config(state, action) {
    const initialState = {
        auth: null,
        cinfo: null,
        menu: {
            dashboard: null,
            main: null
        }
    };

    state = state || initialState;
    if (action.type === 'CONFIG_UPDATE') {
        return Object.assign({}, state, {
            auth: action.payload.auth,
            cinfo: action.payload.cinfo,
            menu: action.payload.menu
        });
    }
    return state
}


export function user(state, action) {
    const initialState = {
        isLoggedIn: false,
        token: null,
        error: null
    };

    state = state || initialState;

    if (action.type === 'LOGIN_SUCCESS') {
        return Object.assign({}, state, {
            isLoggedIn: true,
            token: action.payload.token
        });
    }

    if (action.type === 'LOGIN_FAILURE') {
        return Object.assign({}, state, {
            isLoggedIn: false,
            token: null,
            error: action.payload.reason
        });
    }

    if (action.type === 'LOGOUT') {
        return Object.assign({}, state, {
            isLoggedIn: false,
            token: null,
            error: null
        });
    }

    return state;
}