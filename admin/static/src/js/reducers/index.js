export function config(state, action) {
    const initialState = {
        auth: null,
        cinfo: null,
        menu: {
            dashboard: [],
            main: []
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
        error: null,
        name: 'root'
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


export function stream(state, action) {
    const initialState = {
        isLoading: true,
        stream: null,
        items: [],
        filters: {},
        errors: {},
        total: 0,
        limit: 20,
        offset: 0
    };

    state = state || initialState;

    if (action.type === 'STREAM_UPDATE_REQUEST') {
        return Object.assign({}, state, {
            isLoading: true,
            stream: null,
            items: [],
            filters: {},
            errors: {},
            total: 0,
            limit: 20,
            offset: 0
        });
    }

    if (action.type === 'STREAM_UPDATE_SUCCESS') {
        return Object.assign({}, state, {
            isLoading: false,
            stream: action.payload.stream,
            items: action.payload.items,
            filters: action.payload.filters,
            errors: action.payload.errors,
            total: action.payload.total,
            limit: action.payload.limit,
            offset: action.payload.offset
        });
    }

    return state;
}