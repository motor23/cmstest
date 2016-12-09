import {routerReducer} from 'react-router-redux'
import {createStore, applyMiddleware, combineReducers} from 'redux';
import reducers from './reducers';


function createThunkMiddleware(connection) {
    return store => next => action => {
        if (typeof action === 'function') {
            return action(store.dispatch, store.getState, connection);
        }
        return next(action);
    };
}


function createLoggerMiddleware(logging) {
    return store => next => action => {
        if (logging) {
            console.log('[dispatching]', action);
        }
        const result = next(action);
        if (logging) {
            console.log('[next state]', store.getState());
        }
        return result;
    };
}


function createPromiseMiddleware() {
    return store => next => action => {
        const {dispatch} = store;
        const {type, payload} = action;
        if (payload && typeof payload === 'object' && typeof payload.then === 'function') {
            const PENDING_TYPE = `${type}_PENDING`;
            const SUCCESS_TYPE = `${type}_SUCCESS`;
            const FAILURE_TYPE = `${type}_FAILURE`;
            const fullfill = value => {
                dispatch({type: SUCCESS_TYPE, payload: value});
            };
            const reject = reason => {
                dispatch({type: FAILURE_TYPE, payload: reason});
            };
            next({type: PENDING_TYPE, payload: payload});
            return payload.then(fullfill, reject);
        }
        return next(action);
    }
}


export default function configureStore(initialState, {logging, connection}) {
    const reducer = combineReducers({...reducers});
    const middleware = applyMiddleware(
        createThunkMiddleware(connection),
        createLoggerMiddleware(logging),
        createPromiseMiddleware()
    );
    return createStore(reducer, initialState, middleware);
};