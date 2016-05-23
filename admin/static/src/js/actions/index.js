export function configureRequest() {
    return {
        type: 'CONFIG_REQUEST'
    }
}


export function configureUpdate(configuration) {
    return {
        type: 'CONFIG_UPDATE',
        payload: configuration
    }
}


export function logout() {
    localStorage.removeItem('token');
    return {
        type: 'LOGOUT'
    };
}


export function loginRequest() {
    return {
        type: 'LOGIN_REQUEST'
    };
}


export function loginSuccess(token) {
    localStorage.setItem('token', token);
    return {
        type: 'LOGIN_SUCCESS',
        payload: {
            token: token
        }
    };
}


export function loginFailure(reason) {
    localStorage.removeItem('token');
    return {
        type: 'LOGIN_FAILURE',
        payload: {
            reason: reason
        }
    };
}


export function configure() {
    return (dispatch, state, connection) => {
        dispatch(configureRequest());
        connection.call('cinfo.cfg.request').then(payload => {
            dispatch(configureUpdate(payload.cfg));
        });
    };
}


export function loginWithCredentials(login, password) {
    return (dispatch, state, connection) => {
        dispatch(loginRequest());
        connection.call('auth.login.request', {login, password}).then(payload => {
            if (payload.status === 'ok') {
                dispatch(loginSuccess(payload.key));
                dispatch(configure())
            }
            if (payload.status === 'failed') {
                dispatch(loginFailure(payload.reason));
            }
        });
    };
}


export function loginWithToken(token) {
    return (dispatch, state, connection) => {
        dispatch(loginRequest());
        connection.call('auth.login.request', {key: token}).then(payload => {
            if (payload.status === 'ok') {
                dispatch(loginSuccess(payload.key));
                dispatch(configure())
            }
            if (payload.status === 'failed') {
                dispatch(loginFailure(payload.reason));
            }
        });
    };
}


export function updateStreamListRequest(stream) {
    return {
        type: 'STREAM_UPDATE_REQUEST'
    };
}


export function updateStreamListSuccess(data) {
    return {
        type: 'STREAM_UPDATE_SUCCESS',
        payload: data
    };
}


export function updateStreamListFailure(reason) {
    return {
        type: 'STREAM_UPDATE_FAILURE',
        payload: {
            reason: reason
        }
    }
}


export function updateStreamList(stream, limit) {
    return (dispatch, state, connection) => {
        dispatch(updateStreamListRequest());
        connection.call('streams.action.request', {stream, limit, action: 'list'}).then(payload => {
            console.log(payload);
            dispatch(updateStreamListSuccess(payload));
        })
    };
}