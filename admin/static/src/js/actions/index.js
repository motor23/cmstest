export function config() {
    return {
        type: 'CONFIG_REQUEST',
        endpoint: 'cinfo.cfg'
    }
}


export function configUpdate(configuration) {
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


export function loginWithCredentials(login, password) {
    return {
        type: 'LOGIN_REQUEST',
        endpoint: 'auth.login',
        payload: {
            login: login,
            password: password
        }
    }
}


export function loginWithToken(token) {
    return {
        type: 'LOGIN_REQUEST',
        endpoint: 'auth.login',
        payload: {
            key: token
        }
    };
}


export const endpoints = {
    'auth.login_ok': (dispatch, body) => {dispatch(loginSuccess(body.key)); dispatch(config());},
    'auth.login_error': (dispatch, body) => dispatch(loginFailure(body.reason)),
    'cinfo.cfg_response': (dispatch, body) => dispatch(configUpdate(body))
};