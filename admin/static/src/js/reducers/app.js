const initialState = {
    isConnected: false,
    isLogged: false,
    isConfigured: false,
    shouldReloadPage: false,
    location: {}
};


export function app(state=initialState, action={}) {
    switch (action.type) {
        case 'CONNECTION_OPENED':
            return {
                ...initialState,
                isConnected: true
            };
        case 'CONNECTION_CLOSED':
            return {
                ...initialState,
                isConnected: false,
                shouldReloadPage: action.payload.shouldReloadPage ? true : false
            };
        case 'LOGIN_SUCCESS':
            return {
                ...initialState,
                isConnected: true,
                isLogged: true
            };
        case 'LOGIN_FAILURE':
            return {
                ...initialState,
                isConnected: true,
                isLogged: false
            };
        case 'LOGOUT_SUCCESS':
            return {
                ...initialState,
                isLogged: false
            };
        case 'CONFIGURE_SUCCESS':
            return {
                ...initialState,
                isLogged: true,
                isConnected: true,
                isConfigured: true,
                cfg: action.payload.cfg
            };
        case 'PUSH':
            return {
                ...state,
                location: action.payload
            };
    }
    return state;
}