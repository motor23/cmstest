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
            dispatch(loginSuccess(payload.token));
            dispatch(confUpdate());
        }).catch(payload => dispatch(loginFailure(payload.message)));
    };
}


export function loginWithToken(token) {
    return (dispatch, state, connection) => {
        dispatch(loginRequest({token}));
        connection.call('auth.login', {token: token}).then(payload => {
            dispatch(loginSuccess(payload.token));
            dispatch(confUpdate())
        }).catch(payload => dispatch(loginFailure('Невалидный токен')));
    };
}