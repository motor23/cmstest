export function updateStreamListRequest(stream) {
    return {
        type: 'STREAM_UPDATE_REQUEST'
    };
}


export function updateStreamListSuccess(data) {
    return {
        type: 'STREAM_UPDATE_SUCCESS',
        payload: data
    };
}


export function updateStreamListFailure(reason) {
    return {
        type: 'STREAM_UPDATE_FAILURE',
        payload: {
            reason: reason
        }
    };
}


export function updateStreamList(stream, page, pageSize) {
    return (dispatch, state, connection) => {
        const payload = {
            stream: stream,
            page_size: pageSize,
            page: page,
            action: 'list',
            order: '+id'
        };
        dispatch(updateStreamListRequest());
        connection.call('streams.action', payload).then(payload => {
            dispatch(updateStreamListSuccess(payload));
        })
    };
}