export const ITEM_FETCH         = 'ITEM_FETCH';
export const ITEM_FETCH_REQUEST = 'ITEM_FETCH_REQUEST';
export const ITEM_FETCH_SUCCESS = 'ITEM_FETCH_SUCCESS';
export const ITEM_FETCH_FAILURE = 'ITEM_FETCH_FAILURE';

export const ITEM_UPDATE         = 'ITEM_UPDATE';
export const ITEM_UPDATE_REQUEST = 'ITEM_UPDATE_REQUEST';
export const ITEM_UPDATE_SUCCESS = 'ITEM_UPDATE_SUCCESS';
export const ITEM_UPDATE_FAILURE = 'ITEM_UPDATE_FAILURE';

export const ITEM_CREATE         = 'ITEM_CREATE';
export const ITEM_CREATE_REQUEST = 'ITEM_CREATE_REQUEST';
export const ITEM_CREATE_SUCCESS = 'ITEM_CREATE_SUCCESS';
export const ITEM_CREATE_FAILURE = 'ITEM_CREATE_FAILURE';

export const ITEM_DELETE         = 'ITEM_DELETE';
export const ITEM_DELETE_REQUEST = 'ITEM_DELETE_REQUEST';
export const ITEM_DELETE_SUCCESS = 'ITEM_DELETE_SUCCESS';
export const ITEM_DELETE_FAILURE = 'ITEM_DELETE_FAILURE';


export function fetchItem({stream, id}) {
    return ({dispatch, state, api}) => ({
        type: ITEM_FETCH,
        payload: api.call('streams.action', {action: 'get_item', stream: stream, item_id: parseInt(id)})
    });
}


export function updateItem({stream, id, values}) {
    return ({dispatch, state, api}) => ({
        type: ITEM_UPDATE,
        payload: api.call('streams.action', {action: 'update_item', stream: stream, item_id: parseInt(id), values: values})
    })
}