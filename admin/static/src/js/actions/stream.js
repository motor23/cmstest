export const STREAM_LIST_PENDING = 'STREAM_LIST_PENDING';
export const STREAM_LIST_SUCCESS = 'STREAM_LIST_SUCCESS';
export const STREAM_LIST_FAILURE = 'STREAM_LIST_FAULURE';
export const STREAM_GET_PENDING = 'STREAM_GET_PENDING';
export const STREAM_GET_SUCCESS = 'STREAM_GET_SUCCESS';
export const STREAM_GET_FAILURE = 'STREAM_GET_FAILURE';


export function streamList({stream, page, pageSize}) {
    return ({dispatch, state, api}) => ({
        type: 'STREAM_LIST',
        payload: api.call('streams.action', {action: 'list', stream: stream, page: page, page_size: pageSize, order: '+id'})
            .then(response => response)
            .catch(error => error)
    });
}


export function streamGet({stream, itemId}) {
    return ({dispatch, state, api}) => ({
        type: 'STREAM_GET',
        payload: api.call('streams.action', {action: 'get', stream: stream, item_id: itemId})
            .then(response => response)
            .catch(error => error)
    });
}
