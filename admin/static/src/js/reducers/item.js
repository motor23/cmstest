const initialState = {
    loading: true,
    errors: {},
    id: null,
    stream: null,
    fields: [],
    values: {}
};


export function item(state=initialState, {type, payload}={}) {
    if (type === 'ITEM_FETCH_PENDING') {
        return {
            ...state,
            loading: true
        };
    }

    if (type === 'ITEM_FETCH_SUCCESS') {
        return {
            ...state,
            loading: false,
            errors: payload.errors,
            id: payload.item_id,
            stream: payload.stream,
            fields: payload.item_fields,
            values: payload.item
        };
    }

    if (type === 'ITEM_UPDATE_SUCCESS') {
        const values = state.values;
        const newValues = payload.values;
        return {
            ...state,
            errors: payload.errors,
            id: payload.item_id,
            values: {...values, ...newValues}
        }
    }

    return state;
}