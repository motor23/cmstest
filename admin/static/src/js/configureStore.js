import {createStore, applyMiddleware, combineReducers} from 'redux';
import createLogger from 'redux-logger';
import {user, config} from './reducers';


const thunkMiddleware = store => next => action => {
    if (typeof action === 'function') {
        return action(store.dispatch, store.getState, window.connection);
    }
    return next(action);
};


const loggerMiddleware = store => next => action => {
    console.log('[dispatching]', action);
    const result = next(action);
    console.log('[next state]', store.getState());
    return result;
};


const connectionMiddleware = store => next => action => {
    if (typeof action.endpoint === 'string') {
        window.connection.send({name: action.endpoint, body: action.payload});
    }
    return next(action);
};


export default function configureStore(initialState) {
    const reducer = combineReducers({
        user: user,
        config: config
    });
    const middleware = applyMiddleware(
        thunkMiddleware,
        loggerMiddleware,
        connectionMiddleware
    );
    return createStore(reducer, initialState, middleware);
};