export function confUpdateRequest() {
    return {
        type: 'CONF_UPDATE_REQUEST'
    };
}


export function confUpdateSuccess(conf) {
    return {
        type: 'CONF_UPDATE_SUCCESS',
        payload: conf
    };
}


export function confUpdate() {
    return (dispatch, state, connection) => {
        dispatch(confUpdateRequest());
        connection.call('cinfo.cfg').then(payload => {
            dispatch(confUpdateSuccess(payload.cfg));
        });
    };
}