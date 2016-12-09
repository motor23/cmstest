export const LOGIN_PENDING = 'LOGIN_PENDING';
export const LOGIN_SUCCESS = 'LOGIN_SUCCESS';
export const LOGIN_FAILURE = 'LOGIN_FAILURE';
export const LOGOUT_PENDING = 'LOGOUT_PENDING';
export const LOGOUT_SUCCESS = 'LOGOUT_SUCCESS';
export const LOGOUT_FAILURE = 'LOGOUT_FAILURE';
export const CONFIGURE_PENDING = 'CONFIGURE_PENDING';
export const CONFIGURE_SUCCESS = 'CONFIGURE_SUCCESS';
export const CONFIGURE_FAILURE = 'CONFIGURE_FAILURE';


export function login({token, login, password}) {
    return (dispatch, state, api) => ({
        type: 'LOGIN',
        payload: api.call('auth.login', {token, login, password})
            .then(response => response)
            .catch(error => error)
    });
}


export function logout({token}) {
    return (dispatch, state, api) => ({
        type: 'LOGOUT',
        payload: api.call('auth.logout', {token})
            .then(response => response)
            .catch(error => error)
    });
}


export function configure() {
    return (dispatch, state, api) => ({
        type: 'CONFIGURE',
        payload: api.call('cfg.cinfo')
            .then(response => response)
            .catch(error => errro)
    });
}