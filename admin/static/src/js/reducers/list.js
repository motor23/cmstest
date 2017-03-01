const initialState = {
    isLoading: true,
    title: null,
    stream: null,
    items: [],
    filters: {},
    errors: {},
    total: 0,
    pageSize: 20,
    page: 1,
    order: '+id'
};


export function list(state=initialState, {type, payload}={}) {
    if (type === 'STREAM_LIST_PENDING') {
        return {
            ...initialState,
            isLoading: true
        };
    }

    if (type === 'STREAM_LIST_SUCCESS') {
        return {
            ...state,
            isLoading: false,
            title: payload.title,
            stream: payload.stream,
            items: payload.items,
            filters: payload.filters,
            errors: payload.errors,
            total: payload.total,
            pageSize: payload.page_size,
            page: payload.page
        };
    }

    return state;
}