import {createStore, applyMiddleware, combineReducers} from 'redux';


const injectDependencies = dependencies => store => next => action => {
    if (typeof action === 'function') {
        const {dispatch, getState} = store;
        return dispatch(action({dispatch, getState, ...dependencies}));
    }
    return next(action);
};


const logActions = store => next => action => {
    console.groupCollapsed(action.type);
    console.log('Payload: ', action.payload);
    console.log('State: ', store.getState());
    console.groupEnd();
    return next(action);
};


const resolvePromises = store => next => action => {
    const PENDING_TYPE = `${action.type}_PENDING`;
    const SUCCESS_TYPE = `${action.type}_SUCCESS`;
    const FAILURE_TYPE = `${action.type}_FAILURE`;
    const {dispatch} = store;
    const {type, payload} = action;
    if (payload && typeof payload.then === 'function') {
        const fullfill = value => dispatch({type: SUCCESS_TYPE, payload: value});
        const reject = reason => dispatch({type: FAILURE_TYPE, payload: reason});
        next({type: PENDING_TYPE, payload: payload});
        return payload.then(fullfill, reject);
    }
    return next(action);
};


export default function configureStore(initialState, {reducers, api}) {
    const reducer = combineReducers(reducers);
    const middleware = applyMiddleware(
        injectDependencies({api}),
        resolvePromises,
        logActions
    );
    return createStore(reducer, initialState, middleware);
};