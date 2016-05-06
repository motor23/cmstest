import {createStore, applyMiddleware} from 'redux';
import createLogger from 'redux-logger';


const LOGIN_REQUEST = 'LOGIN_REQUEST';
const LOGIN_SUCCESS = 'LOGIN_SUCCESS';
const LOGIN_FAILURE = 'LOGIN_FAILURE';


function loginRequest(credentials) {
    return {type: LOGIN_REQUEST, credentials: credentials};
}


function loginSuccess(user) {
    return {type: LOGIN_SUCCESS, user: user};
}


function loginFailure(message) {
    return {type: LOGIN_FAILURE, message: message};
}


function reducer(state={}, action={}) {
    switch (action.type) {
        default:
            return state;
    }
}


const thunkMiddleware = store => next => action => {
    if (typeof action === 'function') {
        return action(store.dispatch, store.getState);
    }
    return next(action);
};


const loggerMiddleware = store => next => action => {
    console.log('dispatching', action);
    const result = next(action);
    console.log('next state', store.getState());
    return result;
};


export default function configureStore(initialState) {
    const middlewares = applyMiddleware(thunkMiddleware, loggerMiddleware);
    return createStore(reducer, initialState, middlewares);
}