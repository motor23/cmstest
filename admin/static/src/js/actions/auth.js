import {confUpdate} from './conf';


export function logout() {
    localStorage.removeItem('token');
    return {
        type: 'AUTH_LOGOUT'
    };
}


export function loginRequest({token, login, password}) {
    return {
        type: 'AUTH_LOGIN_REQUEST',
        payload: {
            token: token,
            login: login,
            password: password
        }
    };
}


export function loginSuccess(token) {
    localStorage.setItem('token', token);
    return {
        type: 'AUTH_LOGIN_SUCCESS',
        payload: {
            token: token
        }
    };
}


export function loginFailure(reason) {
    localStorage.removeItem('token');
    return {
        type: 'AUTH_LOGIN_FAILURE',
        payload: {
            reason: reason
        }
    };
}


export function loginWithPassword(login, password) {
    return (dispatch, state, connection) => {
        dispatch(loginRequest({login, password}));
        connection.call('auth.login', {login, password}).then(payload => {
            if (payload.status === 'ok') {
                dispatch(loginSuccess(payload.key));
                dispatch(confUpdate())
            }
            if (payload.status === 'failed') {
                dispatch(loginFailure(payload.reason));
            }
        });
    };
}


export function loginWithToken(token) {
    return (dispatch, state, connection) => {
        dispatch(loginRequest({token}));
        connection.call('auth.login', {key: token}).then(payload => {
            if (payload.status === 'ok') {
                dispatch(loginSuccess(payload.key));
                dispatch(confUpdate())
            }
            if (payload.status === 'failed') {
                dispatch(loginFailure(payload.reason));
            }
        });
    };
}