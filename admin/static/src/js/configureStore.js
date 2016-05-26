import {routerReducer} from 'react-router-redux'
import {createStore, applyMiddleware, combineReducers} from 'redux';
import createLogger from 'redux-logger';
import {user, config, stream} from './reducers';


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


export default function configureStore(initialState, {logging, connection}) {
    const reducer = combineReducers({
        user: user,
        config: config,
        stream: stream,
        routing: routerReducer
    });
    const middleware = applyMiddleware(
        createThunkMiddleware(connection),
        createLoggerMiddleware(logging)
    );
    return createStore(reducer, initialState, middleware);
};