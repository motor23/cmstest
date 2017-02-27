const initialState = {
    status: 'CONNECTING',
    isConnected: false,
    isLogged: false,
    isConfigured: false,
    shouldReloadPage: false,
    menu: [],
    dashboard: []
};


export function app(state=initialState, action={}) {
    switch (action.type) {
        case 'CONNECTION_OPENED':
            return {
                ...state,
                isConnected: true,
                status: 'CONNECTED'
            };
        case 'CONNECTION_CLOSED':
            return {
                ...state,
                isConnected: false,
                status: 'CONNECTING'
            };
        case 'LOGIN_SUCCESS':
            return {
                ...state,
                isConnected: true,
                isLogged: true
            };
        case 'LOGIN_FAILURE':
            return {
                ...state,
                isConnected: true,
                isLogged: false
            };
        case 'LOGOUT_SUCCESS':
            return {
                ...state,
                isLogged: false
            };
        case 'CONFIGURE_SUCCESS':
            return {
                ...state,
                isLogged: true,
                isConnected: true,
                isConfigured: true,
                cfg: action.payload.cfg, /* deprecated */
                menu: action.payload.cfg.menu.main,
                dashboard: action.payload.cfg.menu.dashboard
            };
        case 'PUSH':
            return {
                ...state,
                location: action.payload
            };
    }
    return state;
}